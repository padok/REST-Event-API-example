# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Contact(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, first_name: str=None, last_name: str=None, email: str=None, fax: str=None):  # noqa: E501
        """Contact - a model defined in Swagger

        :param first_name: The first_name of this Contact.  # noqa: E501
        :type first_name: str
        :param last_name: The last_name of this Contact.  # noqa: E501
        :type last_name: str
        :param email: The email of this Contact.  # noqa: E501
        :type email: str
        :param fax: The fax of this Contact.  # noqa: E501
        :type fax: str
        """
        self.swagger_types = {
            'first_name': str,
            'last_name': str,
            'email': str,
            'fax': str
        }

        self.attribute_map = {
            'first_name': 'firstName',
            'last_name': 'lastName',
            'email': 'email',
            'fax': 'fax'
        }

        self._first_name = first_name
        self._last_name = last_name
        self._email = email
        self._fax = fax

    @classmethod
    def from_dict(cls, dikt) -> 'Contact':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Contact of this Contact.  # noqa: E501
        :rtype: Contact
        """
        return util.deserialize_model(dikt, cls)

    @property
    def first_name(self) -> str:
        """Gets the first_name of this Contact.


        :return: The first_name of this Contact.
        :rtype: str
        """
        return self._first_name

    @first_name.setter
    def first_name(self, first_name: str):
        """Sets the first_name of this Contact.


        :param first_name: The first_name of this Contact.
        :type first_name: str
        """

        self._first_name = first_name

    @property
    def last_name(self) -> str:
        """Gets the last_name of this Contact.


        :return: The last_name of this Contact.
        :rtype: str
        """
        return self._last_name

    @last_name.setter
    def last_name(self, last_name: str):
        """Sets the last_name of this Contact.


        :param last_name: The last_name of this Contact.
        :type last_name: str
        """

        self._last_name = last_name

    @property
    def email(self) -> str:
        """Gets the email of this Contact.


        :return: The email of this Contact.
        :rtype: str
        """
        return self._email

    @email.setter
    def email(self, email: str):
        """Sets the email of this Contact.


        :param email: The email of this Contact.
        :type email: str
        """

        self._email = email

    @property
    def fax(self) -> str:
        """Gets the fax of this Contact.


        :return: The fax of this Contact.
        :rtype: str
        """
        return self._fax

    @fax.setter
    def fax(self, fax: str):
        """Sets the fax of this Contact.


        :param fax: The fax of this Contact.
        :type fax: str
        """

        self._fax = fax