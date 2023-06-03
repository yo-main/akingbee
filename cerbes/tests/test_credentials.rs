use cerbes::domain::adapters::database::*;
use cerbes::domain::entities::Credentials;
use cerbes::domain::entities::User;
use cerbes::infrastructure::database::repository::UserRepository;

mod common;

#[tokio::test]
async fn test_credentials_creation() {
    let conn = common::database::get_db().await;
    let user_repo = UserRepository::new(conn.clone());

    let creds = Credentials::new("username".to_owned(), "password".to_owned());
    let user = User::new("email".to_owned(), creds);
    user_repo.create(&user).await.unwrap();

    let new_user = user_repo.get_by_public_id(user.public_id).await.unwrap();

    assert_eq!(new_user.public_id, user.public_id);
    let creds = new_user.credentials;
    assert_eq!(creds.username, "username");
    assert_eq!(
        creds.password,
        "600c10feb7b03d284eed76d71ae61feacc9e7bd6508ecb97bfc3d7f197a4753d"
    );
}
