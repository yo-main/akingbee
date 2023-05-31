use crate::domain::adapters::database::CredentialsRepositoryTrait;
use crate::domain::entities::Credentials;
use crate::domain::entities::User;
use crate::domain::errors::CerbesError;
use crate::infrastructure::database::models::credentials as CredentialsModel;
use crate::infrastructure::database::models::user as UserModel;
use async_trait::async_trait;
use sea_orm::entity::prelude::*;
use sea_orm::sea_query::Expr;
use sea_orm::Set;
use sea_orm::Value;
use uuid::Uuid;

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
    async fn save(&self, user: &User, credentials: &Credentials) -> Result<(), CerbesError> {
        // TODO: try to set this value through a subquery rather than querying the user object directly
        // This will allow to remove this useless `user` parameter
        let user = UserModel::Entity::find()
            .filter(UserModel::Column::PublicId.eq(user.public_id))
            .one(&self.conn)
            .await?
            .expect("User couldn't be found");

        let model = CredentialsModel::ActiveModel {
            user_id: Set(user.id),
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

    async fn get_by_user_public_id(&self, user_public_id: Uuid) -> Result<User, CerbesError> {
        let (user, credentials) = UserModel::Entity::find()
            .filter(UserModel::Column::PublicId.eq(user_public_id))
            .find_also_related(CredentialsModel::Entity)
            .one(&self.conn)
            .await?
            .expect("User couldn't be found");

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
        return Ok(User::from_entity(user, credentials));
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
        return Ok(User::from_entity(user, credentials));
    }

    async fn reset_request(&self, creds: Credentials) -> Result<Credentials, CerbesError> {
        let result = CredentialsModel::Entity::find()
            .filter(CredentialsModel::Column::Username.eq(&creds.username))
            .one(&self.conn)
            .await?;

        if result.is_none() {
            return Err(CerbesError::user_not_found());
        }

        let mut creds: CredentialsModel::ActiveModel = result.unwrap().into();
        creds.password_reset_id = Set(Some(Uuid::new_v4()));
        let creds = creds.update(&self.conn).await?;

        return Ok(Credentials::from_entity(creds));
    }

    async fn update_password(&self, username: &str, password: &str) -> Result<(), CerbesError> {
        CredentialsModel::Entity::update_many()
            .filter(CredentialsModel::Column::Username.eq(username))
            .col_expr(CredentialsModel::Column::Password, Expr::value(password))
            .col_expr(
                CredentialsModel::Column::PasswordResetId,
                Expr::value(Value::Uuid(None)),
            )
            .exec(&self.conn)
            .await?;

        return Ok(());
    }

    async fn register_login(
        &self,
        creds: &Credentials,
        date: chrono::NaiveDateTime,
    ) -> Result<(), CerbesError> {
        CredentialsModel::Entity::update_many()
            .filter(CredentialsModel::Column::Username.eq(&creds.username))
            .col_expr(CredentialsModel::Column::LastSeen, Expr::value(date))
            .exec(&self.conn)
            .await?;

        Ok(())
    }
}
