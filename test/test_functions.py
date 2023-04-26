import json

import PIL.Image

from analyzer import *
import pandas as pd

def test_preprocess_1():
    input = "https://abcd.com/fix"
    output = ""
    function_out = pre_process(input)
    assert function_out == output

def test_preprocess_2():
    input = "SomEthinG"
    output = "something"
    function_out = pre_process(input)
    assert function_out == output

def test_preprocess_3():
    input = "Nice to meet you."
    output = "nice meet"
    function_out = pre_process(input)
    assert function_out == output

def test_word_cloud(topic):
    tweets = DbConnect(topic)
    print("tweeeeeet",tweets[0])
    tweets_df = pd.DataFrame(columns=['preprocessed_tweets'])
    for data in tweets:
        index = len(tweets_df)
        tweets_df.loc[index, 'preprocessed_tweets'] = pre_process(data[0])
    image = keywords_cloud(tweets_df)
    assert type(image) is PIL.Image.Image


def test_sentiment():
    tweet_1 = [("very happy and satisfied",)]
    expected_1 = {'neg': '0.0', 'neu': '0.0', 'pos': '100.0'}
    output_1 = sentiment(tweet_1)
    tweet_2 = [("exhausted and tired",)]
    expected_2 = {'neg': '100.0', 'neu': '0.0', 'pos': '0.0'}
    output_2 = sentiment(tweet_2)
    assert output_1 == expected_1
    assert output_2 == expected_2