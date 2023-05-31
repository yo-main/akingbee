use cerbes::domain::adapters::database::*;
use cerbes::domain::entities::Credentials;
use cerbes::domain::entities::User;
use cerbes::infrastructure::database::repository::CredentialsRepository;
use cerbes::infrastructure::database::repository::UserRepository;

mod common;

#[tokio::test]
async fn test_credentials_creation() {
    let conn = common::database::get_db().await;
    let user_repo = UserRepository::new(conn.clone());
    let creds_repo = CredentialsRepository::new(conn.clone());

    let user = User::new("email".to_owned());
    user_repo.save(&user).await.unwrap();

    let creds = Credentials::new("username".to_owned(), "password".to_owned());
    creds_repo.save(&creds).await.unwrap();

    let new_user = creds_repo
        .get_by_user_public_id(user.public_id)
        .await
        .unwrap();

    assert_eq!(new_user.public_id, user.public_id);
    let creds = new_user.credentials.unwrap();
    assert_eq!(creds.username, "username");
    assert_eq!(creds.password, "password");
}
