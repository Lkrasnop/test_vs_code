venv:
	python3 -m venv venv
			# source venv/bin/activate   # On macOS and Linux

install:		
	pip install --upgrade pip &&\
	pip install -r requirements.txt

run:	install
	python3 tes.py

remove:
	rm -rf venv
		# deactivate


#add notes for upload to git

#step 1 : git add . 

#step 2 :  git commit -m "update makefile - update  venv"

#step 3 : git branch --M main         

#step 4 : git remote add origin https://github.com/Lkrasnop/test_vs_code.git

#step 5 : git push -u origin main 

git:
	git add . &&\
	git commit -m "update makefile - update  venv" &&\
	git branch --M main &&\
	git remote add origin https://github.com/Lkrasnop/test_vs_code.git &&\
	git push -u origin main

gits:
	git add . &&\
	git commit -m "update makefile - update venv new now" &&\
	git branch --move main &&\
	git remote add origin https://github.com/Lkrasnop/test_vs_code.git &&\
	git push -u origin main


