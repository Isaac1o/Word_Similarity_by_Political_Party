import newsparser as news


if __name__ == '__main__':
    # news.get_fox_articles(500, 'politics', 'data/conservative/fox')
    # news.get_blaze_articles(500, 'politics', 'data/conservative/blaze')
    # news.get_ny_post_articles(500, 'news', 'data/conservative/nypost')
    # news.get_fox_articles(500, 'opinion', 'data/conservative/fox')
    # news.get_blaze_articles(500, 'opinion', 'data/conservative/blaze')
    # news.get_ny_post_articles(500, 'opinion', 'data/conservative/nypost')
    news.get_fox_articles(500, 'media', 'data/conservative/fox')
    news.get_blaze_articles(500, 'media', 'data/conservative/blaze')
    news.get_ny_post_articles(500, 'media', 'data/conservative/nypost')
    # news.get_fox_articles(500, 'business', 'data/conservative/fox')
    # news.get_blaze_articles(500, 'business', 'data/conservative/blaze')
    # news.get_ny_post_articles(500, 'business', 'data/conservative/nypost')