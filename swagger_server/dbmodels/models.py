from sqlalchemy import Boolean, CheckConstraint, Column, Date, DateTime, ForeignKey, Integer, String, Table, Text
from swagger_server.database import Base, metadata
from sqlalchemy.orm import backref, relationship

from swagger_server.tools import hashpasswd

import datetime


# Association tables

t_member_event = Table(
    'member_event', metadata,
    Column('member_id', ForeignKey('member.id', ondelete='CASCADE'), primary_key=True, nullable=False),
    Column('event_id', ForeignKey('event.id', ondelete='CASCADE'), primary_key=True, nullable=False)
)


t_member_image_gallery = Table(
    'member_image_gallery', metadata,
    Column('member_id', ForeignKey('member.id', ondelete='CASCADE'), nullable=False),
    Column('image_id', ForeignKey('image.id', ondelete='CASCADE'), primary_key=True)
)


t_event_image_gallery = Table(
    'event_image_gallery', metadata,
    Column('event_id', ForeignKey('event.id', ondelete='CASCADE'), nullable=False),
    Column('image_id', ForeignKey('image.id', ondelete='CASCADE'), primary_key=True)
)

# Class tables


class Member(Base):
    __tablename__ = 'member'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(Text(100), unique=True, nullable=False)
    passwd = Column(Text, nullable=False)
    name = Column(Text(100), nullable=False)
    email = Column(Text(100), nullable=False)
    description = Column(Text(300), nullable=True)
    created_at = Column(DateTime)

    events = relationship('Event', cascade='all, delete-orphan', back_populates='host_member')
    event_participations = relationship('Event', secondary=t_member_event, back_populates="participants")

    images = relationship('Image', cascade='all, delete-orphan', back_populates='owner_member')

    def set_member_passwd(self, passwd):
        self.passwd = hashpasswd(passwd)

    def compare_member_passwd(self, passwd):
        return self.passwd == hashpasswd(passwd)

    def update(self, username=None, passwd=None, name=None, email=None, description=None):
        if username:
            self.username = username
        if passwd:
            self.set_member_passwd(passwd)
        if name:
            self.name = name
        if description:
            self.description = description
        if email:
            self.email = email

    def get_public(self):
        return dict(
            id=self.id,
            username=self.username,
            name=self.name,
            description=self.description
        )

    def get_privat(self):
        images = []
        for p in self.images:
            images.append(p.to_dict())

        private_dict = dict(
            email=self.email,
            images=images
        )
        return {**self.get_public(), **private_dict}

    def to_dict_list(self):
        return dict(
            id=self.id,
            username=self.username,
            name=self.name,
            description_short=self.description[0:100]
        )

    def dump(self):
        return dict([(k, v) for k, v in vars(self).items() if not k.startswith('_')])

    def __iter__(self):
        return iter(self.get_public())

    def __init__(self, username, passwd, name, email=None, description=None):
        self.username = username
        self.set_member_passwd(passwd)
        self.name = name
        self.description = description
        self.email = email
        self.created_at = datetime.datetime.utcnow()

    def __repr__(self):
        return '<member_id %r, member_name %r>' % (self.id, self.name)


class Event(Base):
    __tablename__ = 'event'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    description = Column(Text)
    age_from = Column(Integer)
    age_to = Column(Integer)
    host_member_id = Column(Integer, ForeignKey('member.id', ondelete='CASCADE'))
    location_id = Column(Integer, ForeignKey('location.id', ondelete='CASCADE'))
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
    start_datetime = Column(DateTime)
    end_datetime = Column(DateTime)

    host_member = relationship('Member', back_populates='events')
    participants = relationship('Member', secondary=t_member_event, back_populates='event_participations')
    location = relationship('Location', single_parent=True, cascade='all, delete-orphan', back_populates='event')
    images = relationship('Image', secondary=t_event_image_gallery, back_populates='events')

    def update(self, name=None, description=None, start_datetime=None, end_datetime=None, age_from=None, age_to=None, location=None, images=None):
        if name:
            self.name = name
        if description:
            self.description = description
        # created_at
        self.updated_at = datetime.datetime.utcnow()
        if start_datetime:
            self.start_datetime = start_datetime
        if end_datetime:
            self.end_datetime = end_datetime
        if age_from:
            self.age_from = age_from
        if age_to:
            self.age_to = age_to
        if location:
            self.location.update(location.name, location.longitude, location.latitude, location.address)
        self.images = []
        if images:
            for image in images:
                self.images.append(image)

    def __init__(self, host_member_id, name, description, start_datetime, end_datetime, age_from=None, age_to=None, location=None, images=None):
        self.host_member_id = host_member_id
        self.name = name
        self.description = description
        currentTime = datetime.datetime.utcnow()
        self.created_at = currentTime
        self.updated_at = currentTime
        self.start_datetime = start_datetime
        self.end_datetime = end_datetime
        self.age_from = age_from
        self.age_to = age_to
        if location:
            self.location = Location(location.name, location.longitude, location.latitude, location.address)
        if images:
            self.images = []
            for image in images:
                self.images.append(image)

    def to_dict(self):
        participants = []
        for p in self.participants:
            participants.append(p.get_public())
        images = []
        for i in self.images:
            images.append(i.to_dict())
        return dict(id=self.id,
                    host=self.host_member.get_public(),
                    name=self.name,
                    description=self.description,
                    created_at=self.created_at,
                    updated_at=self.updated_at,
                    start_datetime=self.start_datetime,
                    end_datetime=self.end_datetime,
                    age_from=self.age_from,
                    age_to=self.age_to,
                    participants=participants,
                    images=images,
                    location=self.location.to_dict() if self.location else None
                    )

    def to_dict_list(self):
        return dict(id=self.id,
                    host=self.host_member.get_public(),
                    name=self.name,
                    description=self.description[0:100],
                    start_datetime=self.start_datetime,
                    end_datetime=self.end_datetime,
                    age_from=self.age_from,
                    age_to=self.age_to,
                    )

    def __iter__(self):
        return iter(self.to_dict())

    def __repr__(self):
        return '<Event: id=%r, name:%r>' % (self.id, self.name)


class Location(Base):
    __tablename__ = 'location'

    id = Column(Integer, primary_key=True)
    address_id = Column(ForeignKey('address.id', ondelete='CASCADE'), nullable=False)
    name = Column(Text, nullable=False)
    gps_longitude = Column(String, nullable=False)
    gps_latitude = Column(String, nullable=False)

    event = relationship('Event', back_populates='location')

    address = relationship('Address', single_parent=True, cascade='all, delete-orphan', back_populates='location')

    def to_dict(self):
        return dict(
            name=self.name,
            gps_latitude=self.gps_latitude,
            gps_longitude=self.gps_longitude,
            address=self.address.to_dict()
        )

    def update(self, name=None, longitude=None, latitude=None, address=None):
        self.name = name
        self.gps_longitude = longitude
        self.gps_latitude = latitude
        if address:
            self.address.update(address.name, address.street, address.city, address.state, address.zip)

    def __init__(self, name, longitude, latitude, address=None):
        self.name = name
        self.gps_longitude = longitude
        self.gps_latitude = latitude
        if address:
            self.address = Address(address.name, address.street, address.city, address.state, address.zip)

    def __repr__(self):
        return "<Location: id=%r, name=%r>" % (self.id, self.name)


class Address(Base):
    __tablename__ = 'address'

    id = Column(Integer, primary_key=True)
    name = Column(Text, nullable=False)
    street = Column(Text, nullable=False)
    city = Column(Text, nullable=False)
    state = Column(Text, nullable=False)
    zip = Column(Text(20), nullable=False)

    location = relationship('Location', back_populates='address')

    def update(self, name=None, street=None, city=None, state=None, zip=None):
        if name:
            self.name = name
        if street:
            self.street = street
        if city:
            self.city = city
        if state:
            self.state = state
        if zip:
            self.zip = zip

    def to_dict(self):
        return dict(
            name=self.name,
            street=self.street,
            city=self.city,
            state=self.state,
            zip=self.zip
        )

    def __init__(self, name, street, city, state, zip):
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.zip = zip

    def __repr__(self):
        return "<Address: id=%r>" % self.address_id


class Image(Base):
    __tablename__ = 'image'

    id = Column(Integer, primary_key=True)
    uuid = Column(Text, unique=True, nullable=False)
    description = Column(Text)
    path = Column(Text)
    mimetype = Column(String)
    owner_member_id = Column(Integer, ForeignKey('member.id', ondelete='CASCADE'), nullable=False)
    owner_member = relationship('Member', back_populates='images')

    events = relationship('Event', secondary=t_event_image_gallery, back_populates='images')

    def to_dict(self):
        return dict(
            id=self.id,
            uuid=self.uuid,
            description=self.description,
            url="/v1/image/"+self.uuid
        )

    def __init__(self, owner_member_id, uuid, path, mimetype, description):
        self.owner_member_id = owner_member_id
        self.uuid = uuid
        self.path = path
        self.mimetype = mimetype
        self.description = description

    def __repr__(self):
        return '<Image: id=%r, uuid=%r>' % (self.id, self.uuid)
