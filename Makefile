mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

compile:
	django-admin compilemessages --ignore=.venv

dumpdata:
	python3 manage.py dumpdata --indent=2 apps.shop.Product > product.json

loaddata:
	python3 manage.py loaddata categories

