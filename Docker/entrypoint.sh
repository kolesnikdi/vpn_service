#!/bin/bash

echo "Waiting for postgres..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT;
  do
    echo "Attempt to connect DB"
    sleep 0.1
  done

echo "PostgreSQL started"
python manage.py migrate
echo "WEB: Migrations process done ..."
echo "\n"

echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "++                                                                                ++"
echo "++                    Hatred to russians still not enough!                        ++"
echo "++                                                                                ++"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
echo "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"

python manage.py runserver 0.0.0.0:8000
# python manage.py runserver 0.0.0.0:8000  --noreload # comand that stops reloading

exec "$@"
