import requests


def create_url_recent_search(query, last_tweet=None):
    # Tweet fields are adjustable.
    # Options include:
    # attachments, author_id, context_annotations,
    # conversation_id, created_at, entities, geo, id,
    # in_reply_to_user_id, lang, non_public_metrics, organic_metrics,
    # possibly_sensitive, promoted_metrics, public_metrics, referenced_tweets,
    # source, text, and withheld
    if query:
        tweet_fields = "tweet.fields=created_at"
        expansion_field = "expansions=author_id,referenced_tweets.id"
        if last_tweet:
            since_id = "since_id=" + str(last_tweet)
            print("Accessing Last Tweet ", since_id)
            url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}&{}&{}".format(
                query, tweet_fields, expansion_field, since_id
            )
        else:
            print("Accessing Last 10 Tweets")
            url = "https://api.twitter.com/2/tweets/search/recent?query={}&{}".format(
                query, tweet_fields, expansion_field
            )

    return url


def connect_to_endpoint_recent_search(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    return response.json()


def create_url_user_lookup(usernames):
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    # usernames = "usernames=TwitterDev,TwitterAPI"
    user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def connect_to_endpoint_user_lookup(url, headers):
    response = requests.request("GET", url, headers=headers)
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()
