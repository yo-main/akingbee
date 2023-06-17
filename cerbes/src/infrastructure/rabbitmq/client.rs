use crate::domain::adapters::publisher::PublisherTrait;
use crate::domain::errors::CerbesError;
use async_trait::async_trait;

#[derive(Clone)]
pub struct TestPublisherClient;

impl TestPublisherClient {
    pub fn new() -> Self {
        TestPublisherClient {}
    }
}

#[async_trait]
impl PublisherTrait for TestPublisherClient {
    async fn publish(&self, _routing_key: &str, _content: &str) -> Result<(), CerbesError> {
        println!("NOOOOO");
        Ok(())
    }
}
