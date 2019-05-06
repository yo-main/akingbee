import re
from copy import copy

from src.data_access.factory import Factory
from src.data_access.base_object import BaseObject


class SQLObject(BaseObject):
    table = None
    columns = ()
    foreign = {}
    id = None

    def __init__(self, data=None, recursive=False):
        if data:
            self._init_with_values(data)
        self._create_missing_attr()
        if recursive:
            self._get_foreign_objects()

    def save(self):
        if self.id:
            new_values = self.get_diff()
            for table, values in new_values.items():
                if values:
                    Factory().update(table, values)
        else:
            items = {key: getattr(self, key)
                     for key in self.columns
                     if getattr(self, key) is not None}
            res = Factory().create(self.table, items)
            self.id = res[0]

    def get_diff(self):
        if self.id:
            original = Factory().get_from_id(self.id, type(self))
        else:
            original = type(self)()

        to_modify = {}

        to_modify[self.table] = {}
        for key in self.columns:
            new_value = getattr(self, key)
            old_value = getattr(original, key)

            if isinstance(new_value, BaseObject):
                to_modify.update(new_value.get_diff())
            else:
                if new_value != old_value:
                    to_modify[self.table][key] = new_value

            if to_modify[self.table]:
                to_modify[self.table]['id'] = self.id

        return to_modify

    def _init_with_values(self, data):
        assert all(key in self.columns for key in data)
        for key, item in data.items():
            setattr(self, key, item)

    def _create_missing_attr(self):
        for key in self.columns:
            if key not in self.__dict__:
                self.__dict__[key] = None

    def _get_foreign_objects(self):
        for key, class_ in self.foreign.items():
            id_ = getattr(self, key)
            if id_:
                self.__dict__[key] = Factory().get_from_id(id_, class_)

    def copy(self):
        return copy(self)

    def __copy__(self):
        new = type(self)()
        new.__dict__.update(
            {key: copy(item) for key, item in self.__dict__.items()}
        )
        return new

    def __repr__(self):
        return str(self.id)

    def __setattr__(self, key, item):
        if key == "columns":
            raise AttributeError("You cannot change the columns attribute")

        validator = self.columns[key]
        if item is None or validator.match(item):
            self.__dict__[key] = item
        else:
            raise ValueError('"{}" is not correct for {}'
                             .format(item, key))

    def __eq__(self, other):
        if not isinstance(other, (int, str, type(self))):
            return NotImplemented

        if isinstance(other, str):
            if not other.isdigit():
                return False
            other = int(other)

        if isinstance(other, type(self)):
            other = other.id

        return self.id == other

    def __str__(self):
        template = "{column:>{size_column}} | {value}\n"
        size_column = len(max(self.columns, key=len))
        out = template.format(column="COLUMNS",
                              size_column=size_column,
                              value="VALUES")
        for key in self.columns:
            value = getattr(self, key)
            if isinstance(value, BaseObject):
                value = value.id
            out += template.format(column=key,
                                   size_column=size_column,
                                   value=value)
        return out



class DataValidator:
    def __init__(self, arg):
        self.regex = False
        if isinstance(arg, type(re.compile(''))):
            self.regex = True
            self.validator = arg
        elif isinstance(arg, type):
            self.validator = arg
        else:
            raise TypeError("The provided argument is not correct: {}"
                            .format(arg))

    def validate(self, other):
        if not self.regex:
            return isinstance(other, self.validator)
        return bool(self.validator.match(other))



class DataTemplate:
    def __init__(self, args):
        self.args = args
        self.validators = []
        if isinstance(args, (list, tuple)):
            for arg in args:
                self.validators.append(DataValidator(arg))
        else:
            self.validators.append(DataValidator(args))

    def match(self, other):
        for validator in self.validators:
            if validator.validate(other):
                return True
        return False

    def __get__(self, obj, type=None):
        return self.args



class DataAccess:
    def __call__(self, class_object):
        for key, item in class_object.columns.items():
            class_object.columns[key] = DataTemplate(item)
        return class_object

