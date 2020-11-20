# Twitter Slackbot

Note: This is a prototype and use with caution or at your own risk. 

## Introduction

This repo contains the work of the team DataMasters in developing a Twitter Slackbot as a part of the Professional Development competition at Cybera. The work is aimed at streaming near real-time tweets from Twitter focusing on COVID-19 in Alberta. The streamed tweets are then sent as Slack message updates using a Slack bot. There are two components to this bot.

### Twitter Component

Apply for a developer account at [Twitter](https://developer.twitter.com/en/apply-for-access). You will have to submit an application stating the need and the intent for using the Twitter APIs.

After successfully setting up the Twitter developer account, create a new project with `Read only` permission to read the tweets from Twitter using API v2. The Bearer token and other credentials with Twitter APIs can be found here. 

### Slack Component

Generate a Slack App, `your-app-name`, by following the detailed instructions provided in the link [here](https://slack.com/intl/en-ca/help/articles/115005265703-Create-a-bot-for-your-workspace).  

In `oAuth & Permissions` tab, add `chat:write` and `app_mentions:read` to give relevant permissions to the app. 

Go ahead and then click `Install to Workspace` to successfully set it up in your workspace. You would find the `User OAuth Token` and `Signing Secret` for the app here.  

The Twitter Slackbot is developed and tested leveraging our [Rapid Access Cloud](https://www.cybera.ca/rapid-access-cloud/) with Ubuntu 20.04. The only requirement to run this script successfully is to have the latest version of `docker-ce` and `docker-compose` installed on your server.

## Set-up

In your Slack Workspace, add the `your-app-name` app to the `#your-slack-channel-name` channel. 

Then, set the access tokens for Twitter and Slack APIS including the Slack Channel name that the bot is part of using the terminal. 

```bash
cd twitter_slack_bot
export TWITTER_TOKEN=<twitter-access-token>
export SLACK_BOT_TOKEN=<slack-access-token>
export SLACK_SIGNING_SECRET=<slack-signing-secret>
export SLACK_CHANNEL_NAME=<your-slack-channel-name>
```

To initialize and run the Twitter Slackbot, run the following command

```bash
docker-compose up --build -d
```

## Interacting with the bot

In Slack API portal of `your-app-name`, go to the `Event Subscriptions` Tab and turn on `Enable Events`. Please provide the follwing url to activate event subscriptions: 

```bash
http://<dns-remote-server>:3297/slack/events 
```

If the Docker is running successfully, the above URL will be verified. Under `Subscribe to bot events`, add `app_mention` as the `Event name`, 

If you have set up the correct credentials for the Twitter Slackbot, you would start seeing the messages in `#your-slack-channel-name` channel in Slack as and when there is a new tweet. 

If you wish to view or add the queries sent to Twitter, you can send the queries as the Slack message.  

```bash
@your-app-name HELP
```
Gives the list of commands available. 

```bash
@your-app-name SHOW ALL
```
Outputs the list of all existing queries. 

```bash
@your-app-name from:<new-twitter-username> keyword-1 or keyword-2 or keyword-3
```
Adds a new query with keywords. 
