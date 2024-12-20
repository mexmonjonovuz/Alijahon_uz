FROM python:3.11-slim

WORKDIR /app
COPY  . /app

#RUN #pip3 install -r requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

#RUN pip install --upgrade pip
#RUN --mount=type=cache,id=custom-pip,target=/root/.cache/pip pip install -r requirements.txt

CMD ["python3", "manage.py", "runserver", "0:8000"]