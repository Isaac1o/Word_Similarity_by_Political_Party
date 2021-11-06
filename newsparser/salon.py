import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import requests


def get_salon_articles(num_articles, topic, dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    full_dir_path = f'{dir_name}/{topic}'
    if not os.path.isdir(full_dir_path):
        os.mkdir(full_dir_path)

    # Start browser
    browser = webdriver.Chrome()
    page_num = 1
    url = f'https://www.salon.com/search/{topic}?pagenum={page_num}'

    n = 0
    while n < num_articles:
        browser.get(url)
        time.sleep(1)
        try:
            link_containers = browser.find_elements_by_class_name('search-title')
        except Exception as e:
            print(e)
            print('No results on this page')
            break
        for link_container in link_containers:
            link = link_container.get_attribute('href')
            try:
                content = get_salon_content(link)
                with open(f'{full_dir_path}/article{n}.txt', 'w') as f:
                    f.write(content)
                n += 1
                if n == num_articles:
                    break
            except Exception as e:
                print(e)
                print(f'Unable to write or read {link}')
                print()

        page_num += 1

    browser.close()
    time.sleep(2)


def get_salon_content(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')

    header = soup.find(class_='article_badge_wrapper').text.strip()
    article_container = soup.find(class_='article-content')
    paragraph_containers = soup.find_all('p')
    body = ''
    for paragraph_container in paragraph_containers:
        paragraph = paragraph_container.text.strip()
        if len(paragraph) != 0:
            body += paragraph + ' '

    content = header + ' ' + body.strip()

    return content
