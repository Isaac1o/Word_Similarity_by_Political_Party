import newsparser as news


if __name__ == '__main__':
    news.get_cnn_articles(500, 'politics', 'data/liberal/cnn')
    news.get_vox_articles(500, 'politics', 'data/liberal/vox')
    news.get_mother_jones_articles(500, 'politics', 'data/liberal/motherjones')
    news.get_cnn_articles(500, 'opinion', 'data/liberal/cnn')
    news.get_vox_articles(500, 'opinion', 'data/liberal/vox')
    news.get_mother_jones_articles(500, 'opinion', 'data/liberal/motherjones')
    news.get_cnn_articles(500, 'business', 'data/liberal/cnn')
    news.get_vox_articles(500, 'business', 'data/liberal/vox')
    news.get_mother_jones_articles(500, 'business', 'data/liberal/motherjones')
