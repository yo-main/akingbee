use cerbes::domain::adapters::database::*;
use cerbes::domain::entities::Credentials;
use cerbes::domain::entities::User;
use cerbes::infrastructure::database::repository::PermissionRepositoryPg;
use cerbes::infrastructure::database::repository::UserRepositoryPg;
use sea_orm::DatabaseConnection;

mod common;

async fn get_user(conn: DatabaseConnection) -> User {
    let rep = UserRepositoryPg::new(conn.clone());
    let creds = Credentials::new("user".to_owned(), "pwd".to_owned());
    let user = User::new("email".to_owned(), creds);

    rep.create(&user).await.unwrap();
    return user;
}

#[tokio::test]
async fn test_no_permission() {
    let conn = common::database::get_db().await;
    let user = get_user(conn.clone()).await;

    let repo = PermissionRepositoryPg::new(conn.clone());
    let permissions = repo.get_permissions_for_user(&user).await.unwrap();
    assert!(permissions.is_empty())
}

#[tokio::test]
async fn test_with_permissions() {
    let conn = common::database::get_db().await;
    let user = get_user(conn.clone()).await;

    let repo = PermissionRepositoryPg::new(conn.clone());
    let permissions = repo.get_permissions_for_user(&user).await.unwrap();
    assert!(permissions.is_empty())
}
