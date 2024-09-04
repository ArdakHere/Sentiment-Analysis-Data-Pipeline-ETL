from sqlalchemy import Column, Integer, String, Float, Text, DateTime, ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class NewsProcessed(Base):
    __tablename__ = 'news_processed'

    id = Column(Integer, primary_key=True)
    color = Column(ARRAY(Float))  # Assuming color is an array of numeric values, adjust type if needed
    publisher_identifier = Column(String)
    sentiment_index = Column(Float)
    text = Column(Text)
    timestamp = Column(String)

class NewsFrequencyWords(Base):
    __tablename__ = 'news_frequency_words'
    id = Column(Integer, primary_key=True)
    associated_sentiment = Column(Float)
    color = Column(ARRAY(Float))  # Assuming color is an array of numeric values, adjust type if needed
    frequency = Column(Integer)
    timestamp = Column(String)
    text = Column(Text)

class NewsAvgSentimentByPublisher(Base):
    __tablename__ = 'news_avg_sentiment_by_publisher'
    id = Column(Integer, primary_key=True)
    average_sentiment = Column(Float)
    color = Column(ARRAY(Float))  # Assuming color is an array of numeric values, adjust type if needed
    timestamp = Column(String)
    publisher = Column(String)
