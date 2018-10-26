unittest:
	if [ -z ${report} ]; then py.test unit_tests; else py.test --junitxml=test-output/unit-test-output.xml --cov-report=html:test-output/unit-test-cov-report unit_tests; fi

run:
	python3 manage.py runserver

lint:
	flake8 ./

