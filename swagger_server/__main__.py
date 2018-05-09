#!/usr/bin/env python3

import connexion
import logging

from swagger_server import encoder
from swagger_server.database import init_db, db_session


def main():
    app.run(port=8080)


logging.basicConfig(level=logging.INFO)
init_db()

app = connexion.App(__name__, specification_dir='./swagger/')
app.app.json_encoder = encoder.JSONEncoder
app.add_api('swagger.yaml', arguments={'title': 'P7 Renderservice'})

application = app.app


@application.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == '__main__':
    main()
