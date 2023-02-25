use cerbes::domain::adapters::database::*;
use cerbes::infrastructure::database::repository::UserRepository;

mod common;

#[tokio::test]
async fn test_user_creation() {
    let conn = common::database::get_db().await;

    let user = cerbes::domain::models::User::new("email".to_owned());
    let repo = UserRepository::new(conn);
    repo.create_user(&user).await.unwrap();

    let user_created = repo.get_by_public_id(user.public_id).await.unwrap();

    assert_eq!(user.public_id, user_created.public_id);
    assert_eq!(user.email, user_created.email);
}
