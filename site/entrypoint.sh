#!/usr/bin/dumb-init /bin/sh


if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

cd /usr/src/app/anonchat

python manage.py collectstatic --no-input

if [ $DEBUG ]
then
  python manage.py makemigrations --no-input
  python manage.py migrate --no-input
  python manage.py createsuperuser --no-input
fi

exec "$@"
