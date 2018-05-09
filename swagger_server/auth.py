import connexion
import flask
from swagger_server.database import db_session
from swagger_server.dbmodels.models import Event, Member

try:
    from decorator import decorator
except ImportError:
    import sys
    import logging
    logging.error('Missing dependency. Please run `pip install decorator`')
    sys.exit(1)


def check_auth(username: str, password: str):
    '''This function is called to check if a username /
    password combination is valid.'''

    getMember = db_session.query(Member).filter(Member.username == username).first()
    if getMember is None:
        return False

    return getMember.compare_member_passwd(password)


def check_owner(event_id, username):
    event = db_session.query(Event).filter(Event.id == event_id).first()
    if event is None:
        return False
    return event.host_member.username == username


def authenticate():
    '''Sends a 401 response that enables basic auth'''
    return connexion.problem(401, "Login Required", "You have to login with proper credentials", "WWW-Authenticate", headers={'WWW-Authenticate': 'Basic realm="Login Required"'})


@decorator
def requires_auth(f: callable, *args, **kwargs):
    auth = flask.request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return authenticate()
    return f(*args, **kwargs)


@decorator
def requires_user_sameuser(f: callable, *args, **kwargs):
    auth = flask.request.authorization
    if not auth or args[0] != auth.username:
        return connexion.problem(401, "Login Required", "You have only access to your account.", "WWW-Authenticate", headers={'WWW-Authenticate': 'Basic realm="Login Required"'})

    return f(*args, **kwargs)


@decorator
def requires_event_owner(f: callable, *args, **kwargs):
    auth = flask.request.authorization
    if not auth or not check_owner(args[0], auth.username):
        return connexion.problem(401, "Login Required", "You can't edit others Events.", "WWW-Authenticate", headers={'WWW-Authenticate': 'Basic realm="Login Required"'})
    return f(*args, **kwargs)
