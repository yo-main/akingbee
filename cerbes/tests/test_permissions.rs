use cerbes::domain::adapters::database::*;
use cerbes::domain::entities::Credentials;
use cerbes::domain::entities::User;
use cerbes::infrastructure::database::repository::CredentialsRepository;
use cerbes::infrastructure::database::repository::PermissionsRepository;
use cerbes::infrastructure::database::repository::UserRepository;
use sea_orm::DatabaseConnection;

mod common;

async fn get_user(conn: DatabaseConnection) -> User {
    let rep = UserRepository::new(conn.clone());
    let cred_rep = CredentialsRepository::new(conn);
    let creds = Credentials::new("user".to_owned(), "pwd".to_owned());
    let user = User::new("email".to_owned(), creds);

    cred_rep.save(&user.credentials).await.unwrap();
    rep.save(&user).await.unwrap();
    return user;
}

#[tokio::test]
async fn test_no_permission() {
    let conn = common::database::get_db().await;
    let user = get_user(conn.clone()).await;

    let repo = PermissionsRepository::new(conn.clone());
    let permissions = repo.get_permissions_for_user(&user).await.unwrap();
    assert!(permissions.is_empty())
}

#[tokio::test]
async fn test_with_permissions() {
    let conn = common::database::get_db().await;
    let user = get_user(conn.clone()).await;

    let repo = PermissionsRepository::new(conn.clone());
    let permissions = repo.get_permissions_for_user(&user).await.unwrap();
    assert!(permissions.is_empty())
}
