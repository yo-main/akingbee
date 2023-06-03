use super::AppState;

use crate::domain::adapters::database::PermissionsRepositoryTrait;
use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::entities::Jwt;
use crate::domain::entities::User;
use crate::domain::services::user::activate_user;
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
use serde::Deserialize;
use serde::Serialize;
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

pub async fn post_user<R, P>(
    state: State<AppState<R, P>>,
    Json(payload): Json<InputPostUser>,
) -> Result<(StatusCode, Json<OutputUser>), (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionsRepositoryTrait,
{
    let user = match SETTINGS.env.as_str() {
        "test" => {
            create_user(
                payload.email,
                payload.username,
                payload.password,
                &state.user_repo,
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
                &RbmqClient::new().await,
            )
            .await?
        }
    };

    Ok((StatusCode::CREATED, Json(user.into())))
}

pub async fn get_users<R, P>(
    state: State<AppState<R, P>>,
    TypedHeader(auth): TypedHeader<headers::Authorization<headers::authorization::Bearer>>,
) -> Result<Json<Vec<OutputUser>>, (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionsRepositoryTrait,
{
    Jwt::validate_jwt(auth.token().to_owned())?;

    let users = state.user_repo.get_all_users().await?;
    Ok(Json(users.into_iter().map(|u| u.into()).collect()))
}

pub async fn activate_user_endpoint<R, P>(
    state: State<AppState<R, P>>,
    Path(activation_id): Path<Uuid>,
) -> Result<StatusCode, (StatusCode, String)>
where
    R: UserRepositoryTrait,
    P: PermissionsRepositoryTrait,
{
    activate_user(activation_id, &state.user_repo).await?;

    return Ok(StatusCode::OK);
}
