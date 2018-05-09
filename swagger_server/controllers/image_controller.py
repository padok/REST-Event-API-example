import errno
import os
import uuid

import connexion
import flask
import six
from sqlalchemy import event

from swagger_server import util
from swagger_server.auth import requires_auth
from swagger_server.dbmodels import models as dbModels
from swagger_server.database import db_session
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.image import Image  # noqa: E501
from swagger_server.tools import create_path

from swagger_server.settings import IMAGE_DATA_PATH, ALLOWED_MIME_TYPES


@event.listens_for(dbModels.Image, 'after_delete')
def receive_before_delete(mapper, connection, target):
    """listen for the Image 'before_delete' event

    Deletes the file associated with the image record from the data directory.
    """
    os.remove(IMAGE_DATA_PATH+target.uuid)


@requires_auth
def image_upload_post(image, description=None):  # noqa: E501
    """Uploads a file.

     # noqa: E501

    :param image: The file to upload.
    :type image: werkzeug.datastructures.FileStorage
    :param description: Description of the Image.
    :type description: str

    :rtype: Image
    """

    # check file
    if image.content_type not in ALLOWED_MIME_TYPES:
        # 415 Unsupported Media Type - https://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.16
        return connexion.problem(415, "Unsupported Media Type", "Image: only files with mime-type "+str(ALLOWED_MIME_TYPES)+" are allowed", "Parsing")

    # File Handling
    unique_id = str(uuid.uuid1())
    path = IMAGE_DATA_PATH+unique_id
    create_path(path)

    # Database
    auth = flask.request.authorization
    member_id = db_session.query(dbModels.Member.id).filter(dbModels.Member.username == auth.username).first()[0]
    newImage = dbModels.Image(member_id, unique_id, path, image.content_type, description)

    db_session.add(newImage)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        # Error Handling TODO
        raise

    # Save file if database was successful
    image.save(path)

    return newImage.to_dict()


def image_uuid_get(uuid):  # noqa: E501
    """Returns a image.

     # noqa: E501

    :param uuid: Returns an Image
    :type uuid: str

    :rtype: None
    """

    mimetype_query = db_session.query(dbModels.Image.mimetype).filter(dbModels.Image.uuid == uuid).first()

    if not mimetype_query:
        return connexion.problem(404, "Not Found", "uuid not found.", "Lookup")

    return flask.send_file(IMAGE_DATA_PATH+uuid, mimetype=mimetype_query[0])
