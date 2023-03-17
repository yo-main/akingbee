use async_trait::async_trait;
use cerbes::domain::adapters::publisher::PublisherTrait;
use cerbes::domain::errors::CerbesError;

pub struct TestPublisher;

impl TestPublisher {
    pub fn new() -> Self {
        TestPublisher {}
    }
}

#[async_trait]
impl PublisherTrait for TestPublisher {
    async fn publish(&self, _routing_key: &str, _content: &str) -> Result<(), CerbesError> {
        Ok(())
    }
}
