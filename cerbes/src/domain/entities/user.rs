use crate::domain::errors::CerbesError;

use super::Credentials;
use serde_json::json;
use serde_json::Value;
use uuid::Uuid;

#[derive(Debug, Default)]
pub struct User {
    pub email: String,
    pub credentials: Credentials,
    pub public_id: Uuid,
    pub activation_id: Option<Uuid>,
}

impl User {
    pub fn new(email: String, credentials: Credentials) -> Self {
        User {
            email,
            credentials,
            public_id: Uuid::new_v4(),
            activation_id: Some(Uuid::new_v4()),
        }
    }

    pub fn to_json(&self) -> Value {
        json!({
            "user": {
                "id": self.public_id,
                "email": self.email,
                "username": self.credentials.username
            },
            "language": "fr"
        })
    }

    pub fn update_password(
        &mut self,
        new_password: String,
        password_reset_id: Uuid,
    ) -> Result<(), CerbesError> {
        self.credentials
            .set_new_password(new_password, password_reset_id)
    }

    pub fn validate_password(&self, password: String) -> bool {
        self.credentials.validate_password(password)
    }

    pub fn request_password_reset(&mut self) {
        self.credentials.register_password_reset_request();
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn new_user() {
        let credentials = Credentials::new("username".to_owned(), "password".to_owned());
        let user = User::new("email@test.com".to_owned(), credentials);
        assert_eq!(user.email, "email@test.com");
        assert_eq!(user.credentials.username, "username");
        assert!(user.activation_id.is_some());
    }
}
