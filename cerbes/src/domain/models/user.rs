use super::Credentials;
use serde_json::json;
use serde_json::Value;
use uuid::Uuid;

#[derive(Debug, Default)]
pub struct User {
    pub email: String,
    pub credentials: Option<Credentials>,
    pub public_id: Uuid,
    pub activation_id: Option<Uuid>,
}

impl User {
    pub fn new(email: String) -> Self {
        User {
            email,
            credentials: None,
            public_id: Uuid::new_v4(),
            activation_id: Some(Uuid::new_v4()),
        }
    }

    pub fn to_json(&self) -> Value {
        json!({
            "user": {
                "id": self.public_id,
                "email": self.email,
                "username": self.credentials.as_ref().and_then(|c| Some(&c.username))
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
        let user = User::new("email@test.com".to_owned());
        assert_eq!(user.email, "email@test.com");
        assert!(user.activation_id.is_some());
        assert!(user.credentials.is_none());
    }
}
