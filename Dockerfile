FROM python:3.12-alpine

WORKDIR /app

COPY . /app

RUN apk add --no-cache gcc musl-dev libffi-dev mariadb-connector-c-dev pkgconfig

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]