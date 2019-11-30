from src.constants.alert_codes import *

fr = {}

default = (
    "Une erreur est survenue lors du traitement de votre "
    "demande, merci de contacter kingbee.root@gmail.com "
    "si l'erreur persiste."
)

errors = {
    INTERNAL_ERROR: default,
    SQL_PROCESSING_ERROR: default,
    USER_NOT_FOUND_ERROR: "Cet utilisateur n'existe pas",
    INCORRECT_PASSWORD_ERROR: "Le mot de passe fournit est incorrect",
    USER_ALREADY_EXISTS_ERROR: "Cet utilisateur existe déjà",
    EMAIL_ALREADY_EXISTS_ERROR: "Cet email est déjà utilisé",
    TRANSLATION_ID_DOES_NOT_EXISTS: default,
    USERS_MIXED_UP_ERROR: default,
    SQL_FOREIGN_KEY_ERROR: "Cette donnée est actuellement utilisée par d'autres objets et ne peut pas être supprimée",
    OBJECT_COLUMN_NOT_FOUND: "La suppression n'a pas pu se faire. Contacter l'administrateur si cette erreur persiste.",
    INCORRECT_EMAIL_FORMAT: "Le format de l'email fournit est incorrect",
    INCORRECT_PASSWORD_FORMAT: "Le format du mot de passe fournit est incorrect",
    MISSING_INFORMATION_REGISTER: "L'email ou le nom d'utilisateur n'ont pas été fourni",
    SWARM_ALREADY_EXISTS: "La ruche est déjà attaché à un essaim",
    USER_COULD_NOT_BE_IDENTIFIED: "L'utilisateur connecté n'a pas pu être identifié",
    STRING_CANNOT_BE_CONVERTED_TO_DATE: "Une erreur est survenue lors du traitement d'une date",
    MISSING_INFORMATION_APIARY: "Des informations manquantes bloquent la création du rucher",
    INCONSISTANT_DATA: "Des données inconsistantes ont été reçues",
    EMPTY_FIELD: "Des données reçues sont vides",
    UNKNOWN_DATA: "Type de donnée inconnu",
}


successes = {
    LOGIN_SUCCESS: ("Bonjour !", "Vous êtes connecté"),
    REGISTER_SUCCESS: ("Bienvenue !", "Vous êtes bien enregistré"),
    PASSWORD_RESET_SUCCESS: ("", "Votre mot de passe a bien été réinitialisé"),
    NEW_PARAMETER_SUCCESS: ("", "Nouveau paramètre ajouté avec succés"),
    NEW_HIVE_SUCCESS: ("", "Ruche créée avec succés !"),
    NEW_BEEKEEPER_SUCCESS: ("", "Apiculteur créé avec succés !"),
    NEW_APIARY_SUCCESS: ("", "RUcher créé avec succés !"),
    MODIFICATION_SUCCESS: ("", "Modification faites avec succés !"),
    ACTION_PLANIFICATION_SUCCESS: ("", "Action planifiée avec succés !"),
    ACTION_SOLVED_SUCCESS: ("", "Action résolue avec succés !"),
    DELETION_SUCCESS: ("", "Suppression faites avec succés !"),
    NEW_COMMENT_SUCCESS: ("", "Nouveau commentaire enregistré !"),
    NEW_SWARM_SUCCESS: ("", "Nouvel essaim enregistré !"),
    SWARM_ATTACH_WITH_SUCCESS: ("", "Nouvel essaim enregistré !"),
}
