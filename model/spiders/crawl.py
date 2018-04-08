# python 3

import json
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request


# Crawlers are forbidden. Use this header to bypass
HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
ARTICLE_LOCATION = '../articles/'

def parse_coindesk_search_results(host_name, url, page_count):
    '''
    The scrape method for Coindesk.
    It will output the text of an article to month_day_year__hour_minute.txt
    One file for each article
    '''
    print('searching page {}'.format(page_count))
    suffix = 'page/{}/?s=+'.format(page_count)
    print('url is {}'.format(url+suffix))
    try:
        # Get pretty html
        req = Request(url=url + suffix, headers=HEADERS)
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        articlesDiv = soup.select_one('body #content')
        articles = articlesDiv.find_all('div', class_='article')

        # Don't do it recursively
        # if len(articles) > 0 and not page_count > page_limit:
        #     parse_coindesk_search_results(host_name, url, page_count+1, page_limit)

        # Get the URL of an article, and pass it to the parser
        for article in articles:
            div = article.select_one('.post-info')
            h = div.select_one('h3')
            a = h.select_one('a')
            title = a.get_text()
            href = a['href']
            parse_article(href)
    except Exception as ex:
        print(ex)

def parse_article(url):
    '''
    Given an url, get the date and time
    Write article to txt file, where the date is the name and article is just populated as text
    '''
    try:
        req = Request(url=url, headers=HEADERS)
        html = urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')

        # Get the time of article
        articleTop = soup.find('div', class_='article-top')
        time = articleTop.find('span', class_='article-container-left-timestamp')
        parsedTime = time.text[:time.text.find('UTC')]
        parsedTime = parsedTime.strip()
        parsedTime = parsedTime.replace(',', '')
        parsedTime = parsedTime.replace('at', '')
        parsedTime = parsedTime.replace(':', '_')
        parsedTime = parsedTime.replace(' ', '_')
        print(parsedTime)

        # Scrape paragraphs from article
        articleContainer = soup.find('div', class_='article-container')
        articleContentContainer = articleContainer.find('div', class_='article-content-container noskimwords')

        # Save paragraphs to an array
        results = []
        paragraphs = articleContentContainer.select('p')
        for p in paragraphs:
            results.append(p.text)

        # write to a text file
        write_article_to_file(parsedTime+'.txt', results)
    except Exception as ex:
        print(ex)

def write_article_to_file(title, paragraphs):
    if not os.path.exists(ARTICLE_LOCATION):
        os.makedirs(ARTICLE_LOCATION)
    fileLocation = '{}{}'.format(ARTICLE_LOCATION, title)
    with open(fileLocation, 'w+', encoding='UTF-8', newline='') as article_file:
        article_file.writelines(paragraphs)
    print('Done writing {}'.format(title))

def main():
    visited_links = []
    base_urls = dict(coindesk='https://www.coindesk.com/')
    page_count = 1
    page_limit = 25

    for host_name, base_url in base_urls.items():
        for i in range(page_count, page_limit):
            parse_coindesk_search_results(host_name, base_url, i)
        visited_links.append(base_url)

if __name__ == '__main__':
    main()
