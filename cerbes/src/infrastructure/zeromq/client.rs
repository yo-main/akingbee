use crate::domain::adapters::publisher::PublisherTrait;
use crate::domain::errors::CerbesError;
use crate::settings::SETTINGS;
use async_trait::async_trait;
use serde::Serialize;
use std::sync::Arc;
use std::sync::Mutex;
use zmq;

#[derive(Clone)]
pub struct ZMQClient {
    socket: Arc<Mutex<zmq::Socket>>,
}

#[derive(Debug, Serialize)]
struct Message<'a> {
    routing_key: &'a str,
    body: &'a str,
}

impl<'a> Message<'a> {
    fn to_json(&self) -> String {
        serde_json::to_string(self).unwrap()
    }
}

impl ZMQClient {
    pub fn new() -> Self {
        let context = zmq::Context::new();
        let socket = context.socket(zmq::PUB).unwrap();
        println!("publishing to tcp://0.0.0.0:{}", SETTINGS.zeromq.port);
        socket
            .bind(&format!("tcp://0.0.0.0:{}", SETTINGS.zeromq.port))
            .unwrap();

        ZMQClient {
            socket: Arc::new(Mutex::new(socket)),
        }
    }
}

#[async_trait]
impl PublisherTrait for ZMQClient {
    async fn publish(&self, routing_key: &str, content: &str) -> Result<(), CerbesError> {
        let socket = self.socket.lock().unwrap();
        let msg = Message {
            routing_key,
            body: content,
        };

        socket
            .send(&msg.to_json().to_string(), 0)
            .map_err(|_| CerbesError::cant_publish_message())
    }
}
