.PHONY: clean
clean:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	@rm -rf .pytest_cache *.egg-info .coverage coverage.xml dist

.PHONY: test
test: clean
	poetry run pytest -s

.PHONY: cover
cover: clean
	poetry run pytest --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=logtron_aws tests
