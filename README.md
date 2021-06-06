# Following Garbage Collector

## Clean out the people you are following when they have been inactive for a certain period of time

1. [Set up a developer account with Twitter](https://developer.twitter.com/en/portal/projects-and-apps)
2. Create your applicatie with Twitter
3. Set your app read/write (do this before before generating all the tokens)
4. Generate an API Key and Secret
5. Generate an Access Token and Secret
6. [Setup an account with Pushover](https://pushover.net)
7. Get your User Key
8. Create a new app
9. Get token api for the app
10. Create a directory "config" on the same level as "app" and create a Following_Garbage_Collector.ini file.

## Config

    [TWITTER]
    APP_KEY = xxxxxxxxxxxxxxx
    APP_SECRET = xxxxxxxxxxxxxxx
    OAUTH_TOKEN = xxxxxxxxxxxxxxx-xxxxxxxxxxxxxxx
    OAUTH_TOKEN_SECRET = xxxxxxxxxxxxxxx
    UNFOLLOW = OFF
    YEARS_INACTIVE = 10
    excluded_tweeps = xxxxxx,yyyyyyy

    [PUSHOVER]
    USER_KEY = xxxxxxxxxxxxxxx
    TOKEN_API = xxxxxxxxxxxxxxx

2021-05-06 14:27:38
