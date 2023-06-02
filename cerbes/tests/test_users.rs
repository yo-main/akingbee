use cerbes::domain::adapters::database::*;
use cerbes::domain::entities::Credentials;
use cerbes::infrastructure::database::repository::{CredentialsRepository, UserRepository};

mod common;

#[tokio::test]
async fn test_user_creation() {
    let conn = common::database::get_db().await;

    let creds = Credentials::new("user".to_owned(), "pwd".to_owned());
    let user = cerbes::domain::entities::User::new("email".to_owned(), creds);

    let cred_rep = CredentialsRepository::new(conn.clone());
    let repo = UserRepository::new(conn);
    cred_rep.save(&user.credentials).await.unwrap();
    repo.create(&user).await.unwrap();

    let user_created = repo.get_by_public_id(user.public_id).await.unwrap();

    assert_eq!(user.public_id, user_created.public_id);
    assert_eq!(user.email, user_created.email);
}
