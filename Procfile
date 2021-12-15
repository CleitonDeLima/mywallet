release: python manage.py migrate
web: gunicorn mywallet.wsgi --workers 3 --max-requests 100 --timeout 60
