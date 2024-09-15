# from data_ingestor import *
# import requests

print("HE HEY EH HEY hEYEWFEWJFNEWKJ")
# Define the base URL
# base_url = "https://newssentimentdashboard.onrender.com"
#
# #Make a GET request to /ingest_data
#
# response_extract = requests.get(f"{base_url}/ingest_data")
# print("Hello, haven't entered if clause yet")
# # Check if the request was successful
# if response_extract.status_code == 200:
#     print("Hi,  200")
#     print("GET /ingest_data response: success")
#     print(response_extract.json())  # Print the received data
# else:
#     print(f"GET request failed with status code {response_extract.status_code}")
#

# #
# #
# # Prepare data for the POST request
# data_to_send = response_extract.json()  # Using the data received from the GET request
# # # Make a POST request to /process_data
# response_transform = requests.post(f"{base_url}/process_data", json=data_to_send)
# #print(response_transform.text)
# # Check if the request was successful
# if response_transform.status_code == 200:
#     print("POST /process_data response: success")
# else:
#     print(f"POST request failed with status code {response_transform.status_code}")
#
# # #
# # #
# # LOAD data to PostgreSQL
# data_to_send = response_transform.json()  # Using the data received from the GET request
# collection_name = "news_processed"
# data_transform = response_transform.json()
# # print(data_to_send)
# response_load_data = requests.post(f"{base_url}/load_processed_data/{collection_name}", json=data_to_send)
# if response_load_data.status_code == 200:
#     print("POST /load_processed_data response: success")
# else:
#     print(f"POST request failed with status code {response_load_data.status_code}")
#
# #
# # # Make a POST request to /process_data
# response_freq_words = requests.post(f"{base_url}/get_word_frequency", json=data_transform)
# # print(response_freq_words.text)
# # Check if the request was successful
# if response_freq_words.status_code == 200:
#     print("POST /get_word_frequency response: success")
# else:
#     print(f"POST request failed with status code {response_freq_words.status_code}")
#
#
# data_to_load = response_freq_words.json()
# collection_name = "news_frequency_words"
# response_load_data = requests.post(f"{base_url}/load_processed_data/{collection_name}", json=data_to_load)
# if response_load_data.status_code == 200:
#     print("POST /load_processed_data response: success")
# else:
#     print(f"POST request failed with status code {response_load_data.status_code}")
# #
