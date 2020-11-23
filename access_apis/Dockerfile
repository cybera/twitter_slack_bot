FROM python:3.9

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY src/ /app

WORKDIR /app

CMD ["./stream_tweets_to_slack.py"]