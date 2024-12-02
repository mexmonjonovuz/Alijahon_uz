FROM python:3.12-alpine

WORKDIR app/
COPY . /app

RUN echo "Success"

RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["python3","manage.py","8000"]