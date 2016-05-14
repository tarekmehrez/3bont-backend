#!/usr/bin/python
from talata_bont_backend.crawlers import ArticlesCrawler

def main():
    crawler = ArticlesCrawler()
    crawler.fetch('http://hihi2.com/','http://hihi2.com/category/football-news/page/1', {'id':'content-loop'})

if __name__ == "__main__":
	main()