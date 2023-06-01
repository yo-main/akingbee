use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::entities::User;
use crate::domain::errors::CerbesError;
use crate::infrastructure::database::models::credentials as CredentialsModel;
use crate::infrastructure::database::models::user as UserModel;
use async_trait::async_trait;
use sea_orm::entity::prelude::*;
use sea_orm::Set;
use uuid::Uuid;

#[derive(Clone)]
pub struct UserRepository {
    pub conn: DatabaseConnection,
}

impl UserRepository {
    pub fn new(conn: DatabaseConnection) -> Self {
        UserRepository { conn }
    }

    async fn get_raw_model_by_public_id(
        &self,
        public_id: Uuid,
    ) -> Result<(UserModel::Model, CredentialsModel::Model), CerbesError> {
        UserModel::Entity::find()
            .filter(UserModel::Column::PublicId.eq(public_id))
            .find_also_related(CredentialsModel::Entity)
            .one(&self.conn)
            .await?
            .map(|result| {
                (
                    result.0,
                    result.1.expect("No credentials found for the user"),
                )
            })
            .map_or(Err(CerbesError::user_not_found()), |(user, creds)| {
                Ok((user, creds))
            })
    }
}

#[async_trait]
impl UserRepositoryTrait for UserRepository {
    async fn save(&self, user: &User) -> Result<(), CerbesError> {
        UserModel::ActiveModel {
            email: Set(user.email.clone()),
            public_id: Set(user.public_id),
            activation_id: Set(user.activation_id),
            created_at: Set(chrono::Utc::now().naive_utc()),
            updated_at: Set(chrono::Utc::now().naive_utc()),
            ..Default::default()
        }
        .insert(&self.conn)
        .await?;

        Ok(())
    }

    async fn get_by_public_id(&self, public_id: Uuid) -> Result<User, CerbesError> {
        let (user, credentials) = self.get_raw_model_by_public_id(public_id).await?;
        let user = User::from_entity(user, credentials);

        return Ok(user);
    }

    async fn activate_user(&self, activation_id: Uuid) -> Result<User, CerbesError> {
        let result = UserModel::Entity::find()
            .filter(UserModel::Column::ActivationId.eq(activation_id))
            .find_also_related((CredentialsModel::Entity))
            .one(&self.conn)
            .await?;

        if result.is_none() {
            return Err(CerbesError::user_not_found());
        }

        let (mut user, credentials): (UserModel::ActiveModel, CredentialsModel::Model) = result
            .map(|result| {
                (
                    result.0.into(),
                    result.1.expect("No credentials found for the user"),
                )
            })
            .unwrap();
        user.activation_id = Set(None);

        let user = user.update(&self.conn).await?;

        return Ok(User::from_entity(user, credentials));
    }

    async fn get_all_users(&self) -> Result<Vec<User>, CerbesError> {
        let result = UserModel::Entity::find()
            .find_also_related(CredentialsModel::Entity)
            .all(&self.conn)
            .await?;

        return Ok(result
            .into_iter()
            .map(|(u, c)| User::from_entity(u, c.unwrap()))
            .collect());
    }
}
