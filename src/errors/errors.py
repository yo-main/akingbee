from .base import BaseError


class InternalError(BaseError):
    code = 500
    reference = 1
    en = "An internal error happened."
    fr = "Une erreur interne est survenue"


class SqlProcessingError(BaseError):
    code = 500
    reference = 2
    en = "An error happened while manipulating the database"
    fr = "Une erreur s'est produite en manipulant la base de données"


class UserNotFound(BaseError):
    reference = 3
    en = "This user does not exist"
    fr = "Cet utilisateur n'existe pas"


class IncorrectPassword(BaseError):
    reference = 4
    en = "The provided password is incorrect"
    fr = "Le mot de passe fournit est incorrect"


class UserAlreadyExists(BaseError):
    reference = 5
    en = "Username or email already taken"
    fr = "Nom d'utilisateur ou email déjà utilisé"


class TranslationIdDoesNotExists(BaseError):
    code = 500
    reference = 6
    en = "An error happened while trying to fetch locale data"
    fr = "Une erreur est survenue lors de la collecte de données locales"


class NotAuthorizedAccess(BaseError):
    code = 401
    reference = 7
    en = "Not authorized access"
    fr = "Accès non authorisé"


class DeleteIntegrityError(BaseError):
    reference = 8
    en = "This data is currently being used and cannot be deleted"
    fr = "Cette donnée est actuellement utilisée et ne peut être supprimée"


class ObjectColumnNotFound(BaseError):
    code = 500
    reference = 9
    en = "The deletion could not happen"
    fr = "La suppression n'a pas pu se faire"


class IncorrectEmailFormat(BaseError):
    reference = 10
    en = "The format of the provided email is incorrect"
    fr = "Le format de l'email fourni est incorrect"


class IncorrectPasswordFormat(BaseError):
    reference = 11
    en = "The format of the provided password is incorrect"
    fr = "Le format du mot de passe fourni est incorrect"


class SwarmAlreadyExists(BaseError):
    reference = 12
    en = "There's already a swarm in this hive"
    fr = "Il y a déjà un essaim au sein de cette ruche"


class UserCouldNotBeIdentified(BaseError):
    reference = 13
    en = "The user could not be identified"
    fr = "L'utilisateur n'a pas pu être identifié"


class NotDateFormat(BaseError):
    reference = 14
    en = "An error happened while trying to convert a string to date"
    fr = "Une erreur est survenue en voulant convertir un texte à une date"


class MissingInformation(BaseError):
    reference = 15
    en = "Some information are missing"
    fr = "Des informations sont manquantes"


class InconsistantData(BaseError):
    reference = 16
    en = "Inconsistant data was received"
    fr = "Données reçues inconsistantes"


class UnknownData(BaseError):
    reference = 17
    en = "Unknown data type"
    fr = "Type de donnée inconnue"


class HiveAlreadyInApiary(BaseError):
    reference = 18
    en = "This hive already belongs to an apiary"
    fr = "Cette ruche appartient déjà à un rucher"


class UnknownLanguage(BaseError):
    reference = 19

    def __init__(self, language):
        self.en = f"Unknown language: {language}"
        self.fr = f"Language inconnu: {language}"
        super().__init__()
