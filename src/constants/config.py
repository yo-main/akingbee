#! -*- coding: utf-8 -*-

FRENCH = "fr"
ENGLISH = "en"

STATUS_DONE = 1
STATUS_PENDING = 2

COMMENT_TYPE_USER = 1
COMMENT_TYPE_SYSTEM = 2
COMMENT_TYPE_ACTION = 3

COMMENT_TYPES = (COMMENT_TYPE_USER, COMMENT_TYPE_SYSTEM, COMMENT_TYPE_ACTION)


LANGUAGES = (FRENCH, ENGLISH)


DEFAULT_HIVE_CONDITION = (
    {FRENCH: "Neuve", ENGLISH: "Brand new"},
    {FRENCH: "Bon état", ENGLISH: "Good state"},
    {FRENCH: "Usagée", ENGLISH: "Used"},
    {FRENCH: "Inutilisable", ENGLISH: "Broken"},
)

DEFAULT_STATUS_APIARY = (
    {FRENCH: "Actif", ENGLISH: "Active"},
    {FRENCH: "Inactif", ENGLISH: "Inactive"},
)

DEFAULT_ACTION_TYPE = (
    {FRENCH: "Bruler les abeilles", ENGLISH: "Burn the bees"},
    {FRENCH: "Arroser la ruche", ENGLISH: "Water the hive"},
    {FRENCH: "Trouver une nouvelle ruche", ENGLISH: "Find a new hive"},
    {FRENCH: "Trouver une nouvelle reine", ENGLISH: "Find a new bee queen"},
)

DEFAULT_HONEY_KIND = (
    {FRENCH: "Toutes fleurs", ENGLISH: "All flowers"},
    {FRENCH: "Acacia", ENGLISH: "Acacia"},
    {FRENCH: "Bruyère", ENGLISH: "Briar root"},
    {FRENCH: "Chataignier", ENGLISH: "Cheastnut"},
    {FRENCH: "Tournesol", ENGLISH: "Sunflower"},
)

DEFAULT_SWARM_HEALTH = (
    {FRENCH: "Bonne", ENGLISH: "Good"},
    {FRENCH: "Moyenne", ENGLISH: "Medium"},
    {FRENCH: "Mauvaise", ENGLISH: "Bad"},
)
