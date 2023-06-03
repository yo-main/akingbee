use crate::domain::adapters::database::PermissionsRepositoryTrait;
use crate::domain::entities::Permissions;
use crate::domain::entities::User;
use crate::domain::errors::CerbesError;
use crate::infrastructure::database::models::permissions as PermissionModel;
use crate::infrastructure::database::models::user as UserModel;
use async_trait::async_trait;
use migration::JoinType;
use sea_orm::entity::prelude::*;
use sea_orm::query::QuerySelect;
use sea_orm::Set;

#[derive(Clone)]
pub struct PermissionsRepository {
    pub conn: DatabaseConnection,
}

impl PermissionsRepository {
    pub fn new(conn: DatabaseConnection) -> Self {
        PermissionsRepository { conn }
    }
}

#[async_trait]
impl PermissionsRepositoryTrait for PermissionsRepository {
    async fn get_permissions_for_user(&self, user: &User) -> Result<Vec<Permissions>, CerbesError> {
        // let public_id: Uuid = user.public_id.clone();
        let permissions = PermissionModel::Entity::find()
            .join(
                JoinType::LeftJoin,
                PermissionModel::Relation::User.def(), // .on_condition(|left, right| {
                                                       //     Expr::tbl(right, UserModel::Column::PublicId)
                                                       //         .eq(public_id)
                                                       //         .into_condition()
                                                       // Expr::col(UserModel::Column::PublicId).eq(user.public_id)
                                                       // }), // .filter(
                                                       //     PermissionModel::Column::UserId.in_subquery(
                                                       //         Query::select()
                                                       //             .expr(UserModel::Column::PublicId.eq(user.public_id))
                                                       //             .from(UserModel::Entity)
                                                       //             .to_owned(),
                                                       //     ),
                                                       // )
            )
            .filter(UserModel::Column::PublicId.eq(user.public_id))
            .all(&self.conn)
            .await?;

        return Ok(permissions
            .into_iter()
            .map(|p| Into::<Permissions>::into(p))
            .collect());
    }

    async fn add_permission_for_user(
        &self,
        permission: &Permissions,
        user: &User,
    ) -> Result<(), CerbesError> {
        let user_entity = UserModel::Entity::find()
            .filter(UserModel::Column::PublicId.eq(user.public_id))
            .one(&self.conn)
            .await?
            .unwrap();

        PermissionModel::ActiveModel {
            user_id: Set(user_entity.id),
            impersonate: Set(permission.impersonate),
            created_at: Set(chrono::Utc::now().naive_utc()),
            updated_at: Set(chrono::Utc::now().naive_utc()),
            ..Default::default()
        }
        .insert(&self.conn)
        .await?;

        Ok(())
    }
}
