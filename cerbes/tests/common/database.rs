use cerbes::infrastructure::database::models::credentials as CredentialModel;
use cerbes::infrastructure::database::models::permissions as PermissionsModel;
use cerbes::infrastructure::database::models::user as UserModel;
use cerbes::settings::SETTINGS;
use migration::ConnectionTrait;
use sea_orm::schema::Schema;
use sea_orm::ConnectOptions;
use sea_orm::Database;
use sea_orm::DatabaseBackend;
use sea_orm::DatabaseConnection;
use std::time::Duration;

async fn provision_db(conn: &DatabaseConnection) {
    let schema = Schema::new(sea_orm::DatabaseBackend::Sqlite);
    let user_table = schema.create_table_from_entity(UserModel::Entity);
    let credentials_table = schema.create_table_from_entity(CredentialModel::Entity);
    let permissions_table = schema.create_table_from_entity(PermissionsModel::Entity);

    conn.execute(DatabaseBackend::Sqlite.build(&credentials_table))
        .await
        .unwrap();
    conn.execute(DatabaseBackend::Sqlite.build(&user_table))
        .await
        .unwrap();
    conn.execute(DatabaseBackend::Sqlite.build(&permissions_table))
        .await
        .unwrap();
}

pub async fn get_db() -> DatabaseConnection {
    let mut options = ConnectOptions::new(SETTINGS.database.url.clone());
    options.max_lifetime(Duration::from_secs(60 * 10));
    options.max_connections(2);

    let conn: DatabaseConnection = Database::connect(options).await.unwrap();
    provision_db(&conn).await;

    return conn;
}
