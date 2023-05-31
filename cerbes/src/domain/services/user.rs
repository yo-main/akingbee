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
    let mut user = User::new(email);
    let credentials = credentials::create_credentials(username, password);

    // TODO: find a way to wrap those 2 operations in the same transaction
    user_repo.save(&user).await?;
    cred_repo.save(&user, &credentials).await?;

    user.credentials = Some(credentials);
    publisher
        .publish("user.created", &user.to_json().to_string())
        .await?;

    return Ok(user);
}
