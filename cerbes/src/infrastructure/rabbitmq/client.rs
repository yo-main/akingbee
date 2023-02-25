use crate::domain::adapters::publisher::PublisherTrait;
use crate::domain::errors::CerbesError;
use crate::settings::SETTINGS;
use amqprs::callbacks::DefaultChannelCallback;
use amqprs::callbacks::DefaultConnectionCallback;
use amqprs::channel::BasicPublishArguments;
use amqprs::channel::Channel;
use amqprs::connection::Connection;
use amqprs::connection::OpenConnectionArguments;
use amqprs::BasicProperties;
use async_trait::async_trait;
use tokio::time;

pub struct RbmqClient {
    connection: Connection,
    channel: Channel,
    exchange: String,
}

impl RbmqClient {
    pub async fn new() -> Self {
        let connection = Connection::open(&OpenConnectionArguments::new(
            &SETTINGS.rabbitmq.host,
            SETTINGS.rabbitmq.port,
            &SETTINGS.rabbitmq.user,
            &SETTINGS.rabbitmq.password,
        ))
        .await
        .unwrap();

        connection
            .register_callback(DefaultConnectionCallback)
            .await
            .unwrap();

        let channel = connection.open_channel(None).await.unwrap();
        channel
            .register_callback(DefaultChannelCallback)
            .await
            .unwrap();

        RbmqClient {
            connection,
            channel,
            exchange: SETTINGS.rabbitmq.exchange.clone(),
        }
    }
}

#[async_trait]
impl PublisherTrait for RbmqClient {
    async fn publish(&self, routing_key: &str, content: &str) -> Result<(), CerbesError> {
        let content = content.bytes().collect();
        let args = BasicPublishArguments::new(&self.exchange, routing_key);

        self.channel
            .basic_publish(BasicProperties::default(), content, args)
            .await
            .unwrap();

        time::sleep(time::Duration::from_secs(1)).await;

        Ok(())
    }
}

pub struct TestRbmqClient;

impl TestRbmqClient {
    pub fn new() -> Self {
        TestRbmqClient {}
    }
}

#[async_trait]
impl PublisherTrait for TestRbmqClient {
    async fn publish(&self, _routing_key: &str, _content: &str) -> Result<(), CerbesError> {
        Ok(())
    }
}
