web: gunicorn server:app --log-file=- --reload
worker: celery worker --app=server.celery --loglevel=DEBUG
