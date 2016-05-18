"""
Contains the TwitterCrawler class as part of the crawler package.
"""
import tweepy
from talata_bont_backend.util import log

log.init_logger()
logger = log.get_logger()


class TwitterCrawler(object):

    """
    Crawl data in mentioned twitter accounts.
    """

    def __init__(self,
                 consumer_key,
                 consumer_secret,
                 access_token,
                 access_token_secret,
                 db_interface):
        """
        Init twitter api.

        Args:
            consumer_key (str) [Twitter API]
            consumer_secret (str) [Twitter API]
            access_token (str)  [Twitter API]
            access_token_secret (str)  [Twitter API]
            db_interface (MongoInterface)

        """
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)

        self._api = tweepy.API(auth)

        self._db_interface = db_interface

    def run(self, accounts):
        """
        Run crawler for twitter accounts.
        """
        for account in accounts:
            logger.info("Retrieving data for " + str(account))
            try:
                tweets = self._api.user_timeline(account)
            except:
                logger.error("%s does not exist as an account", str(account))
                continue

            self._parse_tweets_for_account(account, tweets)

    def _parse_tweets_for_account(self, account, tweets):
        """
        Given a twitter account, get his latest tweets.

        Args:
            account (twitter API obj)
            tweets (list[twitter API obj])

        Return:
            list[dict]: parsed tweets
        """
        for tweet in tweets:

            curr_item = {}
            curr_item['lang'] = tweet.lang
            curr_item['text'] = tweet.text
            curr_item['account'] = tweet.user.name
            curr_item['account_image'] = tweet.user.profile_image_url

            curr_item['tags'] = []
            if len(tweet.entities['hashtags']) > 0:

                for tag in tweet.entities['hashtags']:
                    curr_item['tags'].append(tag['text'])

            curr_item['date'] = tweet.created_at

            curr_item[
                'url'] = "https://twitter.com/%s/status/%s", (str(tweet.user.
                                                                  screen_name),
                                                              str(tweet.id))

            curr_item['media_url'] = None
            if 'media' in tweet.entities:
                curr_item['media_url'] = tweet.entities[
                    'media'][0]['media_url_https']

            curr_item['retweets'] = tweet.retweet_count
            curr_item['favs'] = tweet.favorite_count
            curr_item['tweet_id'] = tweet.id

            curr_item['type'] = 'social_media'
            curr_item['src'] = 'twitter'

            self._db_interface.insert_one('tweets', curr_item)
            self._db_interface.insert_one('timeline_items', curr_item)
