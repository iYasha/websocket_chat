FROM python:3.7

RUN apt-get update && apt-get install -y libpq-dev gcc python3-dev musl-dev

ADD . /code
WORKDIR /code

RUN pip install -r /code/requirements.txt

CMD python main.py
