pub mod applications;
pub mod domain;
pub mod infrastructure;
pub mod settings;

use crate::infrastructure::database::connection::get_connection;
use crate::settings::SETTINGS;
use std::net::IpAddr;
use std::net::Ipv4Addr;
use std::net::SocketAddr;

pub async fn create_app() {
    let conn = get_connection(&SETTINGS.database.url).await.unwrap();
    let app = applications::api::create_app(conn).await;

    axum::Server::bind(&SocketAddr::new(IpAddr::V4(Ipv4Addr::new(0, 0, 0, 0)), 80))
        .serve(app.into_make_service())
        .await
        .unwrap();
}
