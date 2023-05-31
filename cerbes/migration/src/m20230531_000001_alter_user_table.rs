use sea_orm_migration::prelude::*;

#[derive(DeriveMigrationName)]
pub struct Migration;

#[async_trait::async_trait]
impl MigrationTrait for Migration {
    async fn up(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Users::Table)
                    .add_column(
                        ColumnDef::new(Users::CredentialsId)
                            .integer()
                            .null()
                            .unique_key(),
                    )
                    .add_foreign_key(
                        TableForeignKey::new()
                            .from_tbl(Users::Table)
                            .from_col(Users::CredentialsId)
                            .to_tbl(Credentials::Table)
                            .to_col(Credentials::Id)
                            .on_delete(ForeignKeyAction::Cascade),
                    )
                    .to_owned(),
            )
            .await
    }

    async fn down(&self, manager: &SchemaManager) -> Result<(), DbErr> {
        manager
            .alter_table(
                Table::alter()
                    .table(Users::Table)
                    .drop_column(Users::CredentialsId)
                    .to_owned(),
            )
            .await
    }
}

#[derive(Iden)]
enum Credentials {
    Table,
    Id,
}

/// Learn more at https://docs.rs/sea-query#iden
#[derive(Iden)]
enum Users {
    Table,
    CredentialsId,
}
