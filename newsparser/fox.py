import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
from bs4 import BeautifulSoup
import requests


def get_fox_articles(num_articles: int, topic: str, dir_name: str):
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    full_dir_path = f'{dir_name}/{topic}'
    if not os.path.isdir(full_dir_path):
        os.mkdir(full_dir_path)

    browser = webdriver.Chrome()  # initialize selenium Chrome browser object

    valid_topics = [
        'us',
        'politics',
        'media',
        'opinion',
        'business',
        'entertainment',
        'sports',
        'lifestyle',
        'weather',
        'tv',
        'fox-nation',
        'listen'
    ]
    topic = topic.lower()
    if topic not in valid_topics:
        print('Not a valid topic')
        return None

    base_url = f'https://www.foxnews.com/{topic}'
    browser.get(base_url)  # opens url on Chrome browser
    time.sleep(2)  # give browser time to load

    # There might be an alert button blocking the load more button.
    # Try to close the alert button.
    try:
        alert_container = browser.find_element_by_class_name('alert-banner.is-programming')
        close_alert_button = alert_container.find_element_by_class_name('close')
        close_alert_button.click()
    except Exception as e:
        print(e)

    # Filter search to only contain articles
    # browser.find_element_by_class_name('select').click()  # click drop down
    # browser.find_element_by_xpath('//input[@value="Article"]').click()  # click article check box
    # browser.find_element_by_class_name('search-form').find_element_by_class_name('button').click()  # click search
    # time.sleep(1)

    # Finds the container that contains every news article.
    # article_section = browser.find_element_by_class_name('collection.collection-search.active')
    # article_section = main_news_container.find_element_by_class_name('collection.collection-article-list.has-load-more')

    # Fox has a load more button. Each time you click the button 10 additional articles are displayed.
    # load_more_button = article_section.find_element_by_class_name('button.load-more')

    n = 0
    first_articles_container = browser.find_element_by_class_name('collection.collection-article-list')
    first_articles = first_articles_container.find_elements_by_class_name('title')
    for article in first_articles:
        link = article.find_element_by_tag_name('a').get_attribute('href')
        if 'video.foxnews' not in link:
            try:
                content = get_fox_content(link)
                with open(f'{full_dir_path}/article{n}.txt', 'w') as f:
                    f.write(content)
                n += 1
                if n == num_articles:
                    break
            except Exception as e:
                print(e)
                print(f'Fox Error: Unable to read or write {link}')
                print()

    addition_articles_container = browser.find_element_by_class_name('collection.collection-article-list.has-load-more')
    show_more_button = browser.find_element_by_class_name('button.load-more.js-load-more')
    start_index = 0
    while n < num_articles:
        articles = addition_articles_container.find_elements_by_tag_name('article')
        for article in articles[start_index:]:
            link = article.find_element_by_tag_name('a').get_attribute('href')
            if 'video.foxnews' not in link:
                try:
                    content = get_fox_content(link)
                    with open(f'{full_dir_path}/article{n}.txt', 'w') as f:
                        f.write(content)
                    n += 1
                    if n == num_articles:
                        break
                except Exception as e:
                    print(e)
                    print(f'Fox Error: Unable to read or write {link}')
                    print()
            start_index += 1

        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            show_more_button.click()
            time.sleep(.5)  # give browser time to load additional articles
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        except Exception as e:
            # Popup widget might appear.
            print(e)
            print('Popup window displayed, trying to close...')
            popup_button = browser.find_element_by_class_name('pf-widget-close')
            popup_button.click()

    browser.close()
    time.sleep(2)


def get_fox_content(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.text, 'html.parser')
    header = soup.find(class_='headline').text.strip()
    sub_header_container = soup.find(class_='sub-headline speakable')
    sub_header = ''
    if sub_header_container:
        sub_header = sub_header_container.text.strip()
    article_body = soup.find(class_='article-body')
    paragraph_containers = article_body.find_all('p')
    paragraphs = [p.text for p in paragraph_containers]
    body = ' '.join(paragraphs).strip()
    content = f'{header} {sub_header} {body}'
    
    return content



get_fox_articles(200, 'politics', '/tmp/fox')
# print(get_fox_content('https://www.foxnews.com/opinion/joe-concha-media-questioning-politics-mask-guidelines'))



















