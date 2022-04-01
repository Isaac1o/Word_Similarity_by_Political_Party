import numpy as np
import pandas as pd
import spacy
import os
import pickle
from progressbar import ProgressBar

sp = None
stp_wrds = None


def load_spacy():
    global sp
    if sp is None:
        sp = spacy.load('en_core_web_sm')
    return sp


def load_stopwords():
    global stp_wrds
    sp = load_spacy()
    if stp_wrds is None:
        stp_wrds = sp.Defaults.stop_words
    return stp_wrds


# TODO: Create function gets all article files
def filelist(root):
    """Return a fully-qualified list of filenames under root directory"""
    filenames = list()
    for root_dir, sub_dirs, files in os.walk(root):
        for file in files:
            if file.endswith('.txt'):
                filenames.append(os.path.join(root_dir, file))

    return tuple(filenames)


# TODO: Create function that opens and returns the contents of an article
def read_article(file_path):
    with open(file_path, 'r') as f:
        return f.read()


def article_preprocessor(article, lemmatizer=True):
    sp = load_spacy()
    stopwords = load_stopwords()
    words = sp(article)
    words = [w for w in words if w.is_alpha is True]  # remove word/token if it contains numbers
    if lemmatizer:
        words = [w.lemma_.lower() for w in words]
    else:
        words = [w.text.lower() for w in words]  # lowercase all words
    words = [w for w in words if len(w) > 2]  # remove words with len < 2
    return [w for w in words if w not in stopwords]


def format_articles(root_dir):
    # The root directory contains all articles for given party.
    # Using the file path to an article text, load and read the article and process it.
    # The processing step saves the article in a list of tokens. Append this list of tokens to a list.
    # Returns a list containing a list of words.
    article_paths = filelist(root_dir)
    formatted_articles = []
    pb = ProgressBar()
    for article_path in pb(article_paths):
        article = read_article(article_path)
        formatted_article = article_preprocessor(article)
        formatted_articles.append(formatted_article)

    return formatted_articles


def save_tokenized_article(path, articles):
    with open(path, 'wb') as f:
        pickle.dump(articles, f)


def main():
    print('Tokenizing liberal articles')
    lib_tokenized_articles = format_articles('data/liberal')
    save_tokenized_article('data/tokenized_articles/liberal_tokenized_articles.pickle', lib_tokenized_articles)

    print('\nTokenizing conservative articles')
    cons_tokenized_articles = format_articles('data/conservative')
    save_tokenized_article('data/tokenized_articles/conservative_tokenized_articles.pickle', cons_tokenized_articles)


if __name__ == '__main__':
    main()
