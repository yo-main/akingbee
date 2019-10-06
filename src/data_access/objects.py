"""
THIS MODULE IS DEPRECATED AND REPLACED BY PEEWEE
"""

# import re
# import datetime
# from copy import copy

# from src.data_access.utils import SQLObject
# from src.data_access.utils import DataAccess


# TEMPLATE_EMAIL = re.compile("^[a-zA-Z0-9\-._]+@[a-zA-Z\-._]+\.[a-zA-Z]{2,}$")


# @DataAccess()
# class User(SQLObject):
#     table = "users"
#     columns = {
#         "id": int,
#         "username": str,
#         "pwd": str,
#         "email": TEMPLATE_EMAIL,
#         "date_last_connection": datetime.datetime,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class BeehouseAction(SQLObject):
#     table = "beehouse_actions"
#     foreign = {"user": User}
#     columns = {
#         "id": int,
#         "fr": str,
#         "en": str,
#         "user": int,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class CommentsType(SQLObject):
#     table = "comments_type"
#     columns = {
#         "id": int,
#         "fr": str,
#         "en": str,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class Health(SQLObject):
#     table = "health"
#     foreign = {"user": User}
#     columns = {
#         "id": int,
#         "fr": str,
#         "en": str,
#         "user": int,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class HoneyType(SQLObject):
#     table = "honey_type"
#     foreign = {"user": User}
#     columns = {
#         "id": int,
#         "fr": str,
#         "en": str,
#         "user": int,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class Owner(SQLObject):
#     table = "owner"
#     foreign = {"user": User}
#     columns = {
#         "id": int,
#         "name": str,
#         "user": int,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class StatusActions(SQLObject):
#     table = "status_actions"
#     columns = {
#         "id": int,
#         "fr": str,
#         "en": str,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class StatusApiary(SQLObject):
#     table = "status_apiary"
#     foreign = {"user": User}
#     columns = {
#         "id": int,
#         "fr": str,
#         "en": str,
#         "user": int,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class StatusBeehouse(SQLObject):
#     table = "status_beehouse"
#     foreign = {"user": User}
#     columns = {
#         "id": int,
#         "fr": str,
#         "en": str,
#         "user": int,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class Apiary(SQLObject):
#     table = "apiary"
#     foreign = {"status": StatusApiary, "honey_type": HoneyType, "user": User}
#     columns = {
#         "id": int,
#         "name": str,
#         "birthday": datetime.datetime,
#         "location": str,
#         "status": int,
#         "honey_type": int,
#         "user": int,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class Beehouse(SQLObject):
#     table = "beehouse"
#     foreign = {
#         "user": User,
#         "apiary": Apiary,
#         "health": Health,
#         "owner": Owner,
#         "status": StatusBeehouse,
#     }
#     columns = {
#         "id": int,
#         "name": str,
#         "birthday": datetime.datetime,
#         "apiary": int,
#         "status": int,
#         "health": int,
#         "owner": int,
#         "user": int,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class Actions(SQLObject):
#     table = "actions"
#     foreign = {
#         "beehouse": Beehouse,
#         "type": BeehouseAction,
#         "status": StatusActions,
#         "user": User,
#     }
#     columns = {
#         "id": int,
#         "beehouse": int,
#         "date": datetime.datetime,
#         "deadline": datetime.datetime,
#         "type": int,
#         "comment": str,
#         "status": int,
#         "user": int,
#         "date_done": datetime.datetime,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }


# @DataAccess()
# class Comments(SQLObject):
#     table = "comments"
#     foreign = {
#         "beehouse": Beehouse,
#         "apiary": Apiary,
#         "health": Health,
#         "action": Actions,
#         "type": CommentsType,
#         "user": User,
#     }
#     columns = {
#         "id": int,
#         "date": datetime.datetime,
#         "comment": str,
#         "beehouse": int,
#         "apiary": int,
#         "health": int,
#         "action": int,
#         "type": int,
#         "user": int,
#         "date_creation": datetime.datetime,
#         "date_modification": datetime.datetime,
#     }
