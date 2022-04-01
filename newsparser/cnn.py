import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
from bs4 import BeautifulSoup
import requests


def get_cnn_articles(num_articles: int, topic: str, dir_name: str):
    valid_topics = [
        'politics',
        'us',
        'world',
        'business',
        'opinion',
        'health',
        'entertainment',
        'style',
        'travel'
    ]
    topic = topic.lower()
    if topic not in valid_topics:
        print('Not a valid topic')
        return None

    if not os.path.isdir(dir_name):
        os.makedirs(dir_name)

    full_dir_path = f'{dir_name}/{topic}'
    if not os.path.isdir(full_dir_path):
        os.makedirs(full_dir_path)

    browser = webdriver.Chrome('/Users/Isaacbolo/chromedriver/chromedriver 3')  # initialize selenium Chrome browser object
    time.sleep(3)
    url = f'https://www.cnn.com/search?size=30&q=all&type=article&category={topic}'
    browser.get(url)

    wait = WebDriverWait(browser, 15)
    n = 0
    while n < num_articles:
        # article_container = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'cnn-search__results-list')))
        article_container = browser.find_element_by_class_name('cnn-search__results-list')
        # articles = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'cnn-search__result-headline')))
        articles = article_container.find_elements_by_class_name('cnn-search__result-headline')
        for article in articles:
            try:
                # link = wait.until(EC.presence_of_element_located((By.TAG_NAME, 'a'))).get_attribute('href')
                link = article.find_element_by_tag_name('a').get_attribute('href')
            except Exception as e:
                print(e)
                print('Could not get link. Moving to next link')
                continue
            if 'index.html' in link and '/live-news/' not in link and 'fast-facts' not in link:
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

        # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        next_page_button = browser.find_element_by_class_name('pagination-arrow.pagination-arrow-right.cnnSearchPageLink.text-active')
        try:
            next_page_button.click()
            time.sleep(2)
        except Exception as e:
            print(e)
            print('Unable to go to next page')
            browser.close()
            return

    browser.close()
    time.sleep(2)


def get_cnn_content(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    header = soup.find(class_='pg-headline').text.strip()
    paragraph_containers = soup.find_all(class_='zn-body__paragraph')
    paragraphs = [para.text for para in paragraph_containers]
    paragraphs = ' '.join(paragraphs).lstrip(' (CNN)')
    content = f'{header} {paragraphs}'

    return content

if __name__ == '__main__':
# get_cnn_articles(5000, 'business', '/Users/Isaacbolo/DataspellProjects/word_analysis_project/data/liberal/cnn')
    get_cnn_articles(30, 'politics', '../data/liberal/cnn')
