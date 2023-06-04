use crate::domain::errors::CerbesError;
use crate::settings::SETTINGS;
use chrono::NaiveDateTime;
use sha2::Digest;
use sha2::Sha256;
use uuid::Uuid;

#[derive(Debug, Default, Clone)]
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
            password: Credentials::get_password_hash(password),
            password_reset_id: None,
            last_seen: None,
        }
    }

    fn get_password_hash(password: String) -> String {
        let mut hasher = Sha256::new();

        hasher.update(&SETTINGS.hash_key);
        hasher.update(password);
        let hash: String = format!("{:x}", hasher.finalize()); // format as hex string
        return hash;
    }

    pub fn validate_password(&self, password: String) -> bool {
        Credentials::get_password_hash(password) == self.password
    }

    pub fn set_new_password(
        &mut self,
        new_password: String,
        password_reset_id: Uuid,
    ) -> Result<(), CerbesError> {
        if self.password_reset_id != Some(password_reset_id) {
            return Err(CerbesError::user_not_found());
        }

        self.password = Credentials::get_password_hash(new_password);
        self.password_reset_id = None;

        Ok(())
    }

    pub fn register_password_reset_request(&mut self) {
        self.password_reset_id = Some(Uuid::new_v4());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_credentials() {
        let credentials = Credentials::new("username".to_owned(), "password".to_owned());
        assert_eq!(credentials.username, "username");
        assert_eq!(
            credentials.password,
            "600c10feb7b03d284eed76d71ae61feacc9e7bd6508ecb97bfc3d7f197a4753d"
        );
        assert!(credentials.password_reset_id.is_none());
        assert!(credentials.last_seen.is_none());
    }
}
