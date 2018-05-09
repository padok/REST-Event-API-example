# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.member_create import MemberCreate  # noqa: E501
from swagger_server.models.member_private import MemberPrivate  # noqa: E501
from swagger_server.models.member_public import MemberPublic  # noqa: E501
from swagger_server.models.member_update import MemberUpdate  # noqa: E501
from swagger_server.models.success import Success  # noqa: E501
from swagger_server.test import BaseTestCase


class TestMemberController(BaseTestCase):
    """MemberController integration test stubs"""

    def test_create_member(self):
        """Test case for create_member

        Create member
        """
        body = MemberCreate()
        response = self.client.open(
            '/v1/member',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_member(self):
        """Test case for delete_member

        Delete member
        """
        response = self.client.open(
            '/v1/member/{username}'.format(username='username_example'),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_member_by_name(self):
        """Test case for get_member_by_name

        Get public member information by member name
        """
        response = self.client.open(
            '/v1/member/{username}'.format(username='username_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_member_by_name_private(self):
        """Test case for get_member_by_name_private

        Get private member information by member name
        """
        response = self.client.open(
            '/v1/member/{username}/private'.format(username='username_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_member_list(self):
        """Test case for get_member_list

        Get memberList
        """
        response = self.client.open(
            '/v1/member',
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_member(self):
        """Test case for update_member

        Updated member
        """
        body = MemberUpdate()
        response = self.client.open(
            '/v1/member/{username}'.format(username='username_example'),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
