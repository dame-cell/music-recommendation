install:

	pip install --upgrade pip
	pip install -r requirements.txt
	pip freeze requirements.txt 
	

test:
	#Add the testing command you want to run here
	pytest test\test_recommendation.py

 
deploy:
	# Add the deployment command you want to run here

all:
	@echo "Running all targets..."
	make install 
	make deploy
	make test
	@echo "All targets completed."