use crate::domain::models::Credentials;
use crate::domain::models::Permissions;
use crate::domain::models::User;
use crate::infrastructure::database::entities::credentials as CredentialsEntity;
use crate::infrastructure::database::entities::permissions as PermissionsEntity;
use crate::infrastructure::database::entities::user as UserEntity;

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
