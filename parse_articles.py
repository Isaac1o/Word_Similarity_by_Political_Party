import sys
import newsparser as news
import os


def main():
    news_outlets = ['fox', 'salon', 'blaze', 'cnn', 'vox', 'ny_post']
    topics = ['politics', 'abortion', 'covid19']
    num_articles = 500
    directory_to_save = sys.argv[1]

    for news_outlet in news_outlets:
        if news_outlet == 'cnn':
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

        elif news_outlet == 'fox':
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

        elif news_outlet == 'blaze':
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

        elif news_outlet == 'vox':
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

        elif news_outlet == 'ny_post':
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

        elif news_outlet == 'salon':
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
    # topics = ['politics', 'abortion', 'covid19']
    # directory = f'{sys.argv[1]}/conservative/fox'
    # if not os.path.exists(directory):
    #     os.makedirs(directory)
    # for topic in topics:
    #     news.get_fox_articles(30, topic, directory)