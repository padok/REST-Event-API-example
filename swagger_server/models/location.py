# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.address import Address  # noqa: F401,E501
from swagger_server import util


class Location(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, address: Address=None, name: str=None, longitude: float=None, latitude: float=None):  # noqa: E501
        """Location - a model defined in Swagger

        :param address: The address of this Location.  # noqa: E501
        :type address: Address
        :param name: The name of this Location.  # noqa: E501
        :type name: str
        :param longitude: The longitude of this Location.  # noqa: E501
        :type longitude: float
        :param latitude: The latitude of this Location.  # noqa: E501
        :type latitude: float
        """
        self.swagger_types = {
            'address': Address,
            'name': str,
            'longitude': float,
            'latitude': float
        }

        self.attribute_map = {
            'address': 'address',
            'name': 'name',
            'longitude': 'longitude',
            'latitude': 'latitude'
        }

        self._address = address
        self._name = name
        self._longitude = longitude
        self._latitude = latitude

    @classmethod
    def from_dict(cls, dikt) -> 'Location':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The Location of this Location.  # noqa: E501
        :rtype: Location
        """
        return util.deserialize_model(dikt, cls)

    @property
    def address(self) -> Address:
        """Gets the address of this Location.


        :return: The address of this Location.
        :rtype: Address
        """
        return self._address

    @address.setter
    def address(self, address: Address):
        """Sets the address of this Location.


        :param address: The address of this Location.
        :type address: Address
        """

        self._address = address

    @property
    def name(self) -> str:
        """Gets the name of this Location.


        :return: The name of this Location.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name: str):
        """Sets the name of this Location.


        :param name: The name of this Location.
        :type name: str
        """

        self._name = name

    @property
    def longitude(self) -> float:
        """Gets the longitude of this Location.


        :return: The longitude of this Location.
        :rtype: float
        """
        return self._longitude

    @longitude.setter
    def longitude(self, longitude: float):
        """Sets the longitude of this Location.


        :param longitude: The longitude of this Location.
        :type longitude: float
        """

        self._longitude = longitude

    @property
    def latitude(self) -> float:
        """Gets the latitude of this Location.


        :return: The latitude of this Location.
        :rtype: float
        """
        return self._latitude

    @latitude.setter
    def latitude(self, latitude: float):
        """Sets the latitude of this Location.


        :param latitude: The latitude of this Location.
        :type latitude: float
        """

        self._latitude = latitude
