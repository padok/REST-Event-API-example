# RESTful Event API Server

This is a webservice providing a RESTful API to provide your own Event service.


## Overview
This server was generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project. By using the
[OpenAPI-Spec](https://github.com/swagger-api/swagger-core/wiki) from a remote server, you can easily generate a server stub.  This
is an example of building a swagger-enabled Flask server.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

## Requirements
Python 3.5.2+

### Project Dependencies

* [SQLAlchemy](https://www.sqlalchemy.org/) - an object relational mapper (v1.2.7)
* [Python](https://docs.python.org/2/) - programming language (v3.6.5)
* [Swagger](https://swagger.io/) - API developer tools (v2.2)
* [Connexion](https://connexion.readthedocs.io/) - Swagger framework for python-flask


## Usage
To run the server, please execute the following from the root directory:

```
pip3 install -r requirements.txt
python3 -m swagger_server
```

and open your browser to here:

```
http://localhost:8080/v1/ui/
```

Your Swagger definition lives here:

```
http://localhost:8080/v1/swagger.json
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```

## Running with Docker

To run the server on a Docker container, please execute the following from the root directory:

```bash
# building the image
docker build -t swagger_server .

# starting up a container
docker run -p 8080:8080 swagger_server

# starting up a container with persistent storage
docker run -v "$(pwd)"/data:/usr/src/app/data -p 8080:8080 swagger_server
```

## Deployment

Due to security reasons its suggested to use nginx as proxy for the api. An example configuration of nginx could be
```
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    server_name SET_YOUR_URL_HERE;

    location /nginx_status {
        stub_status on;
        access_log off;
        allow 127.0.0.1;
        deny all;
    }

    location / {
        # to prevent any request other than to the API
        return 404
    }

    location @413_json {
        default_type application/json;
        return 413 '{"title":"Request Entity Too Large", "status": 413, "detail":"The uploaded file is $
    }

    location /v1 {
        # Disallow any http method that is not supported by the API
        if ($request_method !~ ^(GET|POST|DELETE|PUT)$ )
        {
                return 444;
        }

        # Define the location of the proxy server to send the request to
        # 172.17.0.2:8080 - example url and port on the local server (Docker container)
        proxy_pass http://172.17.0.2:8080/v1;
    
        # Redefine the header fields that NGINX sends to the upstream server
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    
        # Set error page for 413 Request Entity Too Large
        error_page 413 @413_json;

        # Define the maximum file size on file uploads
        client_max_body_size 5M;
    }
}
```

and then run the api on the server with docker
```
# Download the source code
git clone GITURL --single-branch
cd SOURCE
# Remove running server with the same name
docker rm $(docker stop $(docker ps -a -q --filter ancestor=swagger_server --format="{{.ID}}"))
# Build the docker container
docker build -t swagger_server .
# run the docker container
docker run -d -v "$(pwd)"/data:/usr/src/app/data swagger_server

```
the proxy url in the nginx config that leads to the docker server may have to be adjusted