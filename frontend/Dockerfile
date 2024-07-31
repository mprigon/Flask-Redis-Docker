FROM python:3.11.0-alpine

# set work directory
WORKDIR /flask-4

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies if any
RUN pip install --upgrade pip
COPY ./requirements.txt /flask-4
RUN pip install --upgrade pip -r requirements.txt

# install httpie for testing API purposes
RUN pip install --upgrade pip wheel
RUN pip install --upgrade httpie

# copy project
COPY . .

ENV FLASK_APP=flasky.py
ENV FLASK_RUN_HOST=0.0.0.0

EXPOSE "5000"

CMD flask --debug --app flasky run
