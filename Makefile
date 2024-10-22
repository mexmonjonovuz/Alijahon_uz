mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

compile:
	python3 manage.py compilemessages --ignore=.venv --locale=uz

makemessage:
	python3 manage.py makemessages -l ru -l uz -l oz

dumpdata:
	python3 manage.py dumpdata --indent=2 apps.shop.Product > product.json

loaddata:
	python3 manage.py loaddata categories

