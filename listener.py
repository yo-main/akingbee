from common.log.logger import logger
from common.redis_client import RedisClient, QUEUE_EMAIL_RESET
from messaging_bee.controller import reset_password


def main():
    logger.info("Starting messaging bee listener...")
    client = RedisClient()
    client.listen(QUEUE_EMAIL_RESET, reset_password)


if __name__ == "__main__":
    main()
