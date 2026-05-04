#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.prod}"

pip install -r requirements.txt

python manage.py migrate --noinput

python manage.py import_instalaciones
python manage.py import_mantenciones
python manage.py import_clientes
python manage.py fill_metadata --set-featured --clear-featured-non-segmented
python manage.py clean_mixed_projects

python manage.py collectstatic --noinput
