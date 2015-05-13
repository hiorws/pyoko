# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from time import time
from pyoko.exceptions import ValidationError


# class Link(object):
#     def __init__(self, model,  reverse=False):
#         self.reverse = reverse
#         self.model =
from pyoko.settings import SOLR_STORE_ALL


class BaseField(object):
    link_type = False
    default_value = None

    def __init__(self, required=False, index=False, default=None, index_as=None, store=SOLR_STORE_ALL):
        self.required = required
        self.index_as = index_as
        self.index = index or bool(index_as)
        self.store = store
        self.name = ''
        self.value = default or self.default_value
        self._updated = False  # user set or updated the value
        self._fetched = False  # value loaded from solr or riak
    #
    # def set_value(self, value):
    #     self._updated = self.validate(value)
    #     self.value = value

    def __get__(self, instance, cls=None):
        # return self
        # print "GET___", self.value, instance, cls
        if cls is None:
            return self
        return instance._field_values.get(self.name, None)

    def __set__(self, instance, value):
        # print "__set__ called for : ", self, value
        # self._updated = self.validate(value)
        instance._field_values[self.name] = value

    def __delete__(self,instance):
        raise AttributeError("Can't delete attribute")

    def clean_value(self, val):
        return val

    def validate(self, val):
        return True


# class Dict(BaseField):
#     pass


class String(BaseField):
    pass

class Text(BaseField):
    pass

class Boolean(BaseField):
    pass

class Date(BaseField):
    pass

class Timestamp(BaseField):
    def clean_value(self, val):
        return round(time())



class Integer(BaseField):
    default_value = 0

    def clean_value(self, val):
        val = val or self.default_value
        try:
            return int(val)
        except ValueError:
            raise ValidationError("%r could not be cast to integer" % val)
