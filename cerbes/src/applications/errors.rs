use crate::domain::errors::CerbesError;
use axum::http::StatusCode;
use tracing::error;

impl From<CerbesError> for StatusCode {
    fn from(item: CerbesError) -> Self {
        error!("Error happened: {}", item);
        match item.code {
            400 => StatusCode::BAD_REQUEST,
            401 => StatusCode::UNAUTHORIZED,
            403 => StatusCode::FORBIDDEN,
            404 => StatusCode::NOT_FOUND,
            _ => StatusCode::INTERNAL_SERVER_ERROR,
        }
    }
}

impl From<CerbesError> for (StatusCode, String) {
    fn from(item: CerbesError) -> Self {
        match item.code {
            400 => (StatusCode::BAD_REQUEST, item.msg),
            401 => (StatusCode::UNAUTHORIZED, item.msg),
            403 => (StatusCode::FORBIDDEN, item.msg),
            404 => (StatusCode::NOT_FOUND, item.msg),
            _ => (StatusCode::INTERNAL_SERVER_ERROR, item.msg),
        }
    }
}
