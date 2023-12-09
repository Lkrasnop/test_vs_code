.venv:
	python3 -m venv .venv

install:	.venv	
	pip install -r requirements.txt

run:	install
	python3 tes.py