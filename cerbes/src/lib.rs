pub mod applications;
pub mod domain;
pub mod infrastructure;
pub mod settings;

use infrastructure::database::repository::PermissionRepositoryPg;
use infrastructure::database::repository::UserRepositoryPg;

use crate::infrastructure::database::connection::get_connection;
use crate::infrastructure::zeromq::client::ZMQClient;
use crate::settings::SETTINGS;
use std::net::IpAddr;
use std::net::Ipv4Addr;
use std::net::SocketAddr;

pub async fn create_app() {
    let conn = get_connection(&SETTINGS.database.url).await.unwrap();

    let user_repo = UserRepositoryPg::new(conn.clone());
    let permissions_repo = PermissionRepositoryPg::new(conn.clone());
    let publisher = ZMQClient::new();

    let app = applications::api::create_app(user_repo, permissions_repo, publisher).await;
    let port = &SETTINGS.app.port;

    axum::Server::bind(&SocketAddr::new(
        IpAddr::V4(Ipv4Addr::new(0, 0, 0, 0)),
        *port,
    ))
    .serve(app.into_make_service())
    .await
    .unwrap();
}
