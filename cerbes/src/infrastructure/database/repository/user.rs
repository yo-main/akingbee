use crate::domain::adapters::database::UserRepositoryTrait;
use crate::domain::entities::User;
use crate::domain::errors::CerbesError;
use crate::infrastructure::database::models::credentials as CredentialsModel;
use crate::infrastructure::database::models::user as UserModel;
use async_trait::async_trait;
use sea_orm::entity::prelude::*;
use sea_orm::sea_query::query::QueryStatementBuilder;
use sea_orm::sea_query::Expr;
use sea_orm::sea_query::Query;
use sea_orm::sea_query::SimpleExpr;
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
    async fn create(&self, user: &User) -> Result<(), CerbesError> {
        let creds_select = SimpleExpr::SubQuery(
            None,
            Box::new(
                Query::select()
                    .column(CredentialsModel::Column::Id)
                    .from(CredentialsModel::Entity)
                    .and_where(
                        Expr::col(CredentialsModel::Column::Username)
                            .eq(user.credentials.username.as_str()),
                    )
                    .to_owned()
                    .into_sub_query_statement(),
            ),
        );

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
                creds_select,
                chrono::Utc::now().naive_utc().into(),
                chrono::Utc::now().naive_utc().into(),
            ])
            .unwrap();

        let builder = self.conn.get_database_backend();
        self.conn.execute(builder.build(&query)).await?;

        Ok(())
    }

    async fn update(&self, user: &User) -> Result<(), CerbesError> {
        let mut user_query = Query::update();
        let mut creds_query = Query::update();
        user_query.table(UserModel::Entity).values(vec![
            (UserModel::Column::Email, user.email.as_str().into()),
            (UserModel::Column::ActivationId, user.activation_id.into()),
            (
                UserModel::Column::UpdatedAt,
                chrono::Utc::now().naive_utc().into(),
            ),
        ]);

        creds_query.table(CredentialsModel::Entity).values(vec![
            (
                CredentialsModel::Column::PasswordResetId,
                user.credentials.password_reset_id.into(),
            ),
            (
                CredentialsModel::Column::Password,
                user.credentials.password.as_str().into(),
            ),
            (
                CredentialsModel::Column::UpdatedAt,
                chrono::Utc::now().naive_utc().into(),
            ),
        ]);

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
