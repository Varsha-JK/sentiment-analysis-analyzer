from flask import Flask, render_template, Response, send_file
from analyzer import keywords_cloud, pre_process, DbConnect, sentiment
import pandas as pd
import jsonpickle
import base64
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze/wordcloud")
def get_wordcloud():
    tweets_df = pd.DataFrame(columns=['preprocessed_tweets'])
    for data in tweets:
        index = len(tweets_df)
        tweets_df.loc[index, 'preprocessed_tweets'] = pre_process(data[0])
    img = keywords_cloud(tweets_df)
    # imgword = 'data:image/png;base64,{}'.format(base64.b64encode(img.getvalue()).decode())
    # return render_template('visuals.html', wordcloud=imgword)
    img.save("./wordcloud.png")
    return send_file('./wordcloud.png')

@app.route("/analyze/sentiment")
def get_sentiment():
    sentiment_list = sentiment(tweets)
    return Response(response=jsonpickle.encode(sentiment_list), status=200, mimetype="application/json")

@app.route("/analyze/<topic>")
def analyze(topic):
    global tweets
    tweets = DbConnect(topic)
    result = {"status":"success"}
    return Response(response=jsonpickle.encode(result), status=200, mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0",port=7007)






