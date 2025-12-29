web: gunicorn shorelux.wsgi:application --timeout 120 --workers 1
worker: celery -A shorelux worker -l info
beat: celery -A shorelux beat -l info