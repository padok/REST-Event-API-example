# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server import util


class Price(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, price_group: str=None, value: float=None):  # noqa: E501
        """Price - a model defined in Swagger

        :param price_group: The price_group of this Price.  # noqa: E501
        :type price_group: str
        :param value: The value of this Price.  # noqa: E501
        :type value: float
        """
        self.swagger_types = {
            'price_group': str,
            'value': float
        }

        self.attribute_map = {
            'price_group': 'priceGroup',
            'value': 'value'
        }

        self._price_group = price_group
        self._value = value

    @classmethod
    def from_dict(cls, dikt) -> 'Price':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Price of this Price.  # noqa: E501
        :rtype: Price
        """
        return util.deserialize_model(dikt, cls)

    @property
    def price_group(self) -> str:
        """Gets the price_group of this Price.


        :return: The price_group of this Price.
        :rtype: str
        """
        return self._price_group

    @price_group.setter
    def price_group(self, price_group: str):
        """Sets the price_group of this Price.


        :param price_group: The price_group of this Price.
        :type price_group: str
        """

        self._price_group = price_group

    @property
    def value(self) -> float:
        """Gets the value of this Price.


        :return: The value of this Price.
        :rtype: float
        """
        return self._value

    @value.setter
    def value(self, value: float):
        """Sets the value of this Price.


        :param value: The value of this Price.
        :type value: float
        """

        self._value = value