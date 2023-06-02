use core::panic;

use crate::domain::adapters::database::CredentialsRepositoryTrait;
use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::adapters::publisher::PublisherTrait;
use crate::domain::entities::Credentials;
use crate::domain::entities::User;
use crate::domain::errors::CerbesError;
use uuid::Uuid;

pub async fn create_user<R, D, Q>(
    email: String,
    username: String,
    password: String,
    user_repo: &R,
    cred_repo: &D,
    publisher: &Q,
) -> Result<User, CerbesError>
where
    R: UserRepositoryTrait,
    D: CredentialsRepositoryTrait,
    Q: PublisherTrait,
{
    let credentials = Credentials::new(username, password);
    let user = User::new(email, credentials);

    // TODO: find a way to wrap those 2 operations in the same transaction
    cred_repo.save(&user.credentials).await?;
    user_repo.create(&user).await?;

    publisher
        .publish("user.created", &user.to_json().to_string())
        .await?;

    return Ok(user);
}

pub async fn password_reset<R>(
    user_id: Uuid,
    reset_id: Uuid,
    password: String,
    repo: &R,
) -> Result<(), CerbesError>
where
    R: UserRepositoryTrait,
{
    let mut user = repo.get_by_public_id(user_id).await?;
    user.update_password(password, reset_id)?;

    repo.update(&user).await
}

pub async fn user_login<R>(
    username: String,
    password: String,
    user_repo: &R,
) -> Result<String, CerbesError>
where
    R: UserRepositoryTrait,
{
    let mut user = user_repo.get_by_username(&username).await?;

    if !user.validate_password(password) {
        return Err(CerbesError::not_enough_permissions());
    }

    user.register_login();
    user_repo.update(&user).await?;

    Ok(user.generate_jwt())
}
