use crate::domain::errors::CerbesError;
use axum::http::StatusCode;

impl From<CerbesError> for StatusCode {
    fn from(item: CerbesError) -> Self {
        match item.code {
            400 => StatusCode::BAD_REQUEST,
            401 => StatusCode::UNAUTHORIZED,
            403 => StatusCode::FORBIDDEN,
            404 => StatusCode::NOT_FOUND,
            _ => StatusCode::INTERNAL_SERVER_ERROR,
        }
    }
}
