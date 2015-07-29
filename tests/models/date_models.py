# -*-  coding: utf-8 -*-
"""
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.

from pyoko.model import Model, ListNode, field, Node

class DateModel(Model):
    date_with_format = field.Date(index=True, format="%d.%m.%Y")
    name = field.String(index=True)
