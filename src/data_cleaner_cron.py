import psycopg2
import os
from datetime import datetime, timedelta


def delete_old_data():
    conn = psycopg2.connect(
        dbname= os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        host=os.getenv('DB_HOST'),  # Match the service name in Docker Compose
        port=os.getenv('DB_PORT')
    )

    cur = conn.cursor()

    # Calculate the date 30 days ago
    thirty_days_ago = datetime.now() - timedelta(days=30)
    thirty_days_ago_str = thirty_days_ago.strftime('%Y-%m-%d')  # Format date to match the timestamp format

    # Delete records older than 30 days
    cur.execute("DELETE FROM news_processed WHERE timestamp < %s", (thirty_days_ago_str,))
    cur.execute("DELETE FROM news_frequency_words WHERE timestamp < %s", (thirty_days_ago_str,))

    conn.commit()

    cur.close()
    conn.close()


if __name__ == "__main__":
    delete_old_data()
