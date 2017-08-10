FROM python:3

WORKDIR /app

ADD . /app

RUN pip install -r requirements.txt

EXPOSE 4200

ENTRYPOINT ["python", "update_calendar.py"]
