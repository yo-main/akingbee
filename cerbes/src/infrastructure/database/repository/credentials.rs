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

    async fn get_by_user_public_id(&self, user_public_id: Uuid) -> Result<User, CerbesError> {
        let (user, credentials) = UserModel::Entity::find()
            .filter(UserModel::Column::PublicId.eq(user_public_id))
            .find_also_related(CredentialsModel::Entity)
            .one(&self.conn)
            .await?
            .expect("User couldn't be found");

        let user = User::from_entity(user, credentials.unwrap());
        return Ok(user);
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
