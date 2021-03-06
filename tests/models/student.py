# -*-  coding: utf-8 -*-
"""
data models for tests
"""

# Copyright (C) 2015 ZetaOps Inc.
#
# This file is licensed under the GNU General Public License v3
# (GPLv3).  See LICENSE.txt for details.
from pyoko import Model, ListNode, field, Node

class Student(Model):
    # def __init__(self, **kwargs):
        # We define model relations in __init__ method, because Python parser raises a NameError
        # if we refer to a not yet defined class in body of another class.
        # self.contact_info = ContactInfo()
        # super(Student, self).__init__(**kwargs)
    # contact_info = ContactInfo()

    # def row_level_access(self):
    #     self.objects = self.objects.filter(user_in=self._context.user['id'],)


    number = field.String("Student No", index=True)
    pno = field.String("TC No", index=True)
    name = field.String("First Name", type='text_tr')
    surname = field.String("Last Name", type='text_tr')
    join_date = field.Date("Join Date", index=True)
    bio = field.Text("Biography", index=True)

    class AuthInfo(Node):
        username = field.String("Username", index=True)
        email = field.String("Email", index=True)
        password = field.String("Password")

    class Lectures(ListNode):
        name = field.String(type='text_tr')
        code = field.String(required=False, index=True)
        credit = field.Integer(default=0, index=True)

        class NodeInListNode(Node):
            foo = field.String()

        class Exams(ListNode):
            type = field.String()
            date = field.Date()
            point = field.Integer(store=False)

        class Attendance(ListNode):
            date = field.Date()
            hour = field.Integer()
            attended = field.Boolean(default=False)




