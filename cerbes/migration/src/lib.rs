pub use sea_orm_migration::prelude::*;

mod m20230215_000001_create_user_table;
mod m20230215_000002_create_credentials_table;
mod m20230215_000003_create_permissions_table;

pub struct Migrator;

#[async_trait::async_trait]
impl MigratorTrait for Migrator {
    fn migrations() -> Vec<Box<dyn MigrationTrait>> {
        vec![
            Box::new(m20230215_000001_create_user_table::Migration),
            Box::new(m20230215_000002_create_credentials_table::Migration),
            Box::new(m20230215_000003_create_permissions_table::Migration),
        ]
    }
}
