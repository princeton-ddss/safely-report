#!/bin/sh

# Synchronize database schema
flask db upgrade

# Launch application
exec gunicorn --bind 0.0.0.0:80 "app:app"
