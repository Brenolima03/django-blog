#!/bin/sh
makemigrations.sh
echo 'Executing migrate.sh'
python manage.py migrate --noinput
