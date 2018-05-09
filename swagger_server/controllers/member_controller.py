import logging
import re

import connexion
import six
import sqlalchemy.exc

from swagger_server import util
from swagger_server.auth import requires_auth, requires_user_sameuser
from swagger_server.dbmodels import models as dbModels
from swagger_server.database import db_session
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.member import Member  # noqa: E501
from swagger_server.models.member_create import MemberCreate  # noqa: E501
from swagger_server.models.member_private import MemberPrivate  # noqa: E501
from swagger_server.models.member_public import MemberPublic  # noqa: E501
from swagger_server.models.member_update import MemberUpdate  # noqa: E501
from swagger_server.models.success import Success  # noqa: E501


def create_member(body):  # noqa: E501
    """Create member

    This creates a new Member # noqa: E501

    :param body: Created member object
    :type body: dict | bytes

    :rtype: MemberPrivate
    """
    if connexion.request.is_json:
        body = MemberCreate.from_dict(connexion.request.get_json())  # noqa: E501

    if not body.username or not re.match(r'^(?=.{4,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$', body.username):
        return connexion.problem(400, "Bad Request", "Username validation failed.", "Parsing")

    if db_session.query(dbModels.Member.id).filter_by(username=body.username).scalar() is not None:
        return connexion.problem(409, "Conflict", "Username already used", "IntegrityError")

    newMember = dbModels.Member(body.username, body.password, body.name, body.email, body.description)

    db_session.add(newMember)

    try:
        db_session.commit()
    except Exception as e:
        logging.error(e)
        db_session.rollback()
        if isinstance(e, sqlalchemy.exc.IntegrityError):
            return connexion.problem(400, "Bad Request", "'username', 'name', 'password' and 'email' are required.", "Parsing")
        raise e

    return newMember.get_privat(), 201


@requires_auth
@requires_user_sameuser
def delete_member(username):  # noqa: E501
    """Delete member 

    This can only be done by the logged in member. 

    Attention! 
    All information, events and pictures associated with this member will be deleted!  # noqa: E501

    :param username: The name that needs to be deleted
    :type username: str

    :rtype: Success 
    """

    deleteMember = db_session.query(dbModels.Member).filter(dbModels.Member.username == username).first()

    if deleteMember is None:
        return connexion.problem(404, "Not Found", "Username not found.", "Lookup")

    db_session.delete(deleteMember)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        return connexion.problem(500, "Internal Server Error", "Database", "Database")

    return {"success": True, "Description": "Member has been deleted."}


def get_member_by_name(username):  # noqa: E501
    """Get public member information by member name

    Returns public Member information # noqa: E501

    :param username: The name that needs to be fetched.
    :type username: str

    :rtype: MemberPublic
    """

    getMember = db_session.query(dbModels.Member).filter(
        dbModels.Member.username == username).first()

    if getMember is None:
        return connexion.problem(404, "Not Found", "Username not found.", "Lookup")

    return getMember.get_public()


@requires_auth
@requires_user_sameuser
def get_member_by_name_private(username):  # noqa: E501
    """Get private member information by member name

    This can only be done by the logged in member. # noqa: E501

    :param username: The name that needs to be fetched.
    :type username: str

    :rtype: MemberPrivate
    """
    getMember = db_session.query(dbModels.Member).filter(
        dbModels.Member.username == username).first()

    if getMember is None:
        return connexion.problem(404, "Not Found", "Username not found.", "Lookup")

    return getMember.get_privat()


def get_member_list():  # noqa: E501
    """Get memberList

    Returns a list of reduced Member objects # noqa: E501


    :rtype: None
    """
    members = db_session.query(dbModels.Member).order_by(dbModels.Member.name)

    member_list = []
    for member in members:
        member_list.append(member.to_dict_list())

    return {"member_list": member_list}


@requires_auth
@requires_user_sameuser
def update_member(username, body):  # noqa: E501
    """Updated member

    This can only be done by the logged in member. # noqa: E501

    :param username: name that need to be updated
    :type username: str
    :param body: Update member object
    :type body: dict | bytes

    :rtype: MemberPrivate
    """
    if connexion.request.is_json:
        body = MemberUpdate.from_dict(connexion.request.get_json())  # noqa: E501

    updateMember = db_session.query(dbModels.Member).filter(dbModels.Member.username == username).first()

    updateMember.update(body.name, body.password, body.name, body.email, body.description)

    db_session.add(updateMember)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        # Bad Error Handling TODO
        return connexion.problem(400, "Bad Request", "Username, Name, Passwd and Email are required.", "Parsing")

    return updateMember.get_privat(), 200
