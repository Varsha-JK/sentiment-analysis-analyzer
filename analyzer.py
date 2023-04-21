from textblob import TextBlob
import re
from wordcloud import WordCloud
import psycopg2
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from io import BytesIO

nltk.download('wordnet')
nltk.download('vader_lexicon')

def pre_process(tweet):
    tweet = re.sub(r'http\S+', '', tweet)
    tweet = re.sub("@\w+", "", tweet)
    tweet = re.sub("[^a-zA-Z#]", " ", tweet)
    tweet = re.sub("\s+", " ", tweet)
    tweet = tweet.lower()
    # lemmatizer = WordNetLemmatizer()
    # sent = ' '.join([lemmatizer.lemmatize(w) for w in tweet.split() if len(lemmatizer.lemmatize(w)) > 3])
    tweet = ' '.join([word for word in tweet.split() if len(word) > 3])
    return tweet

#Connect to db and fetch data
def DbConnect(topic):
    DATABASE_URL = 'postgres://bnariixreyjoiz:824ef864682bec505c004f004ff146ea86ecfcd6eeac5f65f2b56f2b023484cb@ec2-54-208-11-146.compute-1.amazonaws.com:5432/de7a7uvn6sad18'
    connection = psycopg2.connect(DATABASE_URL)
    # connection = psycopg2.connect(host="postgres", database="postgres", port=5432, user= "postgres", password = "postgres")
    curr = connection.cursor()
    curr.execute("SELECT tweets FROM tweets WHERE topic = (%s);", [topic])
    data = curr.fetchall()

    return data


def keywords_cloud(tweet_df):
    words = ' '.join([text for text in tweet_df['preprocessed_tweets']])
    wordcloud = WordCloud(width=800, height=500, random_state=21, max_font_size=110).generate(words)
    wordcloudImage = wordcloud.to_image()
    # img = BytesIO()
    # wordcloudImage.save(img, format='PNG')
    return wordcloudImage


def calc_percent(number, total):
    return number*100/total

def sentiment(tweets):
    positive = 0
    negative = 0
    neutral = 0
    polarity = 0
    neutral_list = []
    negative_list = []
    positive_list = []
    number_of_tweets = len(tweets)
    for tweet in tweets:
        tweet = tweet[0]
        analysis = TextBlob(tweet)
        score = SentimentIntensityAnalyzer().polarity_scores(tweet)
        negative_score = score['neg']
        positive_score = score['pos']
        polarity += analysis.sentiment.polarity

        if negative_score > positive_score:
            negative_list.append(tweet)
            negative += 1
        elif positive_score > negative_score:
            positive_list.append(tweet)
            positive += 1

        elif positive_score == negative_score:
            neutral_list.append(tweet)
            neutral += 1
    positive = calc_percent(positive, number_of_tweets)
    negative = calc_percent(negative, number_of_tweets)
    neutral = calc_percent(neutral, number_of_tweets)
    positive = format(positive, '.1f')
    negative = format(negative, '.1f')
    neutral = format(neutral, '.1f')
    return {'pos':positive, 'neu':neutral, 'neg':negative}
