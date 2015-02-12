test:
	nosetests

run:
	gunicorn server:app
