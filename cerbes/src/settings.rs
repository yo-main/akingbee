use config::Config;
use config::Environment;
use config::File;
use lazy_static::lazy_static;
use serde::Deserialize;
use std::env;

#[derive(Deserialize)]
pub struct Database {
    pub url: String,
}

#[derive(Deserialize)]
pub struct App {
    pub port: u16,
}

#[derive(Deserialize)]
pub struct RabbitMQ {
    pub host: String,
    pub port: u16,
    pub user: String,
    pub password: String,
    pub exchange: String,
    pub vhost: String,
}

#[derive(Deserialize)]
pub struct Settings {
    pub database: Database,
    pub rabbitmq: RabbitMQ,
    pub app: App,
    pub hash_key: String,
    pub jwt_key: String,
    pub env: String,
}

impl Settings {
    pub fn new() -> Self {
        let cerbes_env = env::var("CERBES_ENV").unwrap_or("test".to_owned());
        let s = Config::builder()
            .add_source(File::with_name(&format!("config/{}.toml", cerbes_env)))
            .add_source(Environment::with_prefix("CERBES").separator("__"))
            .build()
            .expect("Could loadconfig");

        return s.try_deserialize().expect("Couldn't deserialize config");
    }
}

lazy_static! {
    pub static ref SETTINGS: Settings = Settings::new();
}
