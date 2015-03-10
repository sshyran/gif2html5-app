web: gunicorn server:app --log-file=-
worker: celery worker --app=server.celery
