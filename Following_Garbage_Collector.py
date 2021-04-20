# Name: Follow_Garbage_Collector
# Coder: Marco Janssen (twitter @marc0janssen)
# date: 2021-04-19
# update: 2021-04-20 17:24:10


# Importing the modules
from twython import Twython, TwythonError
from chump import Application
from datetime import datetime
from time import time, sleep
from Following_Garbage_Collector_settings import (twitter_app_key,
                                                  twitter_app_secret,
                                                  twitter_oauth_token,
                                                  twitter_oauth_token_secret,
                                                  pushover_user_key,
                                                  pushover_token_api,
                                                  excluded_tweeps)


# Variables
unfollow = False
years_inactive = 10


# Convert UTC times to local times
def datetime_from_utc_to_local(utc_datetime):
    now_timestamp = time()
    offset = datetime.fromtimestamp(
        now_timestamp) - datetime.utcfromtimestamp(now_timestamp)
    return utc_datetime + offset


# convert a tweetdatetime to datetime_utc
def tweetdatetime_to_datetime_utc(tweetDate):

    return datetime_from_utc_to_local(
        datetime.strptime(
            tweetDate, "%a %b %d %H:%M:%S +0000 %Y"
        )
    )


# Setting for PushOver
app = Application(pushover_token_api)
user = app.get_user(pushover_user_key)


try:
    # This time we want to set our q to search for our keywords
    twitter = Twython(twitter_app_key, twitter_app_secret,
                      twitter_oauth_token, twitter_oauth_token_secret)

    friends = twitter.get_friends_ids()

    for friend in friends["ids"]:

        user_timeline = twitter.get_user_timeline(user_id=friend, count=1)

        for tweet in user_timeline:

            diffDate = datetime.now() - datetime_from_utc_to_local(
                tweetdatetime_to_datetime_utc(tweet["created_at"]))

            if diffDate.days >= 365*years_inactive:

                tweetDate = datetime.strftime(
                    datetime_from_utc_to_local(
                        tweetdatetime_to_datetime_utc(tweet["created_at"])),
                    "%Y-%m-%d %H:%M:%S",
                )

                if not tweet["user"]["screen_name"] in excluded_tweeps:

                    if unfollow:
                        twitter.destroy_friendship(user_id=friend)

                    messagePushover = "@%s - %s\n%s\n%s" % (
                        tweet["user"]["screen_name"], tweet["user"]["name"],
                        tweetDate, tweet["text"])

                    message = user.send_message(messagePushover)

        # trying not to upset the Twitter Gods
        sleep(0.2)


except TwythonError as e:
    print(e)
