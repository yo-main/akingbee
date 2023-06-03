use std::error::Error;
use std::fmt;

#[derive(Debug)]
pub struct CerbesError {
    pub msg: String,
    pub code: u16,
}

impl Error for CerbesError {}

impl CerbesError {
    pub fn database_error() -> Self {
        CerbesError {
            msg: String::from("Database error has been wildly encountered"),
            code: 400,
        }
    }

    pub fn credentials_could_not_be_created() -> Self {
        CerbesError {
            msg: String::from("Something went wrong when creating credentials"),
            code: 400,
        }
    }

    pub fn user_not_found() -> Self {
        CerbesError {
            msg: String::from("User not found"),
            code: 404,
        }
    }

    pub fn invalid_jwt() -> Self {
        CerbesError {
            msg: String::from("Invalid jwt"),
            code: 401,
        }
    }

    pub fn not_enough_permissions() -> Self {
        CerbesError {
            msg: String::from("Not enough permissions"),
            code: 403,
        }
    }
}

impl fmt::Display for CerbesError {
    fn fmt(&self, f: &mut fmt::Formatter) -> fmt::Result {
        write!(f, "{} - {}", self.code, self.msg)
    }
}
