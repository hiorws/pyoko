# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
import datetime
import time
import uuid
import six
from pyoko.exceptions import ValidationError
from pyoko.conf import settings

DATE_TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
DATE_FORMAT = "%Y-%m-%dT00:00:00Z"
EMPTY_DATETIME = '0000-00-00T00:00:00Z'

# W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W
#
#  FIXME: INPUT VALIDATIONS ARE MISSING !!!
#
#     in __set__() methods of fields
#
# W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W#W

class BaseField(object):
    _TYPE = 'Field'
    default_value = None
    creation_counter = 0

    def __init__(self, title='',
                 default=None,
                 required=True,
                 index=False,
                 type=None,
                 store=False,
                 choices=None,
                 order=None,
                 **kwargs):
        self._order = order or self.creation_counter
        BaseField.creation_counter += 1
        self.required = required
        self.choices = choices
        self.title = title
        if type:
            self.solr_type = type
        self.index = index or bool(type)
        self.store = store
        self.default = default
        self.name = ''
        self.kwargs = kwargs

    def __get__(self, instance, cls=None):
        if cls is None:
            return self
        return instance._field_values.get(self.name, None) if instance else self.__class__
        # if val or not instance.parent:
        #     return val
        # else:
        #     instance._load_from_parent()
        #     return instance._field_values.get(self.name, None)

    def __set__(self, instance, value):
        instance._field_values[self.name] = value

    def _load_data(self, instance, value):
        """
        for some field types (eg:date, datetime)
        we treat differently to data that came from db and given by user
        """
        self.__set__(instance, value)

    def __delete__(self, instance):
        raise AttributeError("Can't delete an attribute")

    def clean_value(self, val):
        if val is None:
            val = self.default() if callable(self.default) else self.default
        return val

    def validate(self, val):
        return True


class String(BaseField):
    solr_type = 'string'
    pass

class Id(BaseField):
    solr_type = 'string'
    def __init__(self, *arg, **kwargs):
        super(Id, self).__init__(*arg, **kwargs)
        self.index = True

    def clean_value(self, val):
        try:
            if val:
                return str(val)
            else:
                return str(self.default() if self.default else uuid.uuid4().hex)
        except ValueError:
            raise ValidationError("%r could not be cast to string" % val)


class Text(BaseField):
    solr_type = 'text_general'
    pass


class Float(BaseField):
    solr_type = 'float'

    def clean_value(self, val):
        try:
            if val is not None:
                return float(val)
            elif val is None and self.default is not None:
                return float(
                    self.default() if callable(self.default) else self.default)
        except ValueError:
            raise ValidationError("%r could not be cast to float" % val)


class Boolean(BaseField):
    solr_type = 'boolean'

    def clean_value(self, val):
        if val is None:
            return bool(
                self.default() if callable(self.default) else self.default)
        else:
            return bool(val)


class DateTime(BaseField):
    solr_type = 'date'

    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', settings.DATETIME_DEFAULT_FORMAT or DATE_TIME_FORMAT)
        super(DateTime, self).__init__(*args, **kwargs)
        if self.default is None:
            self.default = EMPTY_DATETIME
        elif self.default == 'now':
            self.default = lambda: datetime.datetime.now().strftime(DATE_TIME_FORMAT)

    def clean_value(self, val):
        if val is None:
            return self.default() if callable(self.default) else self.default
        else:
            return val.strftime(DATE_TIME_FORMAT)

    def __set__(self, instance, value):
        if isinstance(value, six.string_types) and value:
            value = datetime.datetime.strptime(value, self.format)
        instance._field_values[self.name] = value

    def _load_data(self, instance, value):
        if value is None or value == EMPTY_DATETIME:
            value = ''
        else:
            value = datetime.datetime.strptime(value, DATE_TIME_FORMAT)
        instance._field_values[self.name] = value


class Date(BaseField):
    solr_type = 'date'

    def __init__(self, *args, **kwargs):
        self.format = kwargs.pop('format', settings.DATE_DEFAULT_FORMAT or DATE_FORMAT)
        super(Date, self).__init__(*args, **kwargs)
        if self.default is None:
            self.default = EMPTY_DATETIME
        elif self.default == 'now':
            self.default = lambda: datetime.datetime.now().strftime(DATE_FORMAT)

    def __set__(self, instance, value):
        if isinstance(value, six.string_types) and value:
            value = datetime.datetime.strptime(value, self.format).date()
        instance._field_values[self.name] = value

    def clean_value(self, val):
        if not val:
            return self.default() if callable(self.default) else self.default
        else:
            return val.strftime(DATE_FORMAT)

    def _load_data(self, instance, value):
        if value is None or value == EMPTY_DATETIME:
            value = ''
        else:
            value = datetime.datetime.strptime(value, DATE_FORMAT).date()
        instance._field_values[self.name] = value


class Integer(BaseField):
    # TODO: add checks for solr's int field's limits
    # TODO: add support for solr's long int field
    solr_type = 'int'
    default_value = 0

    def clean_value(self, val):
        if val is not None:
            try:
                return int(val)
            except ValueError:
                raise ValidationError("%r could not be cast to integer" % val)
        elif val is None and self.default is not None:
            return int(
                self.default() if callable(self.default) else self.default)
        else:
            return self.default_value


class TimeStamp(BaseField):
    solr_type = 'long'

    def __init__(self, *args, **kwargs):
        super(TimeStamp, self).__init__(*args, **kwargs)
        self.index = True

    def clean_value(self, val):
        return int(repr(time.time()).replace('.', ''))
