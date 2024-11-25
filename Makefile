.phony: test

run:
	@echo "Running the application..."
	@python package.py

test:
	@echo "Running tests..."
	@pytest .
