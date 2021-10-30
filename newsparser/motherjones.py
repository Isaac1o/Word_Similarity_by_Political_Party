import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import requests


def get_mother_jones_articles(num_articles, topic, dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    full_dir_path = f'{dir_name}/{topic}'
    if not os.path.isdir(full_dir_path):
        os.mkdir(full_dir_path)

    # Start browser
    browser = webdriver.Chrome()
    url = f'https://www.motherjones.com/?s={topic}'
    browser.get(url)

    n = 0
    while n < num_articles:
        link_containers = browser.find_elements_by_class_name('hed')
        for link_container in link_containers:
            link = link_container.get_attribute('href')
            try:
                content = get_mother_jones_content(link)
                with open(f'{full_dir_path}/article{n}.txt', 'w') as f:
                    f.write(content)
                n += 1
                if n == num_articles:
                    break
            except Exception as e:
                print(e)
                print(f'Unable to read or write {link}')
                print()

        next_button = browser.find_element_by_class_name('pager_next')
        next_button.click()

    browser.close()


def get_mother_jones_content(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')

    header = soup.find(class_='entry-title').text.strip()
    body_container = soup.find(class_='entry-content')
    paragraph_containers = body_container.find_all('p', class_=None)
    body = ''
    for paragraph_container in paragraph_containers:
        paragraph = paragraph_container.text.strip()
        if len(paragraph) != 0:
            body += f'{paragraph} '

    content = f'{header}\n{body}'

    return content
