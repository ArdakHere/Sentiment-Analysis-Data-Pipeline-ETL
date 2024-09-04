import streamlit as st
import pandas as pd
import certifi
import numpy as np
from pymongo import MongoClient

connection_string = "mongodb+srv://ardakatagulov:gJ221JJ51LdfO3tr@cluster0.adqyl76.mongodb.net/"

# Connect to MongoDB
client = MongoClient(connection_string, tlsCAFile=certifi.where())

# Access the database
db = client['news_data']  # Replace with your database name

# Access the collection
collection = db['news_processed']  # Replace with your collection name

documents = collection.find()

sentiments = {}

# Streamlit app
st.title("Publisher Sentiment Dashboard")
# while len(sentiments) != 5:

if 'sentiments' not in st.session_state:
    st.session_state.sentiments = {}

entered_check = 0

while len(st.session_state.sentiments) != 5:
    entered_check = 1
    docs = collection.find()
    for doc in docs:
        for key, value in doc.items():
            if key.endswith('_avg_sentiment'):
                publisher_name = key.replace('_avg_sentiment', '')
                if publisher_name not in st.session_state.sentiments:
                    st.session_state.sentiments[publisher_name] = value
                if len(st.session_state.sentiments) == 5:
                    break
        if len(st.session_state.sentiments) == 5:
            break

if entered_check == 0:
    docs = collection.find()

    for doc in docs:
        for key, value in doc.items():
            if key.endswith('_avg_sentiment'):
                publisher_name = key.replace('_avg_sentiment', '')
                if publisher_name not in st.session_state.sentiments:
                    st.session_state.sentiments[publisher_name] = value
            if len(st.session_state.sentiments) == 5:
                break



for avg_sentiment in st.session_state.sentiments.items():

    if avg_sentiment[1] > 0.3:
        color = (0, 255, 0)  # Green for positive sentiment
    if 0.3 >= avg_sentiment[1] > 0.15:
        color = (196, 255, 0)
    if 0.15 >= avg_sentiment[1] > 0:
        color = (222, 255, 0)
    if avg_sentiment[1] == 0:
        color = (255, 239, 0)  # White for neutral sentiment
    if 0 > avg_sentiment[1] > -0.15:
        color = (255, 179, 0)
    if -0.15 >= avg_sentiment[1] >= -0.3:
        color = (255, 94, 0)
    if avg_sentiment[1] < -0.3:
        color = (255, 0, 0)  # Red for negative sentiment

    color_str = f"rgb{color}"

    st.markdown(f"""
                <div style='border: 1px solid #ccc; padding: 8px; margin-bottom: 10px; border-radius: 15px; background: {color_str};'>
                    <h3 style='margin-top: 5px; margin-left: 5px; margin-bottom: -5px; font-size: 26px;color: black; text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff;'>{avg_sentiment[0]}</h3>
                    <p style='margin-left: 5px; margin-bottom: 5px; font-size: 26px; color: black; text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff;'>Sentiment: {avg_sentiment[1]}</p>
                </div>
            """, unsafe_allow_html=True)


# Display tiles for each publisher
# for index, row in df.iterrows():
#     publisher = row['Publisher']
#     sentiment = row['Sentiment']
#     color = row['Color']
#     change = row['Change']
#     change_symbol = "▲" if change > 0 else "▼" if change < 0 else "-"
#
#     color_str = f"rgb{color}"
#
#     st.markdown(f"""
#             <div style='border: 1px solid #ccc; padding: 10px; margin-bottom: 10px; border-radius: 15px; background: {color_str};'>
#                 <h3 style='color: black; text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff;'>{publisher}</h3>
#                 <p style='color: black; text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff;'>Sentiment: {sentiment:.2f}</p>
#                 <p style='color: black; text-shadow: -1px -1px 0 #fff, 1px -1px 0 #fff, -1px 1px 0 #fff, 1px 1px 0 #fff;'>Change: {change} {change_symbol}</p>
#             </div>
#         """, unsafe_allow_html=True)
