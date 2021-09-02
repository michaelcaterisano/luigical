FROM python:2

WORKDIR /app

ADD . /app

RUN pip install --upgrade google-api-python-client

RUN pip install -r requirements.txt

EXPOSE 4200

ENTRYPOINT ["python", "update_calendar.py"]
