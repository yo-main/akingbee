use axum::body::Body;
use axum::http;
use axum::http::Request;
use axum::http::StatusCode;
use cerbes::applications::api::create_app;
use cerbes::domain::adapters::database::*;
use cerbes::domain::entities::Permissions;
use cerbes::domain::services::user::create_user;
use cerbes::infrastructure::database::repository::PermissionRepositoryMem;
use cerbes::infrastructure::database::repository::UserRepositoryMem;
use cerbes::infrastructure::rabbitmq::client::TestPublisherClient;
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
    let app = create_app(
        UserRepositoryMem::new(),
        PermissionRepositoryMem::new(),
        TestPublisherClient::new(),
    )
    .await;

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
    let app = create_app(
        UserRepositoryMem::new(),
        PermissionRepositoryMem::new(),
        TestPublisherClient::new(),
    )
    .await;

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
    let user_repo = UserRepositoryMem::new();

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &user_repo,
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(
        user_repo,
        PermissionRepositoryMem::new(),
        TestPublisherClient::new(),
    )
    .await;

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
    let app = create_app(
        UserRepositoryMem::new(),
        PermissionRepositoryMem::new(),
        TestPublisherClient::new(),
    )
    .await;

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
    let user_repo = UserRepositoryMem::new();
    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &user_repo,
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(
        user_repo,
        PermissionRepositoryMem::new(),
        TestPublisherClient::new(),
    )
    .await;

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
    let user_repo = UserRepositoryMem::new();
    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &user_repo,
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(
        user_repo,
        PermissionRepositoryMem::new(),
        TestPublisherClient::new(),
    )
    .await;
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
    let user_repo = UserRepositoryMem::new();

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &user_repo,
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(
        user_repo,
        PermissionRepositoryMem::new(),
        TestPublisherClient::new(),
    )
    .await;
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
    let user_repo = UserRepositoryMem::new();

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &user_repo,
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let user = user_repo
        .get_all_users()
        .await
        .unwrap()
        .into_iter()
        .next()
        .unwrap();
    let app = create_app(
        user_repo.clone(),
        PermissionRepositoryMem::new(),
        TestPublisherClient::new(),
    )
    .await;

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

    let user = user_repo
        .get_all_users()
        .await
        .unwrap()
        .into_iter()
        .next()
        .unwrap();
    assert!(user.activation_id.is_none());
}

#[tokio::test]
async fn test_reset_password() {
    let user_repo = UserRepositoryMem::new();

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &user_repo,
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(
        user_repo.clone(),
        PermissionRepositoryMem::new(),
        TestPublisherClient::new(),
    )
    .await;

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

    let user = user_repo
        .get_all_users()
        .await
        .unwrap()
        .into_iter()
        .next()
        .unwrap();

    assert!(user.credentials.password_reset_id.is_some());

    let response = app
        .clone()
        .oneshot(
            Request::builder()
                .uri(format!(
                    "/password-reset/validate?user_id={}&reset_id={}",
                    user.public_id,
                    user.credentials.password_reset_id.unwrap()
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
                        "reset_id": user.credentials.password_reset_id,
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

    let user_repo = UserRepositoryMem::new();

    create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &user_repo,
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();
    create_user(
        "email2".to_owned(),
        "username2".to_owned(),
        "password2".to_owned(),
        &user_repo,
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let app = create_app(
        user_repo,
        PermissionRepositoryMem::new(),
        TestPublisherClient::new(),
    )
    .await;

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
    let user_repo = UserRepositoryMem::new();
    let perm_repo = PermissionRepositoryMem::new();

    let user = create_user(
        "email".to_owned(),
        "username".to_owned(),
        "password".to_owned(),
        &user_repo,
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    let impersonated = create_user(
        "email2".to_owned(),
        "username2".to_owned(),
        "password2".to_owned(),
        &user_repo,
        &common::publisher::TestPublisher::new(),
    )
    .await
    .unwrap();

    perm_repo
        .add_permission_for_user(&Permissions { impersonate: true }, &user)
        .await
        .unwrap();

    let app = create_app(user_repo, perm_repo, TestPublisherClient::new()).await;

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
