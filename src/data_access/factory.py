from concurrent import futures
import datetime
import flask

from mysql.connector import errors as mysql_error

from src.data_access.connectors import MySQL as SQL
from src.data_access.base_object import BaseObject
from src.constants import environments as ENV
from src.services.logger import logger
from src.services.alerts import Error
from src.constants import alert_codes as alerts


class Factory:
    state = False

    def __init__(self, autocommit=True):
        self.autocommit = autocommit
        if not autocommit and not self.state:
            self._create_connection()

    def __enter__(self):
        if not self.state:
            self._create_connection()
        return self

    def __exit__(self, type_, value, traceback):
        if self.state:
            self.conn.commit()
            self.conn.close()

    def _create_connection(self):
        self.conn = SQL()
        self.cursor = self.conn.cursor()
        self.state = True

    def rollback(self):
        self.conn.rollback()
        self.conn.close()
        self.state = False

    def commit(self):
        self.conn.commit()
        self.conn.close()
        self.state = False

    def get_all(self, class_, deepth=0):
        raw_data = self._search(class_, {})
        if not raw_data:
            return []

        out = self._build_class(class_, raw_data, deepth)
        return out

    def get_from_id(self, id, class_, deepth=0):
        if not id:
            return None

        raw_data = self._search(class_, {"id": id})
        if not raw_data:
            return None

        out = self._build_class(class_, raw_data, deepth)
        return out[0]

    def get_from_filters(self, class_, filters, deepth=0):
        if not filters:
            return []

        raw_data = self._search(class_, filters)
        if not raw_data:
            return []

        out = self._build_class(class_, raw_data, deepth)
        return out

    def _execute(self, query, params=None):
        if params is None:
            params = []

        logger.info(query + str(params))

        if self.autocommit:
            self._create_connection()

        try:
            self.cursor.execute(query, params)

            if query.startswith("INSERT"):
                data = self.cursor.lastrowid
            elif query.startswith("SELECT"):
                data = self.cursor.fetchall()
            else:
                data = []
        except mysql_error.IntegrityError as e:
            logger.info(e)
            raise Error(alerts.SQL_FOREIGN_KEY_ERROR)
        except Exception as e:
            logger.critical(e)
            raise e

        return data

    def _build_sql_params(self, filters, bounded=False):
        columns, params = [], []
        for key, item in filters.items():
            if bounded:
                columns.append("{}=%s".format(key))
            else:
                columns.append(key)

            if isinstance(item, datetime.datetime):
                item = self._convert_date(item)
            elif isinstance(item, BaseObject):
                item = item.id
            params.append(item)

        return columns, params

    def _search(self, class_, filters):
        if "user" in class_.columns:
            filters["user"] = ENV.USER_ID

        columns, params = self._build_sql_params(filters, bounded=True)
        query = "SELECT {} FROM {} ".format(
            ",".join(class_.columns), class_.table
        )

        if columns:
            query += "WHERE "
            query += " AND ".join(columns)

        query += ";"

        raw_data = self._execute(query, params)

        if not raw_data:
            return []
        return raw_data

    def _build_class(self, class_, raw_data, deepth):
        out = []

        if deepth:
            deepth -= 1

        workers = 10
        with futures.ThreadPoolExecutor(workers) as executor:
            work = [
                executor.submit(self._build_all, class_, raw, deepth)
                for raw in raw_data
            ]
            for done in futures.as_completed(work):
                res = done.result()
                out.append(res)

        return out

    def _build_all(self, class_, raw, deepth):
        data = {}
        for key, item in zip(class_.columns, raw):
            if item and class_.columns[key].args == datetime.datetime:
                if isinstance(item, str):
                    item = self._convert_date(item)
            data[key] = item
        return class_(data, deepth)

    @staticmethod
    def _convert_date(date):
        """ will convert to isoformat or convert to datetime from isoformat"""
        if isinstance(date, datetime.date):
            return date.isoformat(timespec="seconds")
        return datetime.datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    def update(self, table, values):
        assert "id" in values

        id_ = values["id"]
        del values["id"]

        if not values:
            return False

        if "date_modification" not in values:
            values["date_modification"] = datetime.datetime.now()

        columns, params = self._build_sql_params(values, bounded=True)

        query = "UPDATE {} SET ".format(table)
        query += ", ".join(columns)
        query += " WHERE id=%s;"
        params.append(id_)

        self._execute(query, params)

        if self.autocommit:
            self.commit()

        return True

    def delete_all_linked_to(self, class_, obj_to_delete):
        column = class_.find_column_related_to(obj_to_delete)

        if not column:
            raise Error(alerts.OBJECT_COLUMN_NOT_FOUND)

        query = "DELETE FROM {} WHERE {}=%s;".format(class_.table, column)
        params = [obj_to_delete.id]

        self._execute(query, params)

        if self.autocommit:
            self.commit()

        return True

    def delete_object(self, obj):
        if not obj.id:
            return False

        query = "DELETE FROM {} WHERE id=%s;".format(obj.table)
        params = [obj.id]

        self._execute(query, params)

        if self.autocommit:
            self.commit()

        return True

    def create(self, table, values):
        if "date_creation" not in values:
            values["date_creation"] = datetime.datetime.now()

        columns, params = self._build_sql_params(values)
        query = "INSERT INTO {} ".format(table)
        query += "({}) ".format(", ".join(columns))
        query += "VALUES ({});".format(", ".join(["%s"] * len(params)))

        res = self._execute(query, params)

        if self.autocommit:
            self.commit()

        return res

    def count(self, class_, values):
        columns, params = self._build_sql_params(values, bounded=True)
        query = "SELECT COUNT(*) FROM {} WHERE ".format(class_.table)
        query += " AND ".join(columns)
        query += ";"

        res = self._execute(query, params)
        return int(res[0][0])
