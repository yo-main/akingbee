use super::AppState;
use crate::domain::adapters::database::PermissionRepositoryTrait;
use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::entities::Jwt;
use crate::domain::errors::CerbesError;
use crate::domain::services::user::impersonate_user;
use crate::domain::services::user::password_reset;
use crate::domain::services::user::password_reset_validate;
use crate::domain::services::user::register_password_reset_request;
use crate::domain::services::user::user_login;
use crate::infrastructure::rabbitmq::client::RbmqClient;
use crate::infrastructure::rabbitmq::client::TestRbmqClient;
use crate::settings::SETTINGS;

use axum::extract::Json;
use axum::extract::Path;
use axum::extract::Query;
use axum::extract::State;
use axum::extract::TypedHeader;
use axum::headers;
use axum::http::StatusCode;
use serde::Deserialize;
use serde::Serialize;
use tracing::info;
use uuid::Uuid;

#[derive(Serialize)]
pub struct LoginOutput {
    pub access_token: String,
}

#[derive(Serialize)]
pub struct CheckOutput {
    pub user_id: Uuid,
}

#[derive(Deserialize, Serialize)]
pub struct PasswordResetRequestInput {
    username: String,
}

#[derive(Deserialize)]
pub struct PasswordResetInput {
    user_id: Uuid,
    reset_id: Uuid,
    password: String,
}

#[derive(Deserialize)]
pub struct PasswordResetValidation {
    user_id: Uuid,
    reset_id: Uuid,
}

pub async fn login<R, P>(
    state: State<AppState<R, P>>,
    TypedHeader(auth): TypedHeader<headers::Authorization<headers::authorization::Basic>>,
) -> Result<(StatusCode, Json<LoginOutput>), (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionRepositoryTrait,
{
    let username = auth.username().to_owned();
    let password = auth.password().to_owned();

    info!("Login request from {}", username);

    let token = user_login(username, password, &state.user_repo)
        .await
        .map_err(|_| CerbesError::not_enough_permissions())?;

    return Ok((
        StatusCode::OK,
        Json(LoginOutput {
            access_token: token,
        }),
    ));
}

pub async fn check_jwt(
    TypedHeader(auth): TypedHeader<headers::Authorization<headers::authorization::Bearer>>,
) -> Result<(StatusCode, Json<CheckOutput>), (StatusCode, String)> {
    let token = Jwt::validate_jwt(auth.token().to_owned())?;
    return Ok((StatusCode::OK, Json(CheckOutput { user_id: token.sub })));
}

pub async fn refresh_jwt(
    TypedHeader(auth): TypedHeader<headers::Authorization<headers::authorization::Bearer>>,
) -> Result<(StatusCode, Json<LoginOutput>), (StatusCode, String)> {
    let jwt = Jwt::validate_jwt(auth.token().to_owned())
        .map_err(|_| (StatusCode::FORBIDDEN, "Forbidden".to_owned()))?;

    Ok((
        StatusCode::OK,
        Json(LoginOutput {
            access_token: jwt.refresh().get_token(),
        }),
    ))
}

pub async fn reset_password_request<R, P>(
    state: State<AppState<R, P>>,
    Json(payload): Json<PasswordResetRequestInput>,
) -> Result<StatusCode, (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionRepositoryTrait,
{
    info!("Password reset request from {}", payload.username);
    match SETTINGS.env.as_str() {
        "test" => {
            register_password_reset_request(
                &payload.username,
                &state.user_repo,
                &TestRbmqClient::new(),
            )
            .await?
        }
        _ => {
            register_password_reset_request(
                &payload.username,
                &state.user_repo,
                &RbmqClient::new().await,
            )
            .await?
        }
    };

    Ok(StatusCode::OK)
}

pub async fn reset_password_validate<R, P>(
    state: State<AppState<R, P>>,
    query: Query<PasswordResetValidation>,
) -> StatusCode
where
    R: UserRepositoryTrait,
    P: PermissionRepositoryTrait,
{
    match password_reset_validate(query.user_id, query.reset_id, &state.user_repo).await {
        true => StatusCode::OK,
        false => StatusCode::NOT_FOUND,
    }
}

pub async fn reset_password<R, P>(
    state: State<AppState<R, P>>,
    Json(payload): Json<PasswordResetInput>,
) -> Result<StatusCode, (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionRepositoryTrait,
{
    password_reset(
        payload.user_id,
        payload.reset_id,
        payload.password,
        &state.user_repo,
    )
    .await?;

    info!(
        "Successfuly reseted password from user {}, reset id {}",
        payload.user_id, payload.reset_id
    );

    Ok(StatusCode::OK)
}

pub async fn impersonate<R, P>(
    state: State<AppState<R, P>>,
    Path(user_id): Path<Uuid>,
    TypedHeader(auth): TypedHeader<headers::Authorization<headers::authorization::Bearer>>,
) -> Result<(StatusCode, Json<LoginOutput>), (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionRepositoryTrait,
{
    let token = Jwt::validate_jwt(auth.token().to_owned()).unwrap();
    info!(
        "Request to impersonate user {} from user {}",
        user_id, token.sub
    );

    let jwt = impersonate_user(
        user_id,
        token.sub,
        &state.user_repo,
        &state.permissions_repo,
    )
    .await?;

    return Ok((StatusCode::OK, Json(LoginOutput { access_token: jwt })));
}

pub async fn desimpersonate<R, P>(
    state: State<AppState<R, P>>,
    TypedHeader(auth): TypedHeader<headers::Authorization<headers::authorization::Bearer>>,
) -> Result<(StatusCode, Json<LoginOutput>), (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionRepositoryTrait,
{
    let token = Jwt::validate_jwt(auth.token().to_owned()).unwrap();

    if token.impersonator.is_none() {
        return Err((StatusCode::BAD_REQUEST, "Not impersonator token".to_owned()));
    }
    let user = state
        .user_repo
        .get_by_public_id(token.impersonator.unwrap())
        .await?;

    let jwt = user.generate_jwt();

    return Ok((StatusCode::OK, Json(LoginOutput { access_token: jwt })));
}
