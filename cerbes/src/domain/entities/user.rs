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
