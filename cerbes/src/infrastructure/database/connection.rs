use sea_orm::error::DbErr;
use sea_orm::ConnectOptions;
use sea_orm::Database;
use sea_orm::DatabaseConnection;
use std::time::Duration;

pub async fn get_connection(url: &str) -> Result<DatabaseConnection, DbErr> {
    let mut options = ConnectOptions::new(url.to_owned());
    options.max_lifetime(Duration::from_secs(60 * 10));

    let db: DatabaseConnection = Database::connect(options).await?;

    return Ok(db);
}
