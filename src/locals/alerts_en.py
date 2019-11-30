from src.constants.alert_codes import *

fr = {}

default = (
    "An error has happened while processing your request.\n"
    "Thank you to contact kingbee.root@gmail.com "
    "if this keep happening"
)

errors = {
    INTERNAL_ERROR: default,
    SQL_PROCESSING_ERROR: default,
    USER_NOT_FOUND_ERROR: "This user does not exist",
    INCORRECT_PASSWORD_ERROR: "The provided password is incorrect",
    USER_ALREADY_EXISTS_ERROR: "This user already exists",
    EMAIL_ALREADY_EXISTS_ERROR: "This email is already used",
    TRANSLATION_ID_DOES_NOT_EXISTS: default,
    USERS_MIXED_UP_ERROR: default,
    SQL_FOREIGN_KEY_ERROR: "This data is currently being used by other objects and cannot be deleted",
    OBJECT_COLUMN_NOT_FOUND: "The deletion could not happen. Contact the administrateur if this error persists",
    INCORRECT_EMAIL_FORMAT: "The format of the provided email is incorrect",
    INCORRECT_PASSWORD_FORMAT: "The format of the provided password is incorrect",
    MISSING_INFORMATION_REGISTER: "The username or email were not provided",
    SWARM_ALREADY_EXISTS: "The hive is already attached to a swarm",
    USER_COULD_NOT_BE_IDENTIFIED: "The logged in user could not be identified",
    STRING_CANNOT_BE_CONVERTED_TO_DATE: "An error happened while trying to convert some date",
    MISSING_INFORMATION_APIARY: "Some information were missing to register the apiary",
    INCONSISTANT_DATA: "Inconsistant data was received",
    EMPTY_FIELD: "Received data were empty",
    UNKNOWN_DATA: "Unknown data type",
}


successes = {
    LOGIN_SUCCESS: ("Hello !", "You are connected"),
    REGISTER_SUCCESS: ("Welcome !", "You have been succesffully registered !"),
    PASSWORD_RESET_SUCCESS: (
        "",
        "You password has been successfully reseted !",
    ),
    NEW_PARAMETER_SUCCESS: ("", "New parameter successfully added !"),
    NEW_HIVE_SUCCESS: ("", "Hive successfully created !"),
    NEW_BEEKEEPER_SUCCESS: ("", "Beekeeper successfully created !"),
    NEW_APIARY_SUCCESS: ("", "Apiary successfully created !"),
    MODIFICATION_SUCCESS: ("", "Modification successfully done !"),
    ACTION_PLANIFICATION_SUCCESS: ("", "Action planified with success !"),
    ACTION_SOLVED_SUCCESS: ("", "Action successfully solved !"),
    DELETION_SUCCESS: ("", "Deletion successfully done !"),
    NEW_COMMENT_SUCCESS: ("", "Commentary successfully registered !"),
    NEW_SWARM_SUCCESS: ("", "Swarm successfully created !"),
    SWARM_ATTACH_WITH_SUCCESS: ("", "Swarm successfully created !"),
}
