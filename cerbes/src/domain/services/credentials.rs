use crate::domain::adapters::database::CredentialsRepositoryTrait;
use crate::domain::adapters::database::PermissionsRepositoryTrait;
use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::adapters::publisher::PublisherTrait;
use crate::domain::entities::Credentials;
use crate::domain::entities::User;
use crate::domain::errors::CerbesError;
use crate::settings::SETTINGS;
use serde::Deserialize;
use serde::Serialize;
use uuid::Uuid;

#[derive(Serialize, Deserialize)]
pub struct JwtData {
    pub impersonator: Option<Uuid>,
    pub admin: bool,
    pub sub: Uuid,
    pub iss: String,
    pub exp: usize,
    pub username: String,
    pub email: String,
}

impl JwtData {
    fn from_user(user: &User) -> Self {
        JwtData {
            // TODO: remove that hack at some point - and blame the lazy me for not doing it now
            admin: if user.credentials.username == "Romain" {
                true
            } else {
                false
            },
            impersonator: None,
            sub: user.public_id,
            iss: "cerbes".to_owned(),
            exp: (chrono::Utc::now() + chrono::Duration::hours(1)).timestamp() as usize,
            email: user.email.to_string(),
            username: user.credentials.username.to_string(),
        }
    }

    fn refresh(self) -> Self {
        JwtData {
            admin: self.admin,
            impersonator: self.impersonator,
            sub: self.sub,
            iss: self.iss,
            exp: (chrono::Utc::now() + chrono::Duration::hours(1)).timestamp() as usize,
            email: self.email,
            username: self.username,
        }
    }
}

pub fn validate_token(token: String) -> Result<JwtData, CerbesError> {
    let jwt = jsonwebtoken::decode::<JwtData>(
        &token,
        &jsonwebtoken::DecodingKey::from_secret(SETTINGS.jwt_key.as_ref()),
        &jsonwebtoken::Validation::new(jsonwebtoken::Algorithm::HS256),
    );

    match jwt {
        Ok(token) => Ok(token.claims),
        _ => Err(CerbesError::invalid_jwt()),
    }
}

pub fn generate_jwt_for_user(user: &User) -> String {
    let data = JwtData::from_user(&user);
    let token = jsonwebtoken::encode(
        &jsonwebtoken::Header::default(),
        &data,
        &jsonwebtoken::EncodingKey::from_secret(SETTINGS.jwt_key.as_ref()),
    )
    .unwrap();

    return token;
}

pub fn generate_jwt_for_impersonator(impersonator: User, target: User) -> String {
    let mut data = JwtData::from_user(&target);
    data.impersonator = Some(impersonator.public_id);
    let token = jsonwebtoken::encode(
        &jsonwebtoken::Header::default(),
        &data,
        &jsonwebtoken::EncodingKey::from_secret(SETTINGS.jwt_key.as_ref()),
    )
    .unwrap();

    return token;
}

pub fn regenerate_jwt(token: JwtData) -> String {
    let token = jsonwebtoken::encode(
        &jsonwebtoken::Header::default(),
        &token.refresh(),
        &jsonwebtoken::EncodingKey::from_secret(SETTINGS.jwt_key.as_ref()),
    )
    .unwrap();

    return token;
}

pub async fn register_password_reset_request<R, P>(
    username: &str,
    repo: &R,
    publisher: &P,
) -> Result<(), CerbesError>
where
    R: UserRepositoryTrait,
    P: PublisherTrait,
{
    let mut user = repo.get_by_username(username).await;

    if user.is_err() {
        user = repo.get_by_user_email(username).await;
    }

    let mut user = user?;

    user.request_password_reset();
    repo.update(&user).await?;

    publisher
        .publish(
            "user.reset_password",
            &serde_json::json!({
                "language": "fr",
                "user": {
                    "email": user.email,
                    "id": user.public_id,
                },
                "reset_link": format!("https://akingbee.com/password-reset/{}/{}", user.public_id, user.credentials.password_reset_id.unwrap())
            })
            .to_string(),
        )
        .await?;

    return Ok(());
}

pub async fn password_reset_validate<R>(user_id: Uuid, reset_id: Uuid, repo: &R) -> bool
where
    R: CredentialsRepositoryTrait,
{
    match repo.get_by_user_public_id(user_id).await {
        Ok(user) => user.credentials.password_reset_id.unwrap_or_default() == reset_id,
        Err(_) => false,
    }
}

pub async fn impersonate_user<U, R, P>(
    user_id: Uuid,
    impersonator_id: Uuid,
    user_repo: &U,
    credentials_repo: &R,
    permissions_repo: &P,
) -> Result<String, CerbesError>
where
    U: UserRepositoryTrait,
    R: CredentialsRepositoryTrait,
    P: PermissionsRepositoryTrait,
{
    let user = credentials_repo.get_by_user_public_id(user_id).await?;
    let impersonator = user_repo.get_by_public_id(impersonator_id).await?;
    let permissions = permissions_repo
        .get_permissions_for_user(&impersonator)
        .await?;

    if !permissions.iter().any(|p| p.impersonate) {
        return Err(CerbesError::not_enough_permissions());
    }

    return Ok(generate_jwt_for_impersonator(impersonator, user));
}

pub async fn register_user_login<C>(repo: &C, creds: &Credentials) -> Result<(), CerbesError>
where
    C: CredentialsRepositoryTrait,
{
    repo.register_login(creds, chrono::Utc::now().naive_utc())
        .await?;
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_jwt_validation_success() {
        let credentials = Credentials::new("username".to_owned(), "password".to_owned());
        let user = User::new("email".to_owned(), credentials);
        let token = generate_jwt_for_user(&user);
        assert!(validate_token(token.to_string()).is_ok());
    }

    #[test]
    fn test_jwt_validation_fails() {
        let data = JwtData {
            admin: false,
            impersonator: None,
            sub: Uuid::new_v4(),
            iss: "cerbes".to_owned(),
            exp: (chrono::Utc::now() - chrono::Duration::hours(3)).timestamp() as usize,
            email: "aze".to_owned(),
            username: "username".to_owned(),
        };

        let token = jsonwebtoken::encode(
            &jsonwebtoken::Header::default(),
            &data,
            &jsonwebtoken::EncodingKey::from_secret("test".as_ref()),
        )
        .unwrap();

        let token = validate_token(token.to_string());
        assert!(token.is_err())
    }
}
