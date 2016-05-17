"""
Contains the ArticleCrawler class as part of the crawler package.
"""
import requests
import urlparse
import eatiht

from goose import Goose
from bs4 import BeautifulSoup
from datetime import datetime

from talata_bont_backend.util import log


log.init_logger()
logger = log.get_logger()


class ArticlesCrawler(object):

    """
    Crawl a given url and get all articles in this url.
    """

    def run(self, articles_limit, *current_url_args):
        """
        Crawl and parse articles in the given url.

        Args:
            articles_limit (int): limit to get articles per page

            current_url_args (tuple):
            (
                domain (str): news sources' domain

                url (str): url to the page listing articles

                div_attr: div id or class cotaining articles,
                to parse and get all links in it
            )

        """
        domain, url, tag, attr_val_dict = current_url_args
        logger.info('fetching articles for: %s', url)

        articles_links = self._get_links(domain, url, tag, attr_val_dict)
        logger.info('total links found %d', len(articles_links))

        if articles_limit:
            articles_links = articles_links[:articles_limit]

        parsed_articles = []
        for link in articles_links:

            logger.info('fetching %s', link)
            parsed_articles.append(self._fetch_article(link))

        return parsed_articles

    def _get_links(self, *current_url_args):
        """
        Get articles parsed from the passed div.

        Args:
            see self.fetch_url

        Returns:
            list (str): links of articles to parse and crawl
        """
        domain, url, tag, attr_val_dict = current_url_args

        response = requests.get(url)
        content = response.content
        parser = BeautifulSoup(content, 'lxml')
        raw_links = parser.find(tag, attrs=attr_val_dict).find_all('a')
        response.close()

        article_links = []
        for link in raw_links:
            href = link.attrs.get("href")

            if not href:
                continue

            # if it's not absolute, prepend the domain
            if not self._is_absolute_url(href):
                href = '%s/%s' % (domain, href)

            article_links.append(href.encode('utf8'))

        # remove duplicates
        article_links = list(set(article_links))

        return article_links

    def _is_absolute_url(self, url):
        """
        Check if url is absolute.

        Args:
            url (str): url of the article

        Retruns:
            bool: whether its absolute, or relative
        """
        return bool(urlparse.urlparse(url).netloc)

    def _fetch_article(self, url):
        """
        Fetch the article, clean it.

        Args:
            url (str): url of the article
        """
        aricle = self._parse_article(url)

        if not aricle['text']:

            try:
                alternative_text = eatiht.extract(url)
                aricle['text'] = alternative_text

            except:
                logger.info('%s dropped', url)
                return

        if not (aricle['title'] or aricle['text']):
            logger.info('%s dropped', url)
            return

        aricle = self._clean_dict(aricle)

        return aricle

        # TODO: dump in db

    def _parse_article(self, url):
        """
        Parse the passed article using goose.

        Args:
            url (str): url of the article

        Returns:
            dict: article's passed content
        """
        goose = Goose()
        article = goose.extract(url=url)

        article_dict = article.opengraph
        article_dict['domain'] = article.domain
        article_dict['title'] = article.title
        article_dict['date'] = article.publish_date
        article_dict['text'] = article.cleaned_text

        return article_dict

    def _clean_dict(self, article_dict):
        """
        Clean dict of the artcile.

        - Check if data is none, and add now's date
        - strip and encode all parsed text to utf8

        Args:
            article_dict (dict): article's parsed dict

        Returned:
            dict: cleaned article dict
        """
        try:

            if article_dict['date'] is None:
                article_dict['date'] = str(datetime.now())

            for key in article_dict:
                article_dict[key] = article_dict[key].strip()

            return article_dict

        except:
            return article_dict
