install:
	sudo apt-get install python3-tk python3-dev
	sudo apt-get install tk-dev
	pipenv install --dev

test:
	pipenv run pytest