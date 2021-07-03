python3 manage.py migrate;\
gunicorn pangpangeats.wsgi:application --bind 0.0.0.0:8000