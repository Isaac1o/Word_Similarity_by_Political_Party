import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import requests


def get_vox_articles(num_articles: int, topic: str, dir_name: str):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    full_dir_path = f'{dir_name}/{topic}'
    if not os.path.isdir(full_dir_path):
        os.mkdir(full_dir_path)

    url = f'https://www.vox.com/search?q={topic}&type=Article'
    browser = webdriver.Chrome()  # initialize selenium Chrome browser object
    time.sleep(2)
    browser.get(url)

    n = 0
    while n < num_articles:
        main_container = browser.find_element_by_class_name('c-compact-river')
        article_containers = main_container.find_elements_by_class_name('c-compact-river__entry ')
        for article in article_containers:
            link = article.find_element_by_tag_name('a').get_attribute('href')
            try:
                with open(f'{full_dir_path}/article{n}.txt', 'w') as f:
                    f.write(get_vox_content(link))
                n += 1
                if n == num_articles:
                    break
            except Exception as e:
                print(e)
                print(f'Vox Error: Unable to read or write {link}')
                print()

        next_page_button = browser.find_element_by_class_name('c-pagination__next.c-pagination__link.p-button')
        next_page_button.click()
        time.sleep(.5)

    browser.close()
    time.sleep(2)


def get_vox_content(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    header = soup.find(class_='c-page-title').text
    sub_header = soup.find(class_='c-entry-summary p-dek').text
    content_container = soup.find(class_='c-entry-content')
    paragraph_containers = content_container.find_all('p')
    paragraphs = [p.text.strip() for p in paragraph_containers if len(p.text.strip()) != 0]
    paragraphs = ' '.join(paragraphs)
    content = f'{header}\n{sub_header}\n{paragraphs}'

    return content
