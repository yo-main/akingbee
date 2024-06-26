use crate::domain::entities::Permissions;
use crate::domain::entities::User;
use crate::domain::errors::CerbesError;
use async_trait::async_trait;
use uuid::Uuid;

#[async_trait]
pub trait UserRepositoryTrait {
    async fn create(&self, user: &User) -> Result<(), CerbesError>;
    async fn update(&self, user: &User) -> Result<(), CerbesError>;
    async fn get_by_public_id(&self, public_id: Uuid) -> Result<User, CerbesError>;
    async fn get_by_username(&self, username: &str) -> Result<User, CerbesError>;
    async fn get_by_user_email(&self, user_email: &str) -> Result<User, CerbesError>;
    async fn get_by_activation_id(&self, activation_id: Uuid) -> Result<User, CerbesError>;
    async fn get_all_users(&self) -> Result<Vec<User>, CerbesError>;
}

#[async_trait]
pub trait PermissionRepositoryTrait {
    async fn get_permissions_for_user(&self, user: &User) -> Result<Vec<Permissions>, CerbesError>;
    async fn add_permission_for_user(
        &self,
        permissions: &Permissions,
        user: &User,
    ) -> Result<(), CerbesError>;
}
