#! -*- coding: utf-8 -*-

from yaml import load, Loader




FRENCH = 'fr'
ENGLISH = 'en'

STATUS_DONE = 1
STATUS_PENDING = 2


COMMENT_TYPE_USER = 1
COMMENT_TYPE_SYSTEM = 2
COMMENT_TYPE_ACTION = 3

COMMENT_TYPES = (
    COMMENT_TYPE_USER,
    COMMENT_TYPE_SYSTEM,
    COMMENT_TYPE_ACTION,
)


LANGUAGES = (
    FRENCH,
    ENGLISH
)

with open("environment.yaml", "r") as stream:
    ENVIRONMENT = load(stream, Loader=Loader)

DATABASE = {}
DATABASE['TEST'] = {
    'user': 'rarnal',
    'password': 'ForYanyansLove1*!',
    'host': '157.230.24.210',
    'database': 'akingbee_test',
}
DATABASE['PROD'] = {
    'user': 'rarnal',
    'password': 'ForYanyansLove1*!',
    'host': '157.230.24.210',
    'database': 'akingbee',
}


URL_ROOT = '/akingbee'


DEFAULT_HEALTH = (
    {FRENCH: "Bonne", ENGLISH: "Good"},
    {FRENCH: "Moyenne", ENGLISH: "Medium"},
    {FRENCH: "Mauvais", ENGLISH: "Bad"}
)

DEFAULT_STATUS_BEEHOUSE = (
    {FRENCH: "Active", ENGLISH: "Active"},
    {FRENCH: "Stock", ENGLISH: "Stock"}
)

DEFAULT_STATUS_APIARY = (
    {FRENCH: "Actif", ENGLISH: "Active"},
    {FRENCH: "Inactif", ENGLISH: "Inactive"}
)

DEFAULT_ACTION_BEEHOUSE = (
    {FRENCH: "Bruler les abeilles", ENGLISH: "Burn the bees"},
    {FRENCH: "Arroser la ruche", ENGLISH: "Water the beehouse"},
    {FRENCH: "Trouver une nouvelle ruche", ENGLISH: "Find a new beehouse"},
    {FRENCH: "Trouver une nouvelle reine", ENGLISH: "Find a new bee queen"},
)

DEFAULT_HONEY_KIND = (
    {FRENCH: "Toutes fleurs", ENGLISH: "All flowers"},
    {FRENCH: "Acacia", ENGLISH: "Acacia"},
    {FRENCH: "Bruyère", ENGLISH: "Briar root"},
    {FRENCH: "Chataignier", ENGLISH: "Cheastnut"},
    {FRENCH: "Tournesol", ENGLISH: "Sunflower"},
)
