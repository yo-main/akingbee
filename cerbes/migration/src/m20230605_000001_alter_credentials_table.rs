use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Credentials::Table)
                    .drop_column(Credentials::UserId)
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Credentials::Table)
                    .add_column(
                        ColumnDef::new(Credentials::UserId)
                            .integer()
                            .unique_key()
                            .not_null(),
                    )
                    .add_foreign_key(
                        TableForeignKey::new()
                            .from_tbl(Credentials::Table)
                            .from_col(Credentials::UserId)
                            .to_tbl(Users::Table)
                            .to_col(Users::Id)
                            .on_delete(ForeignKeyAction::Cascade),
                    )
                    .to_owned(),
            )
            .await
    }
}

#[derive(Iden)]
enum Credentials {
    Table,
    UserId,
}

/// Learn more at https://docs.rs/sea-query#iden
#[derive(Iden)]
enum Users {
    Table,
    Id,
}
