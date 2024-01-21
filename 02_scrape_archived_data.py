import requests
from bs4 import BeautifulSoup
import re

from general_functions import *

def get_data_from_url(url):
	return requests.get(url)


def get_list_of_items_from_file(filename):
	f = open(filename, "r")
	a = f.readlines()
	list_of_files = [i.strip("\n") for i in a]
	f.close()
	return a


page = get_data_from_url("https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy-Archive/cj8s-ivry/about_data")

soup = BeautifulSoup(page.content, "html.parser")
tables = soup.find_all('script')
script_item_csvs = tables[-3]
string_val = script_item_csvs.get_text()

val = re.findall(r'files/.{8}-.{4}-.{4}-.{4}-.{12}\?download=true\\u0026filename=Sensor Transactions_.{4}_.{2}.csv', string_val)



# get parking data (needed for lat long)

app_val_token = get_secret("app_token_val_official", "us-east-1")
lacity_password = get_secret("data_lacity_password_official", "us-east-1")
client = connect_to_la_city_api(app_val_token, lacity_password)
results2 = client.get_all("s49e-q6j2")


parking_dictionary = {}

for i in results2:
	space_id = i['spaceid']
	parking_dictionary[space_id] = i['latlng']



# merge the two data

processed_files = get_list_of_items_from_file("processed_URLs.txt")

prefix_url = "https://data.lacity.org/api/views/cj8s-ivry/"
psql_password = get_secret("psql_password_official", "us-east-1")
conn = connect_to_psql_db(psql_password)

f = open("processed_URLs.txt","a")

for i in val[0:1]:
	csv_file = prefix_url + i

	print("processing " + csv_file + " ...\n")

	response = requests.get(csv_file)
	data = response.text.split("\n")

	if csv_file not in processed_files:

		for j in data[1:]:
			row_data = j.split("\n")[0]
			row_data = row_data.split(",")
			space_id = row_data[0]
			event_time_utc = row_data[2]
			state = row_data[3].strip("\r")
			try:
				lat = parking_dictionary[space_id]['latitude']
				lng = parking_dictionary[space_id]['longitude']
			except KeyError as ke:
				print(ke)
				continue


			print("space id is {}, event_time_utc is {}, state is {} lat is {} lng is {} ".format(space_id, event_time_utc, state, lat, lng))

			insert_sql_statement = "INSERT INTO parking_data (space_id, lat, lng, event_time, occupancy_state) VALUES (%s, %s, %s, %s, %s);"
			params = (space_id, lat, lng, event_time_utc, state)

			print(csv_file + ": running sql...")
			run_sql(conn, insert_sql_statement, params)

	f.write(csv_file)


f.close()

# INSERT INTO table_name(column1, column2, …)
# VALUES (value1, value2, …);


# create_parking_data_table_txt = """
# CREATE TABLE IF NOT EXISTS parking_data (
# 	space_id VARCHAR ( 7 ) PRIMARY KEY,
# 	lat float, 
# 	lng float,
# 	event_time timestamptz,
# 	occupancy_state VARCHAR ( 10 )
# );
# """

