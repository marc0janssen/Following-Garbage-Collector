# Name: Follow_Garbage_Collector
# Coder: Marco Janssen (twitter @marc0janssen)
# date: 2021-04-19
# update: 2021-11-21 11:55:31

# Importing the modules
from twython import Twython, TwythonError
from chump import Application
from datetime import datetime
from time import time, sleep
import logging
import configparser
import shutil
import sys


class Follow_Garbage_Collector():
    def __init__(self):

        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        self.config_file = "/config/Follow_Garbage_Collector.ini"

        try:
            with open(self.config_file, "r") as f:
                f.close()
            try:
                self.config = configparser.ConfigParser()
                self.config.read(self.config_file)

                self.twitter_app_key = self.config['TWITTER']['APP_KEY']
                self.twitter_app_secret = self.config['TWITTER']['APP_SECRET']
                self.twitter_oauth_token = \
                    self.config['TWITTER']['OAUTH_TOKEN']
                self.twitter_oauth_token_secret = \
                    self.config['TWITTER']['OAUTH_TOKEN_SECRET']
                self.twitter_unfollow = True if (
                    self.config['TWITTER']['UNFOLLOW'] == "ON") else False
                self.twitter_years_inactive = \
                    int(self.config['TWITTER']['YEARS_INACTIVE'])
                self.twitter_excluded_tweeps = list(
                    self.config['TWITTER']['EXCLUDED_TWEEPS'].split(","))

                self.pushover_user_key = self.config['PUSHOVER']['USER_KEY']
                self.pushover_token_api = self.config['PUSHOVER']['TOKEN_API']
                self.pushover_sound = self.config['PUSHOVER']['SOUND']

            except KeyError:
                logging.error(
                    "Can't get keys from INI file. "
                    "Please check for mistakes."
                )

                sys.exit()

        except IOError or FileNotFoundError:
            logging.error(
                f"Can't open file {self.config_file}, "
                f"creating example INI file."
            )

            shutil.copyfile('/app/Follow_Garbage_Collector.ini.example',
                            '/config/Follow_Garbage_Collector.ini.example')
            sys.exit()

    # Convert UTC times to local times
    def datetime_from_utc_to_local(self, utc_datetime):
        now_timestamp = time()
        offset = datetime.fromtimestamp(
            now_timestamp) - datetime.utcfromtimestamp(
            now_timestamp)
        return utc_datetime + offset

    # convert a tweetdatetime to datetime_utc
    def tweetdatetime_to_datetime_utc(self, tweetDate):

        return self.datetime_from_utc_to_local(
            datetime.strptime(tweetDate, "%a %b %d %H:%M:%S +0000 %Y"))

    def run(self):

        # Log a run
        logging.info(
            "Executing Follow Garbage Collector."
        )

        # Setting for PushOver
        self.appPushover = Application(self.pushover_token_api)
        self.userPushover = self.appPushover.get_user(self.pushover_user_key)

        try:
            # This time we want to set our q to search for our keywords
            self.twitter = Twython(
                self.twitter_app_key,
                self.twitter_app_secret,
                self.twitter_oauth_token,
                self.twitter_oauth_token_secret,
            )

            friends = self.twitter.get_friends_ids()

            for friend in friends["ids"]:

                user_timeline = self.twitter.get_user_timeline(
                    user_id=friend, count=1)

                for tweet in user_timeline:

                    diffDate = datetime.now() - \
                        self.datetime_from_utc_to_local(
                            self.tweetdatetime_to_datetime_utc(
                                tweet["created_at"]))

                    if diffDate.days >= 365 * self.twitter_years_inactive:

                        tweetDate = datetime.strftime(
                            self.datetime_from_utc_to_local(
                                self.tweetdatetime_to_datetime_utc(
                                    tweet["created_at"])), "%Y-%m-%d %H:%M:%S",
                        )

                        if (not tweet["user"]["screen_name"] in
                                self.twitter_excluded_tweeps):

                            if self.twitter_unfollow:
                                self.twitter.destroy_friendship(user_id=friend)

                            self.message = self.userPushover.send_message(
                                message=f'Flushed @'
                                f'{tweet["user"]["screen_name"]} '
                                f'- {tweet["user"]["name"]}\n{tweetDate}\n'
                                f'{tweet["text"]}', sound=self.pushover_sound
                            )

                            # Log a flush
                            logging.info(
                                f'Flushed @'
                                f'{tweet["user"]["screen_name"]} '
                                f'- {tweet["user"]["name"]} - {tweetDate}'
                            )

                    # trying not to upset the Twitter Gods
                    sleep(2)

        except TwythonError as e:
            print(e)


if __name__ == '__main__':

    FGC = Follow_Garbage_Collector()
    FGC.run()
    FGC = None
