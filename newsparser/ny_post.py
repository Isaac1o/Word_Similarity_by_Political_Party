import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import requests


def get_ny_post_articles(num_articles, topic, dir_name):
    valid_topics = [
        'news',
        'sports',
        'opinion',
        'fashion',
        'living',
        'tech',
        'video',
        'business',
        'entertainment',
        'media'
    ]
    topic = topic.lower()
    if topic not in valid_topics:
        print('Not a valid topic')
        return None

    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    full_dir_path = f'{dir_name}/{topic}'
    if not os.path.isdir(full_dir_path):
        os.mkdir(full_dir_path)

    # Start browser
    browser = webdriver.Chrome('/Users/Isaacbolo/chromedriver/chromedriver 3')
    url = f'https://nypost.com/{topic}/'
    browser.get(url)
    time.sleep(2)

    # Close prompt
    try:
        print('Trying to close prompt')
        browser.find_element_by_class_name('pushly_popover-buttons-dismiss.pushly-prompt-buttons-dismiss').click()
        print('Prompt closed successfully\n')
    except Exception as e:
        print(e)
        print('No prompt to close... Continuing')

    n = 0
    i = 0
    while n < num_articles:
        stories_container = browser.find_element_by_class_name('the-latest__stories')
        article_containers = stories_container.find_elements_by_class_name('story__headline.headline.headline--archive')
        for article_container in article_containers[i:]:
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

            i += 1

        # browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            browser.find_element_by_class_name('button.button--solid.see-more').click()
            time.sleep(1)
        except Exception as e:
            print(e)
            print('Unable to click button. There may be an add in the way.')
            try:
                browser.find_element_by_class_name('bx-close-xsvg').click()
                browser.find_element_by_class_name('button.button--solid.see-more').click()
            except Exception as e:
                print(e)
                print('Unable to click button. Closing browser.')
                time.sleep(120)
                browser.close()
                return

    browser.close()
    time.sleep(2)


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

    content = f'{header} {body}'

    return content

if __name__ == '__main__':
    get_ny_post_articles(500, 'news', '../data/conservative/nypost')