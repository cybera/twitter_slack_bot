FROM python:3.9

COPY requirements.txt /

RUN pip install -r /requirements.txt

COPY src/ /app

WORKDIR /app

CMD ["./run_twitter_slack_bot.py"]