from flask import Flask, render_template, Response, send_file
from analyzer import keywords_cloud, pre_process, DbConnect, sentiment
import pandas as pd
import jsonpickle
import requests
from flask_cors import CORS
import os
from kafka_messaging import producer

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze/<topic>/wordcloud")
def get_wordcloud(topic):
    tweets = DbConnect(topic)
    tweets_df = pd.DataFrame(columns=['preprocessed_tweets'])
    for data in tweets:
        index = len(tweets_df)
        tweets_df.loc[index, 'preprocessed_tweets'] = pre_process(data[0])
    img = keywords_cloud(tweets_df)
    img.save("./wordcloud.png")
    return send_file('./wordcloud.png')

@app.route("/analyze/<topic>/sentiment")
def get_sentiment(topic):
    tweets = DbConnect(topic)
    sentiment_list = sentiment(tweets)
    return Response(response=jsonpickle.encode(sentiment_list), status=200, mimetype="application/json")

@app.route("/analyze/<topic>")
def analyze(topic):
    collector_url = os.getenv("COLLECTOR_URL")
    loc_url = "{0}/collector/{1}".format(collector_url,"collect")
    producer(topic)
    result = requests.get(loc_url).json()
    while "status" not in result:
        result = requests.get(loc_url).json()
    if result["status"] == "success":
        print("success")
    global tweets
    tweets = DbConnect(topic)
    result = {"status":"success"}
    return Response(response=jsonpickle.encode(result), status=200, mimetype="application/json")

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=8000)
#     app.run()
