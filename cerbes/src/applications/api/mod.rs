use axum::routing;
use sea_orm::DatabaseConnection;
mod login;
mod users;
use crate::domain::adapters::database::CredentialsRepositoryTrait;
use crate::domain::adapters::database::PermissionsRepositoryTrait;
use crate::domain::adapters::database::UserRepositoryTrait;
use crate::infrastructure::database::repository::CredentialsRepository;
use crate::infrastructure::database::repository::PermissionsRepository;
use crate::infrastructure::database::repository::UserRepository;
use tower_http::cors::CorsLayer;

#[derive(Clone)]
pub struct AppState<R, D, P>
where
    R: UserRepositoryTrait,
    D: CredentialsRepositoryTrait,
    P: PermissionsRepositoryTrait,
{
    user_repo: R,
    credentials_repo: D,
    permissions_repo: P,
}

pub async fn create_app(conn: DatabaseConnection) -> axum::Router {
    let user_repo = UserRepository { conn: conn.clone() };
    let credentials_repo = CredentialsRepository { conn: conn.clone() };
    let permissions_repo = PermissionsRepository { conn: conn.clone() };

    let state = AppState {
        user_repo,
        credentials_repo,
        permissions_repo,
    };

    let cors = CorsLayer::very_permissive();

    axum::Router::new()
        .route("/_status", routing::get(health_check))
        .route("/users", routing::post(users::post_user))
        .route("/users", routing::get(users::get_users))
        .route("/login", routing::post(login::login))
        .route("/check", routing::get(login::check_jwt))
        .route("/refresh", routing::post(login::refresh_jwt))
        .route(
            "/activate/:activation_id",
            routing::post(users::activate_user),
        )
        .route(
            "/password-reset/request",
            routing::post(login::reset_password_request),
        )
        .route(
            "/password-reset/validate",
            routing::get(login::reset_password_validate),
        )
        .route("/password-reset", routing::post(login::reset_password))
        .route("/impersonate", routing::post(login::impersonate))
        .route("/desimpersonate", routing::post(login::desimpersonate))
        .layer(cors)
        .with_state(state)
}

async fn health_check() -> &'static str {
    "Ok"
}
