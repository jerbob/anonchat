# AnonChat [![Build Status](https://travis-ci.com/AnonGuy/technical-test.svg?branch=master)](https://travis-ci.com/AnonGuy/technical-test)

A website for creating anonymous, ephemeral chatrooms.

## Development

To run the site locally, clone the repo and run:

```sh
$ docker-compose -f development.yml up -d
```

## Deployment
The site's docker container is on [Docker Hub](https://hub.docker.com/repository/docker/aperture/anonchat), so the only file you'll need is [docker-compose.yml](https://raw.githubusercontent.com/AnonGuy/technical-test/master/docker-compose.yml). <br>
You'll need to create an `.env` file in the same directory as `docker-compose.yml`. Set the following variables:
```sh
STATIC_ROOT=static
SECRET_KEY=...

SQL_PORT=5432
SQL_USER=postgres
SQL_HOST=database
SQL_DATABASE=postgres
POSTGRES_HOST_AUTH_METHOD=trust

DJANGO_SETTINGS_MODULE=anonchat.settings
```
Bring the containers up with:
```sh
$ docker-compose up -d
```
Then run migrations:
```
$ docker-compose exec site anonchat/manage.py makemigrations
$ docker-compose exec site anonchat/manage.py migrate
```
To manage Messages and Rooms in the Django admin interface, create a superuser:
```
$ docker-compose exec site anonchat/manage.py createsuperuser
```
Then add the appropriate configuration for your preferred reverse proxy. For example, with nginx:
```nginx
server {
    listen 80;
    server_name anonchat.jeremiahboby.me;

    location / {
        proxy_set_header Upgrade $http_upgrade;
        proxy_pass http://localhost:8000;
    }
}
```
