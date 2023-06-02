use super::AppState;

use crate::domain::adapters::database::CredentialsRepositoryTrait;
use crate::domain::adapters::database::PermissionsRepositoryTrait;
use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::entities::Jwt;
use crate::domain::entities::User;
use crate::domain::services::user::create_user;
use crate::infrastructure::rabbitmq::client::RbmqClient;
use crate::infrastructure::rabbitmq::client::TestRbmqClient;
use crate::settings::SETTINGS;
use axum::extract::Json;
use axum::extract::Path;
use axum::extract::State;
use axum::extract::TypedHeader;
use axum::headers;
use axum::http::StatusCode;
use chrono::NaiveDateTime;
use uuid::Uuid;
// use axum::response::IntoResponse;
use serde::Deserialize;
use serde::Serialize;

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

pub async fn post_user<R, D, P>(
    state: State<AppState<R, D, P>>,
    Json(payload): Json<InputPostUser>,
) -> Result<(StatusCode, Json<OutputUser>), StatusCode>
where
    R: UserRepositoryTrait,
    D: CredentialsRepositoryTrait,
    P: PermissionsRepositoryTrait,
{
    let user = match SETTINGS.env.as_str() {
        "test" => {
            create_user(
                payload.email,
                payload.username,
                payload.password,
                &state.user_repo,
                &state.credentials_repo,
                &TestRbmqClient::new(),
            )
            .await?
        }
        _ => {
            create_user(
                payload.email,
                payload.username,
                payload.password,
                &state.user_repo,
                &state.credentials_repo,
                &RbmqClient::new().await,
            )
            .await?
        }
    };

    Ok((StatusCode::CREATED, Json(user.into())))
}

pub async fn get_users<R, D, P>(
    state: State<AppState<R, D, P>>,
    TypedHeader(auth): TypedHeader<headers::Authorization<headers::authorization::Bearer>>,
) -> Result<Json<Vec<OutputUser>>, StatusCode>
where
    R: UserRepositoryTrait,
    D: CredentialsRepositoryTrait,
    P: PermissionsRepositoryTrait,
{
    Jwt::validate_jwt(auth.token().to_owned())?;

    let users = state.user_repo.get_all_users().await?;
    Ok(Json(users.into_iter().map(|u| u.into()).collect()))
}

pub async fn activate_user<R, D, P>(
    state: State<AppState<R, D, P>>,
    Path(activation_id): Path<Uuid>,
) -> StatusCode
where
    R: UserRepositoryTrait,
    D: CredentialsRepositoryTrait,
    P: PermissionsRepositoryTrait,
{
    let user = state.user_repo.activate_user(activation_id).await;
    if user.is_err() {
        return StatusCode::BAD_REQUEST;
    }

    return StatusCode::OK;
}
