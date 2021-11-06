import sys
import newsparser as news
import os


def main():
    news_outlets = ['fox', 'salon', 'blaze', 'cnn', 'vox', 'ny_post']
    topics = ['politics', 'abortion', 'pandemic']
    num_articles = 3000
    directory_to_save = '/Users/Isaacbolo/DataspellProjects/word_analysis_project/data'

    directory = f'{directory_to_save}/liberal/cnn'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for topic in topics:
        try:
            news.get_cnn_articles(num_articles, topic, directory)
        except Exception as e:
            print(e)
            print(f'Unable to parse CNN {topic}')
            print()

    directory = f'{directory_to_save}/conservative/fox'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for topic in topics:
        try:
            news.get_fox_articles(num_articles, topic, directory)
        except Exception as e:
            print(e)
            print(f'Unable to parse Fox {topic}')
            print()

    directory = f'{directory_to_save}/conservative/blaze'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for topic in topics:
        try:
            news.get_blaze_articles(num_articles, topic, directory)
        except Exception as e:
            print(e)
            print(f'Unable to parse Blaze {topic}')
            print()

    directory = f'{directory_to_save}/liberal/vox'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for topic in topics:
        try:
            news.get_vox_articles(num_articles, topic, directory)
        except Exception as e:
            print(e)
            print(f'Unable to parse Vox {topic}')
            print()

    directory = f'{directory_to_save}/conservative/ny_post'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for topic in topics:
        try:
            news.get_ny_post_articles(num_articles, topic, directory)
        except Exception as e:
            print(e)
            print(f'Unable to parse NYPost {topic}')
            print()

    directory = f'{directory_to_save}/liberal/salon'
    if not os.path.exists(directory):
        os.makedirs(directory)
    for topic in topics:
        try:
            news.get_salon_articles(num_articles, topic, directory)
        except Exception as e:
            print(e)
            print(f'Unable to parse Salon {topic}')
            print()



if __name__ == '__main__':
    main()