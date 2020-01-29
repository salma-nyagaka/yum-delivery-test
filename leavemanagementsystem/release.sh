#!/usr/bin/env bash
python3 manage.py makemigrations authentication
python3 manage.py migrate authentication
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py loaddata leavemanagementsystem/apps/role/fixtures/role
python3 manage.py loaddata leavemanagementsystem/apps/authentication/fixtures/user
