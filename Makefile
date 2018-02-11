TEST_PATH=./

lint:
	flake8

test:
	py.test --verbose --color=yes $(TEST_PATH)
