use crate::domain::errors::CerbesError;
use sea_orm::error::DbErr;

impl From<DbErr> for CerbesError {
    fn from(error: DbErr) -> Self {
        match error {
            DbErr::RecordNotFound(str) => CerbesError {
                msg: str,
                code: 404,
            },
            _ => CerbesError {
                msg: error.to_string(),
                code: 400,
            },
        }
    }
}
