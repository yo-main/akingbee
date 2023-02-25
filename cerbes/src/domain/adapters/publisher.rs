use async_trait::async_trait;

use crate::domain::errors::CerbesError;

#[async_trait]
pub trait PublisherTrait {
    async fn publish(&self, routing_key: &str, content: &str) -> Result<(), CerbesError>;
}
