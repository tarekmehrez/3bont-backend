"""
Contains the CrawlersWrapper class as part of the crawler package.
"""
import os

from articles_crawler import ArticlesCrawler
from instagram_crawler import InstagramCrawler
from twitter_crawler import TwitterCrawler

from talata_bont_backend.util import IO, log
from talata_bont_backend.db import MongoInterface

log.init_logger()
logger = log.get_logger()


class CrawlersWrapper(object):

    """
    Runs all crawlers.
    """

    def __init__(self, host, port, db_name):
        """
        Init crawlers wrapper.

        Args [Mongo db related]:
            host (str)
            port (str)
            db_name (str)
        """
        self.io = IO()

        self._db_interface = MongoInterface(host, port, db_name)

    def crawl_articles(self, urls_file):
        """
        Run articles crawlers.

        Args:
            urls_file (str): csv file with all urls to crawl
        """
        logger.info("Crawling artilces in %s", urls_file)
        news_sources = self.io.read(urls_file)
        crawler = ArticlesCrawler(self._db_interface)

        for news_source in news_sources:
            logger.info('Crwaling News Source: %s', news_source['src'])

            starting_page = int(news_source['starting_page'])
            ending_page = int(news_source['ending_page'])

            try:
                if starting_page == -1 or ending_page == -1:
                    crawler.run(2,
                                news_source['src'],
                                news_source['domain'],
                                news_source['url'],
                                news_source['tag'],
                                {news_source['attr']:
                                 news_source['value']})

                else:
                    for page in xrange(starting_page, ending_page + 1):
                        crawler.run(2,
                                    news_source['src'],
                                    news_source['domain'],
                                    news_source['url'].replace(
                                        '$', str(page)),
                                    news_source['tag'],
                                    {news_source['attr']:
                                     news_source['value']})
            except:
                logger.error("%s CRASHED", news_source['src'])
                continue

    def crawl_instagram(
            self,
            access_token,
            client_secret,
            users_txt,
            users_json):
        """
        Run instagram crawler.

        Args:
            access_token (str): instagram api access token
            client_secret (str): instagram api secret client
            users_txt (str): txt file with usernames
            user_jsons (str): json file with usernames, ids and user prof pics
        """
        crawler = InstagramCrawler(
            access_token, client_secret, self._db_interface)

        if os.path.exists(users_json):
            logger.info('instagram IDs found')
            users_dict = self.io.read(users_json)

        else:
            logger.info('instagram IDs not found')
            accounts_list = self.io.read(users_txt)
            users_dict = crawler.fetch_ids(accounts_list)

            self.io.write(users_json, users_dict)

        crawler.run(users_dict)

    def crawl_twitter(self,
                      consumer_key,
                      consumer_secret,
                      access_token,
                      access_token_secret,
                      users_txt):
        """
        Run twitter crawler.

        Args:
          consumer_key (str)
          consumer_secret (str)
          access_token (str)
          access_token_secret (str)
          users_txt (str)
        """
        crawler = TwitterCrawler(consumer_key,
                                 consumer_secret,
                                 access_token,
                                 access_token_secret,
                                 self._db_interface)

        accounts_list = self.io.read(users_txt)

        crawler.run(accounts_list)
