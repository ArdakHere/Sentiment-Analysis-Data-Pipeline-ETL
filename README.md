
Data Engineering/Analytics pet-project, ETL Data pipeline for ingestion of web-scraped data from news websites:
- News titles are web-scraped from popular news outlets
- Pipeline is orchestrated with Apache Airflow
- Transforming and processing with Pandas and Python sentiment libraries
- Temporary loading to AWS S3 raw and processed buckets and loading to final storage BigQuery
- Deployed on AWS EC2
- Visualization is done via Looker Studio

Tech stack of the project currently: AWS EC2, AWS S3, Apache Airflow, Python, Docker, BigQuery, Looker Studio. 


Architecture of the data pipeline

<img width="625" alt="Screenshot 2024-12-11 at 23 14 39" src="https://github.com/user-attachments/assets/3e2785e8-0215-4076-8c9a-d4f0841589ae" />


It works as follows:

** Extract stage
-  it scrapes news titles from the popular news outlets
- loads to the temporary storage AWS S3 raw and processed buckets. Stores S3 link to Xcoms.

** Transform and process stage
- Pulls raw data from S3 using Xcom. Assigns a sentiment index to every title and the timestamp, transforms data with Pandas.
  Loads processed data to processed S3 temporary bucket.

** Load stage
- Pulls processed data from S3 bucket
- Loads data to BigQuery

** Visualization dashboard with Looker Studio


Image of the dashboard itself

<img width="789" alt="Screenshot 2024-12-11 at 21 01 50" src="https://github.com/user-attachments/assets/6e321138-2cc4-4614-8526-3947f4c1a158" />


Link to the dashboard - https://lookerstudio.google.com/reporting/13f6cdf2-c88b-4feb-8bba-a24306a510b4

Throughout the iterations of my pet project I have tried a lot of tools and even though some of them weren’t used there, I learned a lot. Here’s the rundown:

- Apache NiFi. Great GUI, easy to use processors for various data manipulations. However, the sentiment analysis was very cumbersome to perform. Python scripts are deprecated in NiFi and Groovy, the alternative for sentiment processing, didn’t work as intended
- Apache Kafka. I learned how to launch the tool, create connections from DB to Kafka and vice versa. Ended up, not using it, as I figured it might have been technical overkill for the purpose of the project.
- Grafana. I found it not so useful and simple to use as some BI visualization tools. It just didn’t fit the usage case for me.
- MongoDB. Decided go with PostgreSQL as it's open-source and could be deployed locally in Docker.
- Although I considered using Plotly or pre-made JavaScript graphs, I was more interested in trying out BI tools, which led me to explore Looker, Tableau, and ultimately, Apache Superset.




What I would like to do:
- add a separate dashboard that would analyze scraped contents of news articles, not just titles
- add a bias analysis
- add more news outlets to analyze (also have scripts ready for Nur.kz, Tengrinews.kz and Moscowtimes)
- try using the tools I put away earlier


I am open to feedback and suggestions to add/improve something, don't hesitate.
