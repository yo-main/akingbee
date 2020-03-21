import json

from common.redis_client import RedisClient, QUEUE_EMAIL_RESET

EMAIL_RESET_BODY = {
    "fr": """
Bonjour,

Pour réinitialiser votre mot de passe, merci d'accéder à l'url ci-dessous:
https://www.akingbee.com/reset_password/{uuid}

Si vous n'êtes pas à l'origine de la demande, faites comme si de rien n'était, tout va bien (ou pas).

Bonne journée !
""",
    "en": """
Hello,

In order to reinitialize your password, please access to the below connect:
https://www.akingbee.com/reset_password/{uuid}

If you aren't the original requester of this operation, do like nothing happened, everything is alright (or not)

Good day !
""",
}


def send_reset_email(user, language):
    RedisClient().publish(
        channel=QUEUE_EMAIL_RESET,
        message=json.dumps(
            {
                "headers": {"To": user.email, "Subject": "Password reset"},
                "body": EMAIL_RESET_BODY[language].format(
                    uuid=user.reset_pwd_id
                ),
            }
        ),
    )
