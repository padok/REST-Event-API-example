# coding: utf-8

from __future__ import absolute_import
from datetime import date, datetime  # noqa: F401

from typing import List, Dict  # noqa: F401

from swagger_server.models.base_model_ import Model
from swagger_server.models.member_public import MemberPublic  # noqa: F401,E501
from swagger_server import util


class MemberList(Model):
    """NOTE: This class is auto generated by the swagger code generator program.

    Do not edit the class manually.
    """

    def __init__(self, member_list: List[MemberPublic]=None):  # noqa: E501
        """MemberList - a model defined in Swagger

        :param member_list: The member_list of this MemberList.  # noqa: E501
        :type member_list: List[MemberPublic]
        """
        self.swagger_types = {
            'member_list': List[MemberPublic]
        }

        self.attribute_map = {
            'member_list': 'member_list'
        }

        self._member_list = member_list

    @classmethod
    def from_dict(cls, dikt) -> 'MemberList':
        """Returns the dict as a model

        :param dikt: A dict.
        :type: dict
        :return: The MemberList of this MemberList.  # noqa: E501
        :rtype: MemberList
        """
        return util.deserialize_model(dikt, cls)

    @property
    def member_list(self) -> List[MemberPublic]:
        """Gets the member_list of this MemberList.


        :return: The member_list of this MemberList.
        :rtype: List[MemberPublic]
        """
        return self._member_list

    @member_list.setter
    def member_list(self, member_list: List[MemberPublic]):
        """Sets the member_list of this MemberList.


        :param member_list: The member_list of this MemberList.
        :type member_list: List[MemberPublic]
        """

        self._member_list = member_list
