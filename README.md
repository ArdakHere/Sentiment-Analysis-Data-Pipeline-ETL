**Development status 05.11.2024**

Data Engineering/Analytics pet-project, ETL Data pipeline for ingestion of web-scraped data from news websites:
- News titles are web-scraped from popular news outlets
- Pipeline is orchestrated with Apache Airflow
- Transforming and processing with Pandas and Python sentiment libraries
- Temporary loading to AWS S3 raw and processed buckets and loading to final storage BigQuery
- Deployed on AWS EC2
- Visualization is done via Looker Studio

Resources

<img width="745" alt="Screenshot 2024-12-05 at 15 54 32" src="https://github.com/user-attachments/assets/0a7e5c40-baaa-49bc-913c-b877c19e5fa5">



Attached is the schema of the pipeline. It works as follows:
* Extract stage
-  it scrapes news titles from the popular news outlets
- loads to the temporary storage AWS S3 raw and processed buckets. Stores S3 link to Xcoms.

* Transform and process stage
- Pulls raw data from S3 using Xcom. Assigns a sentiment index to every title and the timestamp, transforms data with Pandas.
  Loads processed data to processed S3 temporary bucket.

* Load stage
- Pulls processed data from S3 bucket
- Loads data to BigQuery


<iframe width="600" height="450" src="https://lookerstudio.google.com/embed/reporting/13f6cdf2-c88b-4feb-8bba-a24306a510b4/page/PdaYE" frameborder="0" style="border:0" allowfullscreen sandbox="allow-storage-access-by-user-activation allow-scripts allow-same-origin allow-popups allow-popups-to-escape-sandbox"></iframe>




A good acquaintance of mine suggested to me the idea of trying out data engineering/analytics a year ago. After some time, I started researching fundamental data concepts and formulating the pet project idea. Throughout the iterations of my pet project I have tried a lot of tools and even though some of them weren’t used there, I learned a lot. Here’s the rundown:

- Apache NiFi. Great GUI, easy to use processors for various data manipulations. However, the sentiment analysis was very cumbersome to perform. Python scripts are deprecated in NiFi and Groovy, the alternative for sentiment processing, didn’t work as intended
- Apache Kafka. I learned how to launch the tool, create connections from DB to Kafka and vice versa. Ended up, not using it, as I figured it might have been technical overkill for the purpose of the project.
- Grafana. I found it not so useful and simple to use as some BI visualization tools. It just didn’t fit the usage case for me.
- MongoDB. Decided go with PostgreSQL as it's open-source and could be deployed in docker in development.
- Although I considered using Plotly or pre-made JavaScript graphs, I was more interested in trying out BI tools, which led me to explore Looker, Tableau, and ultimately, Apache Superset.

- **NOW UTILIZED IN THE PROJECT** Apache Airflow **NOW UTILIZED IN THE PROJECT**


While developing, I have tried building these data pipelines:
- for stock prices of some companies. Rejected because of the limited APIs.
- for news titles with data from news APIs. Rejected because of limited APIs.

What I would like to do:
- add a separate dashboard that would analyze scraped contents of news articles, not just titles
- add a bias analysis
- add more news outlets to analyze (also have scripts ready for Nur.kz, Tengrinews.kz and Moscowtimes)
  
- try using the tools I rejected earlier **Airflow now utilized** 


I am open to feedback and suggestions to add/improve something, don't hesitate.
