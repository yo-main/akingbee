from .base import BaseSuccess

class LoginSuccess(BaseSuccess):
    en = "You are connected !"
    fr = "Vous êtes connecté !"

class RegisterSuccess(BaseSuccess):
    en = "Inscription succesful !"
    fr = "Inscription réussie !"

class PasswordResetSuccess(BaseSuccess):
    en = "Your password have successful reset"
    fr = "Votre mot de passe a bien été réinitialisé"

class NewParameterSuccess(BaseSuccess):
    en = "New parameter successfully added"
    fr = "Nouveau paramètre ajouté avec succés"

class NewHiveSuccess(BaseSuccess):
    en = "Hive successfully created"
    fr = "Ruche créée avec succés"

class NewOwnerSuccess(BaseSuccess):
    en = "Beekeeper succesfully created"
    fr = "Apiculteur créé avec succès"

class NewApiarySuccess(BaseSuccess):
    en = "Apiary successfully created"
    fr = "Rucher créé avec succés"

class ModificationSuccess(BaseSuccess):
    en = "Modification successfully done"
    fr = "Modification faites avec succés"

class EventPlanificationSuccess(BaseSuccess):
    en = "Event successfully planified"
    fr = "Évènement planifié avec succés"

class EventSolvedSuccess(BaseSuccess):
    en = "Event successfully solved"
    fr = "Évènement résolu avec succés"

class DeletionSuccess(BaseSuccess):
    en = "Deletion successfully done"
    fr = "Suppression faites avec succés"

class NewCommentSuccess(BaseSuccess):
    en = "New comment registered"
    fr = "Nouveau commentaire enregistré"

class NewSwarmSuccess(BaseSuccess):
    en = "Swarm successfully created"
    fr = "Essaim créé avec succés"

class SwarmAttachSuccess(BaseSuccess):
    en = "Swarm succesfully attached"
    fr = "Essaim attaché avec succés"

class HiveMoveSuccess(BaseSuccess):
    en = "Hive succesfully moved"
    fr = "Ruche déménagée avec succés"

