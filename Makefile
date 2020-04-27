test:
		coverage run -m unittest discover
		coverage report
		coverage html

citest:
		make test
		coverage xml
