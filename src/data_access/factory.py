import datetime

from src.data_access.connectors import MySQL as SQL
from src.data_access.base_object import BaseObject


class Factory:

    def get_from_id(self, id, class_, recursive=False):
        raw_data = self._search(class_, {'id': id})
        if not raw_data:
            return None
        out = self._build_class(class_, raw_data, recursive)
        return out[0]


    def get_from_filters(self, class_, filters, recursive=False):
        raw_data = self._search(class_, filters)
        if not raw_data:
            return None
        out = self._build_class(class_, raw_data, recursive)
        return out


    def _build_sql_params(self, filters):
        columns, params = [], []
        for key, item in filters.items():
            columns.append("{}=?".format(key))

            if isinstance(item, datetime.datetime):
                item = self._convert_date(item)
            elif isinstance(item, BaseObject):
                item = item.id
            params.append(item)

        return columns, params


    def _search(self, class_, filters):
        if not filters:
            return None
        columns, params = self._build_sql_params(filters)
        query = "SELECT {} FROM {} WHERE ".format(','.join(class_.columns),
                                                  class_.table)
        query += " AND ".join(columns)
        query += ";"

        with SQL() as cursor:
            cursor.execute(query, params)
            raw_data = cursor.fetchall()

        if not raw_data:
            return None
        return raw_data


    def _build_class(self, class_, raw_data, recursive):
        out = []
        for raw in raw_data:
            data = {}
            for key, item in zip(class_.columns, raw):
                if item and class_.columns[key].args == datetime.datetime:
                    item = self._convert_date(item)
                data[key] = item
            out.append(class_(data, recursive))
        return out


    @staticmethod
    def _convert_date(date):
        """ will convert to isoformat or convert to datetime from isoformat"""
        if isinstance(date, datetime.datetime):
            return date.isoformat(timespec='seconds')
        return datetime.datetime.strptime(date, "%Y-%m-%dT%H:%M:%S")


    def update(self, table, values):
        assert 'id' in values

        id_ = values['id']
        del values['id']

        if not values:
            return False

        columns, params = self._build_sql_params(values)

        query = "UPDATE {} SET ".format(table)
        query += ', '.join(columns)
        query += " WHERE id=?;"
        params.append(id_)

        with SQL() as cursor:
            cursor.execute(query, params)

        return True


    def create(self, table, values):
        if 'date_creation' not in values:
            values['date_creation'] = datetime.datetime.now()

        columns, params = self._build_sql_params(values)
        query = "INSERT INTO {} ".format(table)
        query += "({}) ".format(', '.join(columns))
        query += "VALUES ({});".format(", ".join('?' * len(params)))

        with SQL() as cursor:
            res = cursor.execute(query, params)

        return res


    def count(self, class_, values):
        columns, params = self._build_sql_params(values)

        query = "SELECT COUNT(*) FROM {} WHERE ".format(class_.table)
        query += " AND ".join(columns)
        query += ";"

        with SQL() as cursor:
            cursor.execute(query, params)
            res = int(cursor.fetchall()[0][0])

        return res

