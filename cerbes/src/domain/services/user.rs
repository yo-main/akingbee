use crate::domain::adapters::database::CredentialsRepositoryTrait;
use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::adapters::publisher::PublisherTrait;
use crate::domain::entities::User;
use crate::domain::errors::CerbesError;
use crate::domain::services::credentials;

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
    let credentials = credentials::create_credentials(username, password);
    let user = User::new(email, credentials);

    // TODO: find a way to wrap those 2 operations in the same transaction
    cred_repo.save(&user.credentials).await?;
    user_repo.save(&user).await?;

    publisher
        .publish("user.created", &user.to_json().to_string())
        .await?;

    return Ok(user);
}
