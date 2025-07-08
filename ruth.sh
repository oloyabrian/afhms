#!/bin/bash
cd ~/Desktop/Projects/ruth_app/afhms || exit
source venv/bin/activate
nohup python manage.py runserver &
echo "Server started. Access it at http://localhost:8000"