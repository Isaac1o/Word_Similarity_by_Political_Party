import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import requests


def get_blaze_articles(num_articles, topic, dir_name):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    full_dir_path = f'{dir_name}/{topic}'
    if not os.path.isdir(full_dir_path):
        os.mkdir(full_dir_path)

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    URL = f'https://www.theblaze.com/search/?q={topic}'
    browser = webdriver.Chrome('/Users/Isaacbolo/chromedriver/chromedriver 3', options=chrome_options)
    browser.get(URL)
    time.sleep(2)

    n = 0
    i = 0
    while n < num_articles:
        links_container = browser.find_elements_by_class_name('widget__headline.h1')
        for link_element in links_container[i:]:
            link = link_element.find_element_by_tag_name('a').get_attribute('href')
            try:
                content = get_blaze_content(link)
                with open(f'{full_dir_path}/article{n}.txt', 'w') as f:
                    f.write(content)
                n += 1
                if n == num_articles:
                    break
            except Exception as e:
                print(e)
                print(f'Blaze Error: Unable to read or write {link}')
                print()
            i += 1

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # load_button = browser.find_element_by_class_name('btn.button-load-more.next-page-wrapper.action-btn')

        try:
            browser.find_element_by_class_name('btn.button-load-more.next-page-wrapper.action-btn').click()
            time.sleep(2)
        except Exception as e:
            print(e)
            try:
                browser.find_element_by_class_name('sailthru-overlay-close').click()
            except Exception as e:
                print(e)
                try:
                    close_overlay = browser.find_element_by_class_name('overlay-close-button')
                    close_overlay.click()
                except Exception as e:
                    print(e)
                    browser.find_element_by_class_name('overlay-creative-message').click()
                continue

    browser.close()
    time.sleep(2)


def get_blaze_content(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    header = soup.find(class_='headline h1').text.strip()
    paragraph_container = soup.find(class_='body-description')
    paragraph_tags = paragraph_container.find_all('p', class_=None)
    paragraphs = [p.text.strip() for p in paragraph_tags if len(p.text) != 0]
    body = ' '.join(paragraphs).strip()
    content = f'{header} {body}'

    return content


if __name__ == '__main__':
    get_blaze_articles(30, 'opinion', '../data/conservative/blaze')