use crate::domain::adapters::database::CredentialsRepositoryTrait;
use crate::domain::entities::Credentials;
use crate::domain::errors::CerbesError;
use crate::infrastructure::database::models::credentials as CredentialsModel;
use async_trait::async_trait;
use sea_orm::entity::prelude::*;
use sea_orm::Set;

#[derive(Clone)]
pub struct CredentialsRepository {
    pub conn: DatabaseConnection,
}

impl CredentialsRepository {
    pub fn new(conn: DatabaseConnection) -> Self {
        CredentialsRepository { conn }
    }
}

#[async_trait]
impl CredentialsRepositoryTrait for CredentialsRepository {
    async fn save(&self, credentials: &Credentials) -> Result<(), CerbesError> {
        let model = CredentialsModel::ActiveModel {
            username: Set(credentials.username.clone()),
            password: Set(credentials.password.clone()),
            last_seen: Set(credentials.last_seen),
            created_at: Set(chrono::Utc::now().naive_utc()),
            updated_at: Set(chrono::Utc::now().naive_utc()),
            ..Default::default()
        };

        model.insert(&self.conn).await?;

        Ok(())
    }
}
