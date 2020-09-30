.PHONY: clean
clean:
	@find . | grep -E "(__pycache__|\.pyc|\.pyo$$)" | xargs rm -rf
	@rm -rf .pytest_cache *.egg-info .coverage coverage.xml report.xml junit htmlcov dist

.PHONY: test
test: clean
	poetry run pytest --ignore=docs-src -s

.PHONY: ci
ci: clean
	poetry run pytest --ignore=docs-src --junitxml=report.xml

.PHONY: cover
cover: clean
	poetry run pytest  --ignore=docs-src --cov-config .coveragerc --verbose --cov-report term --cov-report xml --cov=logtron_aws tests

.PHONY: clean-docs
clean-docs:
	@rm -rf docs
	@mkdir -p docs

.PHONY: docs
docs: clean-docs
	@cd docs-src && npm run generate
	@cp -R docs-src/dist/* docs/

.PHONY: serve-docs
serve-docs:
	@cd docs-src && npm install
	@cd docs-src && npm run dev
