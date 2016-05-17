#!/usr/bin/python
import config

from talata_bont_backend.crawlers import CrawlersWrapper


def main():
    config_dict = config.get_config_dict()
    twitter_args = config_dict['twitter']

    crawler = CrawlersWrapper()
    crawler.crawl_twitter(

        consumer_key=twitter_args['consumer_key'],
        consumer_secret=twitter_args['consumer_secret'],

        access_token=twitter_args['access_token'],

        access_token_secret=twitter_args['access_token_secret'],
        users_txt=twitter_args['accounts_txt_file'])

if __name__ == "__main__":
    main()
