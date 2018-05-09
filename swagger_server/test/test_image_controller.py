# coding: utf-8

from __future__ import absolute_import

from flask import json
from six import BytesIO

from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.image import Image  # noqa: E501
from swagger_server.test import BaseTestCase


class TestImageController(BaseTestCase):
    """ImageController integration test stubs"""

    def test_image_upload_post(self):
        """Test case for image_upload_post

        Uploads a file.
        """
        data = dict(image=(BytesIO(b'some file data'), 'file.txt'),
                    description='description_example')
        response = self.client.open(
            '/v1/image/upload',
            method='POST',
            data=data,
            content_type='multipart/form-data')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))

    def test_image_uuid_get(self):
        """Test case for image_uuid_get

        Returns a image.
        """
        response = self.client.open(
            '/v1/image/{uuid}'.format(uuid='uuid_example'),
            method='GET')
        self.assert200(response,
                       'Response body is : ' + response.data.decode('utf-8'))


if __name__ == '__main__':
    import unittest
    unittest.main()
