import os

# SQLAlchemy settings
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/database.db'
SQLALCHEMY_DATABASE_ECHO = False

# Image storage settings
IMAGE_DATA_PATH = os.path.abspath("./data/images/")+"/"
ALLOWED_MIME_TYPES = ['image/jpeg', 'image/png']
