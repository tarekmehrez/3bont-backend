"""
Test if all crawlers are working as expected.
"""
import unittest

from talata_bont_backend.crawlers import ArticlesCrawler
from talata_bont_backend.util import IOLayer


class TestArticlesCrawler(unittest.TestCase):

    def test_article_crawler(self):
        urls_file = '/Users/tarekmehrez/talata_bont/data/urls.csv'
        news_sources = IOLayer().read(urls_file)

        crawler = ArticlesCrawler()

        print news_sources
        for news_source in news_sources:
            pages = int(news_source['pages'])

            if pages == -1:

                parsed_articles = crawler.fetch_url(4,
                                                    news_source['domain'],
                                                    news_source['url'],
                                                    {news_source['div_attr']:
                                                     news_source['div_value']})

                self.assertGreaterEqual(len(parsed_articles), 2)
            else:
                for page in xrange(1, 2):
                    parsed_articles = crawler.fetch_url(
                        5,
                        news_source['domain'],
                        news_source['url']. replace(
                            '$', str(page)),
                        {news_source['div_attr']: news_source['div_value']})

                self.assertGreaterEqual(len(parsed_articles), 2)

if __name__ == '__main__':
    unittest.main()
