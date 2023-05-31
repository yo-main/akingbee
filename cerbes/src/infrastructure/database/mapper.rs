use crate::domain::entities::Credentials;
use crate::domain::entities::Permissions;
use crate::domain::entities::User;
use crate::infrastructure::database::models::credentials as CredentialsEntity;
use crate::infrastructure::database::models::permissions as PermissionsEntity;
use crate::infrastructure::database::models::user as UserEntity;

impl User {
    pub fn from_entity(
        entity: UserEntity::Model,
        credentials: Option<CredentialsEntity::Model>,
    ) -> Self {
        User {
            email: entity.email,
            public_id: entity.public_id,
            activation_id: entity.activation_id,
            credentials: credentials.and_then(|creds| Some(Credentials::from_entity(creds))),
        }
    }
}

impl Credentials {
    pub fn from_entity(entity: CredentialsEntity::Model) -> Self {
        Credentials {
            username: entity.username,
            password: entity.password,
            password_reset_id: entity.password_reset_id,
            last_seen: entity.last_seen,
        }
    }
}

impl From<PermissionsEntity::Model> for Permissions {
    fn from(item: PermissionsEntity::Model) -> Self {
        Permissions {
            impersonate: item.impersonate,
        }
    }
}
