import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import requests


def get_cnn_articles(num_articles: int, topic: str, dir_name: str):
    full_dir_path = f'{dir_name}/{topic}'
    if not os.path.isdir(full_dir_path):
        os.mkdir(full_dir_path)

    browser = webdriver.Chrome()  # initialize selenium Chrome browser object
    time.sleep(3)

    n = 0
    starting_article_num = 0
    while n < num_articles:
        # CNN only displays 50 articles per page. I have to get article links in intervals of 50.
        URL = f'https://www.cnn.com/search?q={topic}&size=50&from={starting_article_num}&page='
        browser.get(URL)
        articles = browser.find_elements_by_class_name('cnn-search__result-headline')
        for article in articles:
            link = article.find_element_by_tag_name('a').get_attribute('href')
            if 'index.html' in link:
                try:
                    with open(f'{full_dir_path}/article{n}.txt', 'w') as f:
                        f.write(get_cnn_content(link))
                    n += 1
                    if n == num_articles:
                        break
                except Exception as e:
                    print(e)
                    print(f'CNN Error: Unable to read or write {link}')
                    print()

            starting_article_num += 1

    browser.close()


def get_cnn_content(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    header = soup.find(class_='pg-headline').text.strip()
    paragraph_containers = soup.find_all(class_='zn-body__paragraph')
    paragraphs = [para.text for para in paragraph_containers]
    paragraphs = ' '.join(paragraphs).strip(' (CNN)')
    content = f'{header}\n{paragraphs}'

    return content


