from flask import Flask, request, jsonify
from data_ingestor import *
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
@app.route('/ingest_data', methods=['GET'])
def ingest_data():
    guardian_list = getGuardianNews("https://www.theguardian.com")
    # euronews_list = getEuronews("https://www.euronews.com")
    # bbc_list = getBBCnews("https://bbc.com")
    # nurkz_list = getNurkzNews("https://nur.kz")
    # tengrinews_list = getTengriNews("https://tengrinews.kz")
    # moscowtimes_list = getMoscowTimesNews("https://www.themoscowtimes.com")

    news_data_combined = {
        'guardian': guardian_list,
        # 'euronews': euronews_list,
        # 'bbc': bbc_list,
        # 'nurkz': nurkz_list,
        # 'tengrinews': tengrinews_list,
        # 'moscowtimes': moscowtimes_list
    }

    return jsonify(news_data_combined)

@app.route('/process_data', methods=['POST'])
def assign_sentiment_to_each_news():
    return 0;


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
