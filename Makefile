test:
	py.test tests
run:
	foreman start
lint:
	flake8 . --exclude=node_modules --ignore=E501,F403
