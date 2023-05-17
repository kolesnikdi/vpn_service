#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT;
  do
    echo "Attempt to connect DB"
    sleep 0.1
  done

echo "PostgreSQL started"
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
python manage.py shell -c "from registration.models import WebMenuUser; WebMenuUser.objects.create_superuser('segareta@ukr.net', 'segareta@ukr.net')"
# python manage.py runserver 0.0.0.0:8000  --noreload # comand that stops reloading

exec "$@"
