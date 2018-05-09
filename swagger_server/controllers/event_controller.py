import connexion
import flask
import six
from sqlalchemy import and_

from swagger_server import util
from swagger_server.auth import requires_auth, requires_event_owner
from swagger_server.dbmodels import models as dbModels
from swagger_server.database import db_session
from swagger_server.models.error import Error  # noqa: E501
from swagger_server.models.event import Event  # noqa: E501
from swagger_server.models.event_request import EventRequest  # noqa: E501
from swagger_server.models.success import Success  # noqa: E501
from swagger_server.tools import EvalBuilder


@requires_auth
def attend_event(event_id, state):  # noqa: E501
    """change attendence to a event

    This can only be done by the logged in member. # noqa: E501

    :param event_id: The Event ID
    :type event_id: int
    :param state: The status
    :type state: bool

    :rtype: Success
    """

    auth = flask.request.authorization

    member = db_session.query(dbModels.Member).filter(dbModels.Member.username == auth.username).first()

    event = db_session.query(dbModels.Event).filter(dbModels.Event.id == event_id).first()

    if state == True:
        event.participants.append(member)
    else:
        event.participants.remove(member)

    db_session.add(event)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        # Bad Error Handling TODO
        raise
        return connexion.problem(400, "Bad Request", "Event: model failed", "Parsing")

    return event.to_dict()


@requires_auth
def create_event(body):  # noqa: E501
    """Create event

    This can only be done by the logged in member. # noqa: E501

    :param body: Created event object
    :type body: dict | bytes 

    :rtype: Event
    """

    auth = flask.request.authorization

    if connexion.request.is_json:
        body = EventRequest.from_dict(connexion.request.get_json())  # noqa: E501

    member_id = db_session.query(dbModels.Member.id).filter(dbModels.Member.username == auth.username).first()[0]

    # TODO validate event body function
    if not body.start_datetime or not body.end_datetime or not body.start_datetime <= body.end_datetime:
        return connexion.problem(400, "Bad Request", "Date: Dates not valid; Is the start_date earlier than the end_date?", "Parsing")

    images = None
    if body.images:
        images = db_session.query(dbModels.Image).filter(dbModels.Image.uuid.in_(body.images)).all()

    newEvent = dbModels.Event(member_id, body.name, body.description, body.start_datetime, body.end_datetime, body.age_from, body.age_to, body.location, images)

    db_session.add(newEvent)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        # Bad Error Handling TODO
        raise
        return connexion.problem(400, "Bad Request", "Event: model failed", "Parsing")

    return newEvent.to_dict(), 201


@requires_auth
@requires_event_owner
def delete_event(event_id):  # noqa: E501
    """Delete event

    This can only be done by the logged in member. # noqa: E501

    :param event_id: The name that needs to be deleted
    :type event_id: int

    :rtype: Success
    """

    deleteEvent = db_session.query(dbModels.Event).filter(dbModels.Event.id == event_id).first()

    if deleteEvent is None:
        return connexion.problem(404, "Not Found", "event_id not found.", "Lookup")

    db_session.delete(deleteEvent)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        raise

    return {"success": True, "Description": "Event has been deleted."}


def get_event_by_id(event_id):  # noqa: E501
    """Get event by event_id

    Returns a full Event object # noqa: E501

    :param event_id: The name that needs to be fetched.
    :type event_id: int

    :rtype: Event
    """

    getEvent = db_session.query(dbModels.Event).filter(dbModels.Event.id == event_id).first()

    if getEvent is None:
        return connexion.problem(404, "Not Found", "event_id not found.", "Lookup")

    return getEvent.to_dict()


def get_event_list(start_id=None, end_id=None, start_date=None, end_date=None, max_items=None):  # noqa: E501
    """Get eventList

    Returns a list of reduced Event objects # noqa: E501

    :param start_id: Member_id the list starts with
    :type start_id: int
    :param end_id: Member_id the list ends with
    :type end_id: int
    :param start_date: Member_Date the list starts with
    :type start_date: str
    :param end_date: Member_Date the list ends with
    :type end_date: str
    :param max_items: max items count in the list
    :type max_items: int

    :rtype: None
    """

    if not max_items:
        max_items = 100

    evalBuilder = EvalBuilder()

    if start_id:
        evalBuilder.append('start_id <= dbModels.Event.id')
    if end_id:
        evalBuilder.append('dbModels.Event.id <= end_id')
    if start_date:
        start_date = util.deserialize_datetime(start_date)
        evalBuilder.append('start_date <= dbModels.Event.start_datetime')
    if end_date:
        end_date = util.deserialize_datetime(end_date)
        evalBuilder.append('dbModels.Event.end_datetime <= end_date')

    events = db_session.query(dbModels.Event).filter(eval(evalBuilder.getEvalStr())).order_by(dbModels.Event.start_datetime).limit(max_items).all()

    event_list = []
    for event in events:
        event_list.append(event.to_dict_list())

    if start_date:
        event_list = sorted(event_list, key=lambda k: k['start_datetime'])

    return {"event_list": event_list}


@requires_auth
@requires_event_owner
def update_event(event_id, body):  # noqa: E501
    """Updated event

    This can only be done by the logged in member. # noqa: E501

    :param event_id: name that need to be updated
    :type event_id: int
    :param body: Updated event object
    :type body: dict | bytes

    :rtype: Event
    """
    if connexion.request.is_json:
        body = EventRequest.from_dict(connexion.request.get_json())  # noqa: E501

    putEvent = db_session.query(dbModels.Event).filter(dbModels.Event.id == event_id).first()

    if putEvent is None:
        return connexion.problem(404, "Not Found", "event_id not found.", "Lookup")

    # TODO validate event body function
    if not body.start_datetime or not body.end_datetime or not body.start_datetime <= body.end_datetime:
        return connexion.problem(400, "Bad Request", "Date: Dates not valid; Is the start_date earlier than the end_date?", "Parsing")

    images = None
    if body.images:
        images = db_session.query(dbModels.Image).filter(dbModels.Image.uuid.in_(body.images)).all()

    putEvent.update(body.name, body.description, body.start_datetime, body.end_datetime, body.age_from, body.age_to, body.location, images)

    db_session.add(putEvent)

    try:
        db_session.commit()
    except:
        db_session.rollback()
        raise

    return putEvent.to_dict()
