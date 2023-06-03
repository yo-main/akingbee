use axum::body::Body;
use axum::http;
use axum::http::Request;
use axum::http::StatusCode;
use cerbes::applications::api::create_app;
use cerbes::domain::adapters::database::*;
use cerbes::domain::entities::Permissions;
use cerbes::domain::services::user::create_user;
use cerbes::infrastructure::database::models::credentials as CredentialsModel;
use cerbes::infrastructure::database::models::user as UserModel;
use cerbes::infrastructure::database::repository::PermissionsRepository;
use cerbes::infrastructure::database::repository::UserRepository;
use sea_orm::entity::prelude::*;
use serde::Deserialize;
use serde_json::json;
use tower::ServiceExt;

mod common;

#[derive(Debug, Deserialize)]
struct LoginResponse {
    access_token: String,
}

#[tokio::test]
async fn test_healthcheck() {
    let db = common::database::get_db().await;
    let app = create_app(db).await;
    common::database::get_db().await;

    let response = app
        .oneshot(
            Request::builder()
                .uri("/_status")
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}

#[tokio::test]
async fn test_post_user() {
    let db = common::database::get_db().await;
    let app = create_app(db).await;

    let response = app
        .oneshot(
            Request::builder()
                .uri("/users")
                .method(http::Method::POST)
                .header(
                    http::header::CONTENT_TYPE,
                    http::header::HeaderValue::from_str("application/json").unwrap(),
                )
                .body(Body::from(
                    serde_json::to_string(&json!({
                        "username": "username",
                        "password": "password",
                        "email": "email"
                    }))
                    .unwrap(),
                ))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::CREATED);
}

#[tokio::test]
async fn test_login() {
    let conn = common::database::get_db().await;

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &UserRepository::new(conn.clone()),
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(conn).await;

    let response = app
        .oneshot(
            Request::builder()
                .uri("/login")
                .method(http::Method::POST)
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str("Basic dXNlcm5hbWU6cGFzc3dvcmQ=").unwrap(),
                )
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}

#[tokio::test]
async fn test_login_user_dont_exist() {
    let conn = common::database::get_db().await;
    let app = create_app(conn).await;

    let response = app
        .oneshot(
            Request::builder()
                .uri("/login")
                .method(http::Method::POST)
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str("Basic dXNlcm5hbWU6cGFzc3dvcmQ=").unwrap(),
                )
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::FORBIDDEN);
}

#[tokio::test]
async fn test_login_wrong_password() {
    let conn = common::database::get_db().await;

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &UserRepository::new(conn.clone()),
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(conn).await;

    let response = app
        .oneshot(
            Request::builder()
                .uri("/login")
                .method(http::Method::POST)
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str("Basic dXNlcm5hbWU6dXNlcm5hbWUK").unwrap(),
                )
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::FORBIDDEN);
}

#[tokio::test]
async fn test_check_jwt_success() {
    let conn = common::database::get_db().await;

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &UserRepository::new(conn.clone()),
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(conn).await;
    let app2 = app.clone();

    let response = app
        .oneshot(
            Request::builder()
                .uri("/login")
                .method(http::Method::POST)
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str("Basic dXNlcm5hbWU6cGFzc3dvcmQ=").unwrap(),
                )
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let token = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let jwt: LoginResponse = serde_json::from_slice(&token).unwrap();

    let response = app2
        .oneshot(
            Request::builder()
                .uri("/check")
                .method(http::Method::GET)
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str(&format!("Bearer {}", jwt.access_token)).unwrap(),
                )
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}

#[tokio::test]
async fn test_refresh_jwt() {
    let conn = common::database::get_db().await;

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &UserRepository::new(conn.clone()),
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(conn).await;
    let app2 = app.clone();

    let response = app
        .oneshot(
            Request::builder()
                .uri("/login")
                .method(http::Method::POST)
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str("Basic dXNlcm5hbWU6cGFzc3dvcmQ=").unwrap(),
                )
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let token = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let jwt: LoginResponse = serde_json::from_slice(&token).unwrap();

    let response = app2
        .oneshot(
            Request::builder()
                .uri("/refresh")
                .method(http::Method::POST)
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str(&format!("Bearer {}", jwt.access_token)).unwrap(),
                )
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}

#[tokio::test]
async fn test_activate_user() {
    let conn = common::database::get_db().await;

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &UserRepository::new(conn.clone()),
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let user = UserModel::Entity::find().one(&conn).await.unwrap().unwrap();
    let app = create_app(conn.clone()).await;

    let response = app
        .oneshot(
            Request::builder()
                .uri(format!("/activate/{}", user.activation_id.unwrap()))
                .method(http::Method::POST)
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);

    let user = UserModel::Entity::find().one(&conn).await.unwrap().unwrap();
    assert!(user.activation_id.is_none());
}

#[tokio::test]
async fn test_reset_password() {
    let conn = common::database::get_db().await;

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &UserRepository::new(conn.clone()),
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(conn.clone()).await;

    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/password-reset/request")
                .method(http::Method::POST)
                .header(
                    http::header::CONTENT_TYPE,
                    http::header::HeaderValue::from_str("application/json").unwrap(),
                )
                .body(Body::from(
                    serde_json::to_string(&json!({
                        "username": "username",
                    }))
                    .unwrap(),
                ))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);

    let (user, credentials) = UserModel::Entity::find()
        .find_also_related(CredentialsModel::Entity)
        .one(&conn)
        .await
        .unwrap()
        .unwrap();

    assert!(credentials.as_ref().unwrap().password_reset_id.is_some());

    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri(format!(
                    "/password-reset/validate?user_id={}&reset_id={}",
                    user.public_id,
                    credentials.as_ref().unwrap().password_reset_id.unwrap()
                ))
                .method(http::Method::GET)
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);

    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/password-reset")
                .method(http::Method::POST)
                .header(
                    http::header::CONTENT_TYPE,
                    http::header::HeaderValue::from_str("application/json").unwrap(),
                )
                .body(Body::from(
                    serde_json::to_string(&json!({
                        "user_id": user.public_id,
                        "reset_id": credentials.unwrap().password_reset_id,
                        "password": "coucou"
                    }))
                    .unwrap(),
                ))
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}

#[tokio::test]
async fn test_get_users() {
    #[derive(Deserialize)]
    struct UserTest {
        email: String,
    }

    let conn = common::database::get_db().await;

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &UserRepository::new(conn.clone()),
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();
    create_user(
        "email2".to_owned(),
        "username2".to_owned(),
        "password2".to_owned(),
        &UserRepository::new(conn.clone()),
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(conn.clone()).await;

    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/login")
                .method(http::Method::POST)
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str("Basic dXNlcm5hbWU6cGFzc3dvcmQ=").unwrap(),
                )
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let token = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let jwt: LoginResponse = serde_json::from_slice(&token).unwrap();

    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/users")
                .header(
                    http::header::CONTENT_TYPE,
                    http::header::HeaderValue::from_str("application/json").unwrap(),
                )
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str(&format!("Bearer {}", jwt.access_token)).unwrap(),
                )
                .method(http::Method::GET)
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let response = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let users: Vec<UserTest> = serde_json::from_slice(&response).unwrap();

    assert_eq!(users.len(), 2);
    assert_eq!(users[0].email, "email");
    assert_eq!(users[1].email, "email2");
}

#[tokio::test]
async fn test_impersonate() {
    let conn = common::database::get_db().await;

    let user = create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &UserRepository::new(conn.clone()),
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let impersonated = create_user(
        "email2".to_owned(),
        "username2".to_owned(),
        "password2".to_owned(),
        &UserRepository::new(conn.clone()),
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let perm = PermissionsRepository::new(conn.clone());
    perm.add_permission_for_user(&Permissions { impersonate: true }, &user)
        .await
        .unwrap();

    let app = create_app(conn.clone()).await;

    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/login")
                .method(http::Method::POST)
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str("Basic dXNlcm5hbWU6cGFzc3dvcmQ=").unwrap(),
                )
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let token = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let jwt: LoginResponse = serde_json::from_slice(&token).unwrap();

    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri(format!("/impersonate/{}", impersonated.public_id))
                .header(
                    http::header::CONTENT_TYPE,
                    http::header::HeaderValue::from_str("application/json").unwrap(),
                )
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str(&format!("Bearer {}", jwt.access_token)).unwrap(),
                )
                .method(http::Method::POST)
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
    let token = hyper::body::to_bytes(response.into_body()).await.unwrap();
    let impersonate_jwt: LoginResponse = serde_json::from_slice(&token).unwrap();

    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/desimpersonate")
                .header(
                    http::header::CONTENT_TYPE,
                    http::header::HeaderValue::from_str("application/json").unwrap(),
                )
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str(&format!("Bearer {}", jwt.access_token)).unwrap(),
                )
                .method(http::Method::POST)
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::BAD_REQUEST);

    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri("/desimpersonate")
                .header(
                    http::header::CONTENT_TYPE,
                    http::header::HeaderValue::from_str("application/json").unwrap(),
                )
                .header(
                    http::header::AUTHORIZATION,
                    http::HeaderValue::from_str(&format!(
                        "Bearer {}",
                        impersonate_jwt.access_token
                    ))
                    .unwrap(),
                )
                .method(http::Method::POST)
                .body(Body::empty())
                .unwrap(),
        )
        .await
        .unwrap();

    assert_eq!(response.status(), StatusCode::OK);
}
