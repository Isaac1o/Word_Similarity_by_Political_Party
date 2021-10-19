import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def get_cnn_article_links(num_articles: int, topic: str) -> tuple:
    browser = webdriver.Chrome()  # initialize selenium Chrome browser object

    article_links = set()
    i = 0
    while len(article_links) < num_articles:
        URL = f'https://www.cnn.com/search?q={topic}&size=50&from={i}&page='
        browser.get(URL)  # opens url on Chrome browser
        articles = browser.find_elements_by_class_name('cnn-search__result-headline')
        for article in articles:
            link = article.find_element_by_tag_name('a').get_attribute('href')
            if 'index.html' in link:
                article_links.add(link)
                if len(article_links) == num_articles:
                    break
            i += 1

    browser.close()

    return tuple(article_links)






    #
    #     for starting_index in range(0, num_articles, 50):
    #         # CNN only allows 50 articles to display on a page, so I have to parse 50 articles
    #         # at a time.
    #         base_url = f'https://www.cnn.com/search?q={topic}&size=50&from={starting_index}&page='
    #         browser.get(base_url)  # opens url on Chrome browser
    #         time.sleep(2)  # give browser time to load
    #
    #         # Finds the container that contains every news article.
    #         main_news_container = browser.find_element_by_class_name('cnn-search__results-list')
    #
    #         # In main container get 'a'
    #         text_sections = main_news_container.find_elements_by_xpath("//a[@href]")
    #
    #         current_link = None
    #         for elem in text_sections:
    #             if 'index.html' in elem.get_attribute('href') and elem.get_attribute('href') != current_link:
    #                 article_links.append(elem.get_attribute('href'))
    #                 current_link = elem.get_attribute("href")
    #
    # browser.close()
    #
    # return tuple(article_links)


def get_fox_article_links(num_articles: int, topic: str) -> tuple:
    browser = webdriver.Chrome()  # initialize selenium Chrome browser object

    base_url = f'https://www.foxnews.com/{topic}'
    browser.get(base_url)  # opens url on Chrome browser
    time.sleep(2)  # give browser time to load

    # There might be an alert button blocking the load more button.
    # Try to close the alert button.
    try:
        alert_container = browser.find_element_by_class_name('alert-banner.is-programming')
        close_alert_button = alert_container.find_element_by_class_name('close')
        close_alert_button.click()
    except:
        print('No alert banner to close')

    # Finds the container that contains every news article.
    main_news_container = browser.find_element_by_class_name('main-content')
    article_section = main_news_container.find_element_by_class_name('collection.collection-article-list.has-load-more')

    # Fox has a load more button. Each time you click the button 10 additional
    # articles are displayed.
    load_more_button = article_section.find_element_by_class_name('button.load-more.js-load-more')

    break_switch = False
    article_links = set()
    start_index = 0
    while True:
        articles = article_section.find_elements_by_class_name('article')
        for article in articles[start_index:]:
            try:
                link = article.find_element_by_tag_name('a').get_attribute('href')
                if 'video' not in link and not link.endswith('/'):
                    article_links.add(link)
                    print(link)
                    if len(article_links) == num_articles:
                        break_switch = True
                        break
            except:
                print('Element does not have <a> tag. Going to skip')

            start_index += 1

        if break_switch is True:
            break

        try:
            load_more_button.click()
            time.sleep(1)  # give browser time to load additional articles
        except:
            # Popup widget might appear.
            print('Popup window displayed, trying to close...')
            popup_button = browser.find_element_by_class_name('pf-widget-close')
            popup_button.click()

    browser.close()

    return tuple(article_links)


def get_wp_links(num_articles, topic) -> list:
    URL = f'https://www.washingtonpost.com/{topic}'
    browser = webdriver.Chrome()
    try:
        browser.get(URL)
        time.sleep(3)
    except Exception as e:
        print(e)

    main_container = browser.find_element_by_xpath('//*[contains(@class, "main-content-chain sectionx")]')
    browser.execute_script("window.scrollTo(0, 10000);")
    load_more_button = browser.find_element_by_class_name('pb-loadmore-div-ans.button.pb-loadmore.clear')

    links = set()
    i = 0
    while len(links) < num_articles:
        # articles = main_container.find_elements_by_tag_name()
        articles = main_container.find_elements_by_xpath('//a[@data-pb-local-content-field="web_headline"]')
        assert len(articles) > 0, 'No articles found'
        for article in articles[i:]:
            # if 'web_headline' in articles.get_attribute('data-pb-local-content-field'):
            link = article.get_attribute('href')
            links.add(link)
            if len(links) == num_articles:
                break
            i += 1

        try:
            load_more_button.click()
            time.sleep(1)
        except Exception as e:
            print(e)

    browser.close()

    return tuple(links)


def get_the_blaze_links(num_articles, topic):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-notifications")
    URL = f'https://www.theblaze.com/search/?q={topic}'
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(URL)
    time.sleep(2)

    links = set()
    i = 0
    while len(links) < num_articles:
        headlines = browser.find_elements_by_class_name('widget__headline.h1')
        for headline in headlines[i:]:
            try:
                link = headline.find_element_by_tag_name('a').get_attribute('href')
                links.add(link)
            except Exception as e:
                print(e)
            if len(links) == num_articles:
                break
            i += 1
        browser.execute_script("window.scrollTo(0, 10000);")
        load_button = browser.find_element_by_class_name('btn.button-load-more.next-page-wrapper.action-btn')
        try:
            load_button.click()
            time.sleep(.5)
        except Exception as e:
            print(e)
            try:
                popup_exit = browser.find_element_by_id('no-thanks')
                popup_exit.click()
            except Exception as e:
                print(e)
                try:
                    close_overlay = browser.find_element_by_class_name('overlay-close-button')
                    close_overlay.click()
                except Exception as e:
                    print(e)
                    browser.find_element_by_class_name('overlay-creative-message').click()
                continue

    return tuple(links)

links = get_cnn_article_links(100, 'politics')
for link in links: print(link)



#push-overlay > div > div.overlay-close-button
# fox_articles = get_fox_article_links(100, 'politics')
# for link in fox_articles:
#     print(link)

# cnn_links = get_cnn_article_links(100, 'politics')
# for link in cnn_links:
#     print(link)







    #
    # number_of_clicks = (num_articles // 10) + 1
    # for _click in range(number_of_clicks):
    #     try:
    #         load_more_button.click()
    #         time.sleep(1)
    #     except:
    #         # Popup widget might appear.
    #         print('Popup window displayed, trying to close...')
    #         popup_button = browser.find_element_by_class_name('pf-widget-close')
    #         popup_button.click()
    #
    # article_links = []
    # articles = article_section.find_elements_by_class_name('article')
    # for article in articles:
    #     try:
    #         link_container = article.find_element_by_class_name('m')
    #         link = link_container.find_element_by_tag_name('a').get_attribute('href')
    #         if 'video' not in link and not link.endswith('/'):
    #             article_links.append(link)
    #             print(link)
    #     except:
    #         print('Element does not have <a> tag. Going to skip')
    #         continue










# articles = get_cnn_article_links(100, 'covid19')
# print(articles)