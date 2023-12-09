venv:
	python3 -m venv .venv
			# source .venv/bin/activate   # On macOS and Linux

install:		
	pip install --upgrade pip &&\
	pip install -r requirements.txt

run:	install
	python3 tes.py

remove:
	rm -rf venv
		# deactivate
