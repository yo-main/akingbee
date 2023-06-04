use axum::routing;
mod login;
mod users;
use crate::domain::adapters::database::PermissionRepositoryTrait;
use crate::domain::adapters::database::UserRepositoryTrait;
use tower_http::cors::CorsLayer;

#[derive(Clone)]
pub struct AppState<R, P>
where
    R: UserRepositoryTrait,
    P: PermissionRepositoryTrait,
{
    user_repo: R,
    permissions_repo: P,
}

pub async fn create_app<U, C>(user_repo: U, permissions_repo: C) -> axum::Router
where
    U: UserRepositoryTrait + Clone + Send + Sync + 'static,
    C: PermissionRepositoryTrait + Clone + Send + Sync + 'static,
{
    let state = AppState {
        user_repo,
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
            routing::post(users::activate_user_endpoint),
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
        .route("/impersonate/:user_id", routing::post(login::impersonate))
        .route("/desimpersonate", routing::post(login::desimpersonate))
        .layer(cors)
        .with_state(state)
}

async fn health_check() -> &'static str {
    "Ok"
}
