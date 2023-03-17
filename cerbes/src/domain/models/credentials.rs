use chrono::NaiveDateTime;
use uuid::Uuid;

#[derive(Debug, Default)]
pub struct Credentials {
    pub username: String,
    pub password: String,
    pub last_seen: Option<NaiveDateTime>,
    pub password_reset_id: Option<Uuid>,
}

impl Credentials {
    pub fn new(username: String, password: String) -> Self {
        Credentials {
            username,
            password,
            password_reset_id: None,
            last_seen: None,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_credentials() {
        let credentials = Credentials::new("username".to_owned(), "password".to_owned());
        assert_eq!(credentials.username, "username");
        assert_eq!(credentials.password, "password");
        assert!(credentials.password_reset_id.is_none());
        assert!(credentials.last_seen.is_none());
    }
}
