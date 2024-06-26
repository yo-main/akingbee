use std::cell::RefCell;

use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::entities::User;
use crate::domain::errors::CerbesError;
use crate::infrastructure::database::models::credentials as CredentialsModel;
use crate::infrastructure::database::models::user as UserModel;
use async_trait::async_trait;
use sea_orm::entity::prelude::*;
use sea_orm::sea_query::Query;
use sea_orm::TransactionTrait;
use std::sync::Arc;
use std::sync::Mutex;
use uuid::Uuid;

#[derive(Clone)]
pub struct UserRepositoryMem {
    storage: Arc<Mutex<Vec<User>>>,
}

impl UserRepositoryMem {
    pub fn new() -> Self {
        UserRepositoryMem {
            storage: Arc::new(Mutex::new(Vec::new())),
        }
    }
}

#[async_trait]
impl UserRepositoryTrait for UserRepositoryMem {
    async fn create(&self, user: &User) -> Result<(), CerbesError> {
        let mut storage = self.storage.lock().unwrap();

        if storage
            .iter()
            .find(|u| u.public_id == user.public_id)
            .is_some()
        {
            return Ok(());
        } else {
            storage.push(user.clone());
        }

        Ok(())
    }

    async fn update(&self, user: &User) -> Result<(), CerbesError> {
        let mut storage = self.storage.lock().unwrap();
        if let Some(existing_user) = storage.iter_mut().find(|u| u.public_id == user.public_id) {
            existing_user.email = user.email.clone();
            existing_user.credentials = user.credentials.clone();
            existing_user.activation_id = user.activation_id;
        } else {
            return Err(CerbesError::user_not_found());
        }

        Ok(())
    }

    async fn get_by_public_id(&self, public_id: Uuid) -> Result<User, CerbesError> {
        let storage = self.storage.lock().unwrap();
        if let Some(user) = storage.iter().find(|u| u.public_id == public_id) {
            return Ok(user.clone());
        } else {
            return Err(CerbesError::user_not_found());
        }
    }
    async fn get_by_username(&self, username: &str) -> Result<User, CerbesError> {
        let storage = self.storage.lock().unwrap();
        if let Some(user) = storage.iter().find(|u| u.credentials.username == username) {
            return Ok(user.clone());
        } else {
            return Err(CerbesError::user_not_found());
        }
    }
    async fn get_by_user_email(&self, user_email: &str) -> Result<User, CerbesError> {
        let storage = self.storage.lock().unwrap();
        if let Some(user) = storage.iter().find(|u| u.email == user_email) {
            return Ok(user.clone());
        } else {
            return Err(CerbesError::user_not_found());
        }
    }
    async fn get_by_activation_id(&self, activation_id: Uuid) -> Result<User, CerbesError> {
        let storage = self.storage.lock().unwrap();
        if let Some(user) = storage
            .iter()
            .find(|u| u.activation_id == Some(activation_id))
        {
            return Ok(user.clone());
        } else {
            return Err(CerbesError::user_not_found());
        }
    }
    async fn get_all_users(&self) -> Result<Vec<User>, CerbesError> {
        let storage = self.storage.lock().unwrap();
        Ok(storage.clone())
    }
}

#[derive(Clone)]
pub struct UserRepositoryPg {
    pub conn: DatabaseConnection,
}

impl UserRepositoryPg {
    pub fn new(conn: DatabaseConnection) -> Self {
        UserRepositoryPg { conn }
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
impl UserRepositoryTrait for UserRepositoryPg {
    async fn create(&self, user: &User) -> Result<(), CerbesError> {
        let builder = self.conn.get_database_backend();

        let transaction = self.conn.begin().await?;

        let mut query = Query::insert();
        query
            .into_table(CredentialsModel::Entity)
            .returning_col(CredentialsModel::Column::Id)
            .columns(vec![
                CredentialsModel::Column::Username,
                CredentialsModel::Column::Password,
                CredentialsModel::Column::LastSeen,
                CredentialsModel::Column::CreatedAt,
                CredentialsModel::Column::UpdatedAt,
            ])
            .values(vec![
                user.credentials.username.as_str().into(),
                user.credentials.password.as_str().into(),
                user.credentials.last_seen.into(),
                chrono::Utc::now().naive_utc().into(),
                chrono::Utc::now().naive_utc().into(),
            ])
            .unwrap();

        let cred_id: i32 = match self.conn.query_one(builder.build(&query)).await? {
            Some(result) => result.try_get_by(0).map_err(|err| err.into()),
            _ => Err(CerbesError::credentials_could_not_be_created()),
        }?;

        let mut query = Query::insert();
        query
            .into_table(UserModel::Entity)
            .columns(vec![
                UserModel::Column::Email,
                UserModel::Column::PublicId,
                UserModel::Column::ActivationId,
                UserModel::Column::CredentialsId,
                UserModel::Column::CreatedAt,
                UserModel::Column::UpdatedAt,
            ])
            .values(vec![
                user.email.as_str().into(),
                user.public_id.into(),
                user.activation_id.into(),
                cred_id.into(),
                chrono::Utc::now().naive_utc().into(),
                chrono::Utc::now().naive_utc().into(),
            ])
            .unwrap();

        let builder = self.conn.get_database_backend();
        self.conn.execute(builder.build(&query)).await?;

        transaction.commit().await?;

        Ok(())
    }

    async fn update(&self, user: &User) -> Result<(), CerbesError> {
        let mut user_query = Query::update();
        let mut creds_query = Query::update();
        user_query
            .table(UserModel::Entity)
            .values(vec![
                (UserModel::Column::Email, user.email.as_str().into()),
                (UserModel::Column::ActivationId, user.activation_id.into()),
                (
                    UserModel::Column::UpdatedAt,
                    chrono::Utc::now().naive_utc().into(),
                ),
            ])
            .and_where(UserModel::Column::PublicId.eq(user.public_id));

        creds_query
            .table(CredentialsModel::Entity)
            .values(vec![
                (
                    CredentialsModel::Column::PasswordResetId,
                    user.credentials.password_reset_id.into(),
                ),
                (
                    CredentialsModel::Column::Password,
                    user.credentials.password.as_str().into(),
                ),
                (
                    CredentialsModel::Column::LastSeen,
                    user.credentials.last_seen.into(),
                ),
                (
                    CredentialsModel::Column::UpdatedAt,
                    chrono::Utc::now().naive_utc().into(),
                ),
            ])
            .and_where(CredentialsModel::Column::Username.eq(&user.credentials.username));

        let builder = self.conn.get_database_backend();
        self.conn.execute(builder.build(&user_query)).await?;
        self.conn.execute(builder.build(&creds_query)).await?;

        Ok(())
    }

    async fn get_by_public_id(&self, public_id: Uuid) -> Result<User, CerbesError> {
        let (user, credentials) = self.get_raw_model_by_public_id(public_id).await?;
        let user = User::from_entity(user, credentials);

        return Ok(user);
    }

    async fn get_by_username(&self, username: &str) -> Result<User, CerbesError> {
        let result = UserModel::Entity::find()
            .find_also_related(CredentialsModel::Entity)
            .filter(CredentialsModel::Column::Username.eq(username))
            .one(&self.conn)
            .await?;

        if result.is_none() {
            return Err(CerbesError::user_not_found());
        }

        let (user, credentials) = result.unwrap();
        return Ok(User::from_entity(user, credentials.unwrap()));
    }

    async fn get_by_user_email(&self, user_email: &str) -> Result<User, CerbesError> {
        let result = UserModel::Entity::find()
            .filter(UserModel::Column::Email.eq(user_email))
            .find_also_related(CredentialsModel::Entity)
            .one(&self.conn)
            .await?;

        if result.is_none() {
            return Err(CerbesError::user_not_found());
        }

        let (user, credentials) = result.unwrap();
        return Ok(User::from_entity(user, credentials.unwrap()));
    }

    async fn get_by_activation_id(&self, activation_id: Uuid) -> Result<User, CerbesError> {
        let result = UserModel::Entity::find()
            .filter(UserModel::Column::ActivationId.eq(activation_id))
            .find_also_related(CredentialsModel::Entity)
            .one(&self.conn)
            .await?;

        if result.is_none() {
            return Err(CerbesError::user_not_found());
        }

        let (user, credentials) = result.unwrap();
        return Ok(User::from_entity(user, credentials.unwrap()));
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
