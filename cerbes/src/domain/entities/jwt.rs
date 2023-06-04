use crate::domain::entities::User;
use crate::domain::errors::CerbesError;
use crate::settings::SETTINGS;
use serde::Deserialize;
use serde::Serialize;

use uuid::Uuid;

#[derive(Serialize, Deserialize)]
pub struct Jwt {
    pub impersonator: Option<Uuid>,
    pub admin: bool,
    pub sub: Uuid,
    pub iss: String,
    pub exp: usize,
    pub username: String,
    pub email: String,
}

impl Jwt {
    pub fn from_user(user: &User) -> Self {
        Jwt {
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

    pub fn refresh(self) -> Self {
        Jwt {
            admin: self.admin,
            impersonator: self.impersonator,
            sub: self.sub,
            iss: self.iss,
            exp: (chrono::Utc::now() + chrono::Duration::hours(1)).timestamp() as usize,
            email: self.email,
            username: self.username,
        }
    }

    pub fn get_token(&self) -> String {
        jsonwebtoken::encode(
            &jsonwebtoken::Header::default(),
            &self,
            &jsonwebtoken::EncodingKey::from_secret(SETTINGS.jwt_key.as_ref()),
        )
        .unwrap()
    }

    pub fn validate_jwt(token: String) -> Result<Jwt, CerbesError> {
        let jwt = jsonwebtoken::decode::<Jwt>(
            &token,
            &jsonwebtoken::DecodingKey::from_secret(SETTINGS.jwt_key.as_ref()),
            &jsonwebtoken::Validation::new(jsonwebtoken::Algorithm::HS256),
        );

        match jwt {
            Ok(token) => Ok(token.claims),
            _ => Err(CerbesError::invalid_jwt()),
        }
    }

    pub fn set_impersonator(&mut self, impersonator: &User) {
        self.impersonator = Some(impersonator.public_id);
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::domain::entities::Credentials;
    use crate::domain::entities::User;

    #[test]
    fn test_jwt_validation_success() {
        let credentials = Credentials::new("username".to_owned(), "password".to_owned());
        let user = User::new("email".to_owned(), credentials);
        let token = user.generate_jwt();
        assert!(Jwt::validate_jwt(token.to_string()).is_ok());
    }

    #[test]
    fn test_jwt_data() {
        let credentials = Credentials::new("username".to_owned(), "password".to_owned());
        let user = User::new("email".to_owned(), credentials);
        let jwt = Jwt::from_user(&user);

        assert_eq!(jwt.admin, false);
        assert_eq!(jwt.impersonator, None);
        assert_eq!(jwt.sub, user.public_id);
        assert_eq!(jwt.iss, "cerbes".to_owned());
        assert_eq!(jwt.email, user.email);
        assert_eq!(jwt.username, user.credentials.username);
    }

    #[test]
    fn test_jwt_data_admin() {
        let credentials = Credentials::new("Romain".to_owned(), "password".to_owned());
        let user = User::new("email".to_owned(), credentials);
        let jwt = Jwt::from_user(&user);

        assert_eq!(jwt.admin, true);
        assert_eq!(jwt.impersonator, None);
        assert_eq!(jwt.sub, user.public_id);
        assert_eq!(jwt.iss, "cerbes".to_owned());
        assert_eq!(jwt.email, user.email);
        assert_eq!(jwt.username, user.credentials.username);
    }

    #[test]
    fn test_jwt_refresh() {
        let credentials = Credentials::new("Romain".to_owned(), "password".to_owned());
        let user = User::new("email".to_owned(), credentials);
        let jwt = Jwt::from_user(&user);
        let refreshed = Jwt::refresh(jwt);

        assert_eq!(refreshed.admin, true);
        assert_eq!(refreshed.impersonator, None);
        assert_eq!(refreshed.sub, user.public_id);
        assert_eq!(refreshed.iss, "cerbes".to_owned());
        assert_eq!(refreshed.email, user.email);
        assert_eq!(refreshed.username, user.credentials.username);
    }

    #[test]
    fn test_jwt_impersonator() {
        let credentials = Credentials::new("username".to_owned(), "password".to_owned());
        let user = User::new("email".to_owned(), credentials);
        let credentials = Credentials::new("username".to_owned(), "password".to_owned());
        let impersonator = User::new("email2".to_owned(), credentials);
        let mut jwt = Jwt::from_user(&user);
        jwt.set_impersonator(&impersonator);

        assert_eq!(jwt.impersonator, Some(impersonator.public_id));
    }

    #[test]
    fn test_jwt_impersonator_refreshed() {
        let credentials = Credentials::new("username".to_owned(), "password".to_owned());
        let user = User::new("email".to_owned(), credentials);
        let credentials = Credentials::new("username".to_owned(), "password".to_owned());
        let impersonator = User::new("email2".to_owned(), credentials);
        let mut jwt = Jwt::from_user(&user);
        jwt.set_impersonator(&impersonator);

        assert_eq!(jwt.impersonator, Some(impersonator.public_id));

        let refreshed = jwt.refresh();

        assert_eq!(refreshed.impersonator, Some(impersonator.public_id));
    }

    #[test]
    fn test_jwt_validation_fails() {
        let data = Jwt {
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

        let token = Jwt::validate_jwt(token.to_string());
        assert!(token.is_err())
    }
}
