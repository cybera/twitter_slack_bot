# DataMasters Twitter-Slack Bot

This repo contains the work of the team DataMasters over the month of November-2020 as a part of Professional Development Projects Month in Cybera. The work is aimed at 
streaming near real-time data tweets from Twitter focusing on COVID-19 in Alberta, and with further processing and cleaning, the tweets are sent as a Slack message updates using a Slack bot. 

To get started, you need to have access tokens for Twitter and Slack APIs, which can be generated following the links below: 
1. Apply for a developer account at [Twitter](https://developer.twitter.com/en/apply-for-access). You will have to submit an application stating the need and the intent for using the APIs while agreeing to Twitter's Terms and Conditions. 
2. Generate a Slack bot by following the link [here](https://slack.com/intl/en-ca/help/articles/115005265703-Create-a-bot-for-your-workspace).

Note: For more information listed in this repo, please visit our [presentation](https://docs.google.com/presentation/d/1UWX6lC1-SJixgiS5348sQ-yUetwYOQH4-mHiBwJsc2I/edit#slide=id.p) here. 

This repo is run and tested in Macbook Pro (16inch, 2016) Model. However, it should work equally good in Windows and other Linux servers. Make sure you have the latest version of `docker-ce` and `docker-compose` installed in your machine.

## Set-up

First, we need to set the access tokens for Slack and Twitter in the environment variables.

```bash
cd covid19ab_twitter_slack_bot
export BEARER_TOKEN_TWITTER=<twitter-access-token>
export BEARER_TOKEN_SLACK=<slack-access-token>
```

To initialize and run the Twitter and Slack apis, run the following command

```bash
docker-compose up --build twitter-slack-api
```

If you have setup the access tokens correctly, you would start seeing the messages in `#testing` channel in Slack. If you wish to change the queries sent to Twitter, you can modify them at `/access-apis/src/sample-queries.txt`  
