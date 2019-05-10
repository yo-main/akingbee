#! -*- coding: utf-8 -*-

import sys
import inspect

from src.data_access import objects
from src.data_access import connectors
from src.data_access.tables import Table


def main():
    classes = inspect.getmembers(sys.modules[objects.__name__],
                                 inspect.isclass)

    tables = set(obj[1].table for obj in classes if obj[0] != "DataAccess" and
                                                    obj[1].table)
    conn = connectors.MySQL()
    cursor = conn.cursor()

    query = "DROP TABLE IF EXISTS {};"

    errors = 0

    try:
        while tables:
            to_del = set()
            for table in tables:
                if table:
                    try:
                        cursor.execute(query.format(table))
                        conn.commit()
                    except:
                        pass
                    else:
                        to_del.add(table)
            tables = tables - to_del
            if tables:
                errors += 1
            if errors > 10:
                raise Exception('noooooo')

    except Exception as e:
        conn.rollback()
        conn.close()
        raise e

    conn.close()

    tab = Table()
    tab._create_tables()


if __name__ == "__main__":
    main()
