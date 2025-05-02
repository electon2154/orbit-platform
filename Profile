web: gunicorn orbit-platform.wsgi --log-file -
web: python manage.py migrate && gunicorn orbit-platform.wsgi
