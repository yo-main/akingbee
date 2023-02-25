use cerbes::settings::SETTINGS;
use migration::Migrator;
use migration::MigratorTrait;
use sea_orm::ConnectOptions;
use sea_orm::Database;
use sea_orm::DatabaseConnection;
use std::time::Duration;

async fn provision_db(conn: &DatabaseConnection) {
    Migrator::up(conn, None)
        .await
        .expect("Couldn't executed migrations");
}

pub async fn get_db() -> DatabaseConnection {
    let mut options = ConnectOptions::new(SETTINGS.database.url.clone());
    options.max_lifetime(Duration::from_secs(60 * 10));
    options.max_connections(2);

    let conn: DatabaseConnection = Database::connect(options).await.unwrap();
    provision_db(&conn).await;

    return conn;
}
