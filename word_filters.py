import re
import string
import spacy
import pandas as pd


# TODO: Check if removing names will improve results
def get_words(text, remove_stopwords=True, min_word_length=3):
    regex = re.compile('[' + re.escape(string.punctuation) + '0-9\\r\\t\\n]')
    nopunct = regex.sub(" ", text)  # delete stuff but leave at least a space to avoid clumping together
    words = nopunct.split(' ')
    words = [word for word in words if len(word) >= min_word_length]
    words = [word.lower() for word in words]
    if remove_stopwords:
        sp = spacy.load('en_core_web_sm')
        stopwords = sp.Defaults.stop_words
        words = [word for word in words if word not in stopwords]
    return words


def get_words_spacy(sp, text, remove_stopwords=True, remove_person=False, min_word_length=3):
    doc = sp(text)
    # nopunct = [word for word in doc if word.is_alpha is True]
    doc = [word for word in doc if word.like_url is False and word.like_email is False]
    if remove_person:
        doc = [word for word in doc if word.ent_type_ != 'PERSON']
    words = [word.text.lower() for word in doc if len(word.text.lower()) >= min_word_length]
    if remove_stopwords:
        stopwords = sp.Defaults.stop_words
        words = [word for word in words if word not in stopwords]

    return words


def load_spacy():
    return spacy.load('en_core_web_sm')


# nlp = load_spacy()
#
# with open('/Users/Isaacbolo/data/cnn_5000/article1.txt', 'r') as f:
#     article_text = f.read()
#
# words_spacy = get_words_spacy(nlp, article_text, remove_person=False)
# print(words_spacy)
# words_nonspacy = get_words(article_text)
#
# df = pd.DataFrame(data=zip(words_nonspacy, words_spacy), columns=['no_spacy', 'spacy'])
# df.to_csv('compare_words.csv')