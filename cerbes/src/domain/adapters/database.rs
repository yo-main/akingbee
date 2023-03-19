use crate::domain::errors::CerbesError;
use crate::domain::models::Credentials;
use crate::domain::models::Permissions;
use crate::domain::models::User;
use async_trait::async_trait;
use uuid::Uuid;

#[async_trait]
pub trait UserRepositoryTrait {
    async fn create_user(&self, user: &User) -> Result<(), CerbesError>;
    async fn get_by_public_id(&self, public_id: Uuid) -> Result<User, CerbesError>;
    async fn activate_user(&self, activation_id: Uuid) -> Result<User, CerbesError>;
    async fn get_all_users(&self) -> Result<Vec<User>, CerbesError>;
}

#[async_trait]
pub trait CredentialsRepositoryTrait {
    async fn create_credentials(
        &self,
        user: &User,
        credentials: &Credentials,
    ) -> Result<(), CerbesError>;

    async fn get_by_user_public_id(&self, user_public_id: Uuid) -> Result<User, CerbesError>;
    async fn get_by_username(&self, username: &str) -> Result<User, CerbesError>;
    async fn get_by_user_email(&self, user_email: &str) -> Result<User, CerbesError>;
    async fn reset_request(&self, creds: Credentials) -> Result<Credentials, CerbesError>;
    async fn register_login(
        &self,
        creds: &Credentials,
        date: chrono::NaiveDateTime,
    ) -> Result<(), CerbesError>;

    async fn update_password(&self, username: &str, password: &str) -> Result<(), CerbesError>;
}

#[async_trait]
pub trait PermissionsRepositoryTrait {
    async fn get_permissions_for_user(&self, user: &User) -> Result<Vec<Permissions>, CerbesError>;
    async fn add_permission_for_user(
        &self,
        permissions: &Permissions,
        user: &User,
    ) -> Result<(), CerbesError>;
}
