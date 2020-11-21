#!/bin/bash

export DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE:-deploy_django_project.settings.local}

exec poetry run python3 manage.py "$@"
