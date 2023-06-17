use super::AppState;

use crate::domain::adapters::database::PermissionRepositoryTrait;
use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::adapters::publisher::PublisherTrait;
use crate::domain::entities::Jwt;
use crate::domain::entities::User;
use crate::domain::services::user::activate_user;
use crate::domain::services::user::create_user;
use axum::extract::Json;
use axum::extract::Path;
use axum::extract::State;
use axum::extract::TypedHeader;
use axum::headers;
use axum::http::StatusCode;
use chrono::NaiveDateTime;
use serde::Deserialize;
use serde::Serialize;
use tracing::info;
use uuid::Uuid;

#[derive(Deserialize)]
pub struct InputPostUser {
    username: String,
    password: String,
    email: String,
}

#[derive(Serialize)]
pub struct OutputUser {
    email: String,
    public_id: Uuid,
    activation_id: Option<Uuid>,
    username: String,
    last_seen: Option<NaiveDateTime>,
}

impl Into<OutputUser> for User {
    fn into(self) -> OutputUser {
        OutputUser {
            email: self.email,
            public_id: self.public_id,
            activation_id: self.activation_id,
            username: self.credentials.username,
            last_seen: self.credentials.last_seen,
        }
    }
}

pub async fn post_user<R, P, C>(
    state: State<AppState<R, P, C>>,
    Json(payload): Json<InputPostUser>,
) -> Result<(StatusCode, Json<OutputUser>), (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionRepositoryTrait,
    C: PublisherTrait,
{
    let user = create_user(
        payload.email,
        payload.username,
        payload.password,
        &state.user_repo,
        &state.publisher,
    )
    .await?;

    info!("Create new user {}", user.credentials.username);
    Ok((StatusCode::CREATED, Json(user.into())))
}

pub async fn get_users<R, P, C>(
    state: State<AppState<R, P, C>>,
    TypedHeader(auth): TypedHeader<headers::Authorization<headers::authorization::Bearer>>,
) -> Result<Json<Vec<OutputUser>>, (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionRepositoryTrait,
    C: PublisherTrait,
{
    Jwt::validate_jwt(auth.token().to_owned())?;

    let users = state.user_repo.get_all_users().await?;
    Ok(Json(users.into_iter().map(|u| u.into()).collect()))
}

pub async fn activate_user_endpoint<R, P, C>(
    state: State<AppState<R, P, C>>,
    Path(activation_id): Path<Uuid>,
) -> Result<StatusCode, (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionRepositoryTrait,
    C: PublisherTrait,
{
    activate_user(activation_id, &state.user_repo).await?;

    return Ok(StatusCode::OK);
}
