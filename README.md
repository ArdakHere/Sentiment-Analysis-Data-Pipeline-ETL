Data Engineering/Analytics pet-project, Data pipeline for ingestion of web-scraped data from news websites, processing it with Python sentiment libraries, loading it to PostgreSQL for future visualization with Python script. Orchestrated with Python. Apache Superset is used for Visualization

Resources

Link (shortened) - https://rb.gy/gl2jsz. Enter credentials, login and password are 'public', select the 'News Dashboard' dashboard.

![Data Ingestion](https://github.com/user-attachments/assets/77e7f462-f403-4f2c-97fe-23fbf7d247b1)

![Uploading Screenshot 2024-09-30 at 19.36.08.png…]()


**Development status 16.09.2024
**
Attached is the schema of the pipeline. It works as follows:
- it scrapes news titles from the popular news outlets
- assigns a sentiment index to every title and the timestamp
- analyzes the top 20 most frequent words
- loads data
- dashboard uses premade SQL queries to pull the data from database

A good acquaintance of mine suggested to me the idea of trying out data engineering/analytics a year ago. After some time, I started researching fundamental data concepts and formulating the pet project idea. Throughout the iterations of my pet project I have tried a lot of tools and even though some of them weren’t used there, I learned a lot. Here’s the rundown:

- Apache NiFi. Great GUI, easy to use processors for various data manipulations. However, the sentiment analysis was very cumbersome to perform. Python scripts are deprecated in NiFi and Groovy, the alternative for sentiment processing, didn’t work as intended
- Apache Kafka. I learned how to launch the tool, create connections from DB to Kafka and vice versa. Ended up, not using it, as I figured it might have been technical overkill for the purpose of the project.
- Apache Airflow. Took a quick glance, launched it, and then later rejected it. Again, it seemed to be too much.
- Grafana. I found it not so useful and simple to use as some BI visualization tools. It just didn’t fit the usage case for me.
- MongoDB. Decided go with PostgreSQL as it's open-source and could be deployed in docker in development.
- Although I considered using Plotly or pre-made JavaScript graphs, I was more interested in trying out BI tools, which led me to explore Looker, Tableau, and ultimately, Apache Superset.

While developing, I have tried building these data pipelines:
- for stock prices of some companies. Rejected because of the limited APIs.
- for news titles with data from news APIs. Rejected because of limited APIs.

What I would like to do:
- add a separate dashboard that would analyze scraped contents of news articles, not just titles
- add a bias analysis
- add more news outlets to analyze (also have scripts ready for Nur.kz, Tengrinews.kz and Moscowtimes)
- try using the tools I rejected earlier
- Utilize Apache Airflow for orchestration

I am open to feedback and suggestions to add/improve something, don't hesitate.
