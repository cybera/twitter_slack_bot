import requests
import os
import json
import pandas as pd

from slack_bot import slackbot

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'


def auth():
    return os.environ.get("BEARER_TOKEN_TWITTER")


def create_url(query, last_tweet = None):
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    if (query):
        tweet_fields = "tweet.fields=author_id"
        if (last_tweet):
            since_id = "since_id=" + str(last_tweet)
            print("Accessing Last Tweet ",since_id)
            url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}".format(
                query, tweet_fields, since_id
            )
        else:
            print("Accessing Last 10 Tweets")
            url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
                query, tweet_fields
            )

    return url


def create_headers(bearer_token):
    headers = {"Authorization": "Bearer {}".format(bearer_token)}
    return headers


def connect_to_endpoint(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def main():
    # Access the bearer_token 
    bearer_token = auth()
    # Send in the query string and last tweet
    query = "from:CMOH_Alberta -is:retweet"
    since_id = 1329546200740110337

    url = create_url(query, last_tweet = since_id)
    headers = create_headers(bearer_token)
    json_response = connect_to_endpoint(url, headers)
    if (json_response):
        df_tweet = pd.json_normalize(json_response['data'])
        msg=df_tweet.loc[0,'text']
        #print(df_tweet.loc[0,'text'])
        slackbot(msg)
        #print(json.dumps(json_response["data"], indent=4, sort_keys=True))
    else:
        print("No Tweets exist")
    


if __name__ == "__main__":
    main()