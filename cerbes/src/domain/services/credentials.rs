use crate::domain::adapters::database::CredentialsRepositoryTrait;
use crate::domain::adapters::database::PermissionsRepositoryTrait;
use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::adapters::publisher::PublisherTrait;
use crate::domain::entities::Credentials;
use crate::domain::errors::CerbesError;
use uuid::Uuid;

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

pub async fn impersonate_user<U, P>(
    user_id: Uuid,
    impersonator_id: Uuid,
    user_repo: &U,
    permissions_repo: &P,
) -> Result<String, CerbesError>
where
    U: UserRepositoryTrait,
    P: PermissionsRepositoryTrait,
{
    let user = user_repo.get_by_public_id(user_id).await?;
    let impersonator = user_repo.get_by_public_id(impersonator_id).await?;
    let permissions = permissions_repo
        .get_permissions_for_user(&impersonator)
        .await?;

    if !permissions.iter().any(|p| p.impersonate) {
        return Err(CerbesError::not_enough_permissions());
    }

    return Ok(user.generate_jwt_with_impersonator(&impersonator));
}

pub async fn register_user_login<C>(repo: &C, creds: &Credentials) -> Result<(), CerbesError>
where
    C: CredentialsRepositoryTrait,
{
    repo.register_login(creds, chrono::Utc::now().naive_utc())
        .await?;
    Ok(())
}
