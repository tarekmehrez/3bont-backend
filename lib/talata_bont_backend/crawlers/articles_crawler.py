"""Contains the ArticleCrawler class as part of the crawler package"""

import requests
import urlparse
import eatiht

from goose import Goose
from bs4 import BeautifulSoup
from datetime import datetime

from talata_bont_backend.util import log

log.init_logger()
logger = log.get_logger()

class ArticlesCrawler:
    """Crawl a given url and get all articles in this url."""


    def __init__(self):
        """Initialize ArticleCrawler class and its vars."""
        logger.info('initalizing, seems ok')

        self._goose = Goose()

    def fetch(self, domain, url, div_attr):
        logger.info('fetching articles for: %s', url)

        response = requests.get(url)
        content = response.content
        parser = BeautifulSoup(content,'lxml')
        articles_links = parser.find("div",attrs=div_attr).find_all('a')
        response.close()

        logger.info('total links found %d', len(articles_links))
        failed = 0
        for link in articles_links:
            href = link.attrs.get("href")


            if not self._is_absolute_url(href):
                href = domain + '/' + href

            # try:
            self._parse_article(href.encode('utf8'))
            logger.debug('fetched %s', href)

            # except:
            #     failed += 1
            #     print 'error fetching %s' % href

        logger.info('total successful fetches: %d out of %d' % (len(articles_links) - failed, len(articles_links)))

    def _is_absolute_url(self, url):
        return bool(urlparse.urlparse(url).netloc)

    def _parse_article(self, url):

        article = self._goose.extract(url=url)
        article_dict = article.opengraph
        article_dict['domain'] = article.domain
        article_dict['title'] = article.title
        article_dict['date'] = article.publish_date
        article_dict['text'] = article.cleaned_text

        if not article_dict['text']:
            try:
                alternative_text = eatiht.extract(url)
                article_dict['text'] = alternative_text
            except:
                logger.debug('couldnt parse texti in %s', url)


        if not (article_dict['title'] or article_dict['text']):
            return

        logger.debug(self._clean_dict(article_dict))

        # TODO: dump in db
    def _clean_dict(self, article_dict):
        try:
            if article_dict['date'] == None:
                article_dict['date'] = str(datetime.now())

            for key in article_dict:
                article_dict[key] = str(article_dict[key]).strip().encode('utf8')

            return article_dict

        except:
            logger.debug('failed cleaning dict')
            return article_dict


