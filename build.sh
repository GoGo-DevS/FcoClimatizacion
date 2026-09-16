#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE="${DJANGO_SETTINGS_MODULE:-config.settings.prod}"

pip install -r requirements.txt

python manage.py migrate --noinput

python manage.py import_instalaciones
python manage.py import_mantenciones
# clientes.zip NO se importa: son testimonios con la CARA de clientes reales y
# capturas de pantalla de Instagram. El portafolio muestra el trabajo (equipos,
# instalaciones, mantenciones), no a la gente. 16-09-2026.
python manage.py fill_metadata --set-featured --clear-featured-non-segmented
python manage.py clean_mixed_projects
python manage.py quitar_fotos_de_personas

python manage.py collectstatic --noinput
