import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import requests


def get_ny_post_articles(num_articles, topic, dir_name):
    full_dir_path = f'{dir_name}/{topic}'
    if not os.path.isdir(full_dir_path):
        os.mkdir(full_dir_path)

    # Start browser
    browser = webdriver.Chrome()
    url = f'https://nypost.com/search/{topic}/'
    browser.get(url)
    time.sleep(2)

    n = 0
    while n < num_articles:
        article_containers = browser.find_elements_by_class_name('story__headline.headline.headline--archive')
        for article_container in article_containers:
            # Go through all articles on page and save their article contents
            link = article_container.find_element_by_tag_name('a').get_attribute('href')
            try:
                content = get_ny_post_content(link)
                with open(f'{full_dir_path}/article{n}.txt', 'w') as f:
                    f.write(content)
                n += 1
                if n == num_articles:
                    break
            except Exception as e:
                print(e)
                print(f'Unable to write or save {link}')
                print()

        # Click button for next page
        next_page_button = browser.find_element_by_class_name('button.button--solid')
        next_page_button.click()

    browser.close()


def get_ny_post_content(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')

    header = soup.find(class_='headline headline--single').text.strip()
    content_container = soup.find(class_='single__content entry-content m-bottom')
    paragraph_containers = content_container.find_all('p')
    body = ''
    for paragraph in paragraph_containers:
        paragraph_text = paragraph.text.strip()
        if len(paragraph_text) != 0:
            body += f'{paragraph_text} '

    content = f'{header}\n{body}'

    return content
