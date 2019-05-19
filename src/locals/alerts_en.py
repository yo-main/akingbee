from src.constants.alert_codes import *

fr = {}

default = "An error has happened while processing your request.\n" \
          "Thank you to contact kingbee.root@gmail.com " \
          "if this keep happening"

errors = {
    SQL_PROCESSING_ERROR: default,
    USER_NOT_FOUND_ERROR: "This user does not exist",
    INCORRECT_PASSWORD_ERROR: "The provided password is incorrect",
    USER_ALREADY_EXISTS_ERROR: "This user already exists",
    EMAIL_ALREADY_EXISTS_ERROR: "This email is already used",
    TRANSLATION_ID_DOES_NOT_EXISTS: default,
    USERS_MIXED_UP_ERROR: default,
    INTERNAL_ERROR: default,
}



successes = {
    LOGIN_SUCCESS: ("Hello !", "You are connected"),
    REGISTER_SUCCESS: ("Welcome !", "You have been succesffully registered !"),
    PASSWORD_RESET_SUCCESS: ("", "You password has been successfully reseted !"),
    NEW_PARAMETER_SUCCESS: ("", "New parameter successfully added !"),
    NEW_BEEHOUSE_SUCCESS: ("", "Beehouse successfully created !"),
    NEW_BEEKEEPER_SUCCESS: ("", "Beekeeper successfully created !"),
    NEW_APIARY_SUCCESS: ("", "Apiary successfully created !"),
    MODIFICATION_SUCCESS: ("", "Modification successfully done !"),
    ACTION_PLANIFICATION_SUCCESS: ("", "Action planified with success !"),
    ACTION_SOLVED_SUCCESS: ("", "Action successfully solved !"),
    DELETION_SUCCESS: ("", "Deletion successfully done !"),
    NEW_COMMENT_SUCCESS: ("", "Commentary successfully registered !"),
}
