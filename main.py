import sys
import newsparser as news


def main():
    news_outlet = sys.argv[1].lower()
    topic = sys.argv[2].lower()
    num_articles = int(sys.argv[3])
    directory_to_save = sys.argv[4]
    if news_outlet == 'cnn':
        directory = f'{directory_to_save}/cnn'
        news.get_cnn_articles(num_articles, topic, directory)
    elif news_outlet == 'fox':
        directory = f'{directory_to_save}/cnn'
        news.get_fox_articles(num_articles, topic, directory)
    elif news_outlet == 'blaze':
        directory = f'{directory_to_save}/blaze'
        news.get_blaze_articles(num_articles, topic, directory)


if __name__ == '__main__':
    main()