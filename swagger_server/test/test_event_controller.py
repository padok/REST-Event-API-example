# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.event import Event  # noqa: E501
from swagger_server.models.event_request import EventRequest  # noqa: E501
from swagger_server.models.success import Success  # noqa: E501
from swagger_server.test import BaseTestCase


class TestEventController(BaseTestCase):
    """EventController integration test stubs"""

    def test_attend_event(self):
        """Test case for attend_event

        change attendence to a event
        """
        response = self.client.open(
            '/v1/event/{event_id}/attend/{state}'.format(event_id=56, state=true),
            method='PUT')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_create_event(self):
        """Test case for create_event

        Create event
        """
        body = EventRequest()
        response = self.client.open(
            '/v1/event',
            method='POST',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_delete_event(self):
        """Test case for delete_event

        Delete event
        """
        response = self.client.open(
            '/v1/event/{event_id}'.format(event_id=56),
            method='DELETE')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_event_by_id(self):
        """Test case for get_event_by_id

        Get event by event_id
        """
        response = self.client.open(
            '/v1/event/{event_id}'.format(event_id=56),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_get_event_list(self):
        """Test case for get_event_list

        Get eventList
        """
        query_string = [('start_id', 56),
                        ('end_id', 56),
                        ('start_date', '2013-10-20T19:20:30+01:00'),
                        ('end_date', '2013-10-20T19:20:30+01:00'),
                        ('max_items', 56)]
        response = self.client.open(
            '/v1/event',
            method='GET',
            query_string=query_string)
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_update_event(self):
        """Test case for update_event

        Updated event
        """
        body = EventRequest()
        response = self.client.open(
            '/v1/event/{event_id}'.format(event_id=56),
            method='PUT',
            data=json.dumps(body),
            content_type='application/json')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
