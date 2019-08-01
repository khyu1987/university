#!/bin/bash

echo '=============================================='
echo '====Installing application requirements...===='
echo '=============================================='
pip install -r requirements.txt

echo '=============================================='
echo '====Configuration database migrations...======'
echo '=============================================='
python manage.py migrate

echo '=============================================='
echo '===========Loading initial data...============'
echo '=============================================='
python manage.py loaddata fixtures.json

echo '=============================================='
echo '===============Running tests...==============='
echo '=============================================='
python manage.py test

echo '=============================================='
echo '===========Running local server...============'
echo '=============================================='
python manage.py runserver
