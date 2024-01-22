import requests
from bs4 import BeautifulSoup
import re
import sys
from datetime import datetime

from general_functions import *
import os

def get_data_from_url(url):
	return requests.get(url)


def get_list_of_items_from_file(filename):
	f = open(filename, "r")
	a = f.readlines()
	list_of_files = [i.strip("\n") for i in a]
	f.close()
	return a

os.chdir("/home/ubuntu/los_angeles_walkability_score")

print("datetime is now:")
print(datetime.now())


page = get_data_from_url("https://data.lacity.org/Transportation/LADOT-Parking-Meter-Occupancy-Archive/cj8s-ivry/about_data")

soup = BeautifulSoup(page.content, "html.parser")
tables = soup.find_all('script')
script_item_csvs = tables[-3]
string_val = script_item_csvs.get_text()

val = re.findall(r'files/.{8}-.{4}-.{4}-.{4}-.{12}\?download=true\\u0026filename=Sensor Transactions_.{4}_.{2}.csv', string_val)



# get parking data (needed for lat long)

app_val_token = get_secret("app_token_val_official", "us-east-1")
lacity_password = get_secret("data_lacity_password_official", "us-east-1")
print("test0")

client = connect_to_la_city_api(app_val_token, lacity_password)
results2 = client.get_all("s49e-q6j2")


print("test1")

parking_dictionary = {}

for i in results2:
	space_id = i['spaceid']
	parking_dictionary[space_id] = i['latlng']


print("test3")

# merge the two data

processed_files = get_list_of_items_from_file("processed_URLs.txt")
print("Processed files is ")
print(processed_files)

print("test4")

prefix_url = "https://data.lacity.org/api/views/cj8s-ivry/"
psql_password = get_secret("psql_password_official", "us-east-1")
conn = connect_to_psql_db(psql_password)



print("test5")

f = open("last_index.txt", "r")
last_index = f.readline()
last_index = 0 if last_index == '' else int(last_index)
f.close()


print("test6")


f2 = open("last_index.txt", "w")
f2.write(str(last_index))


for i in val: # change index
	csv_file = prefix_url + i



	if csv_file not in processed_files:
		print("processing URL {};\nlast index is {}".format(csv_file, last_index))


		response = requests.get(csv_file)
		data = response.text.split("\n")

		for j in range(last_index, len(data)):
			try:
				row_data = data[j].split("\n")[0]
				row_data = row_data.split(",")
				space_id = row_data[0]
				event_time_utc = row_data[2]
				state = row_data[3].strip("\r")
				lat = parking_dictionary[space_id]['latitude']
				lng = parking_dictionary[space_id]['longitude']

				insert_sql_statement = "INSERT INTO parking_data (space_id, lat, lng, event_time, occupancy_state) VALUES (%s, %s, %s, %s, %s);"
				params = (space_id, lat, lng, event_time_utc, state)

				print("{} ({}/{}): running sql...".format(csv_file[-31:], j, len(data)))
				run_sql(conn, insert_sql_statement, params)

			except Exception as ke:
				print(ke)

			
			f2.seek(0)
			f2.truncate()
			f2.write(str(j))

		f = open("processed_URLs.txt","a")
		f.write(csv_file + "\n")
		f.close()
		last_index = 0


f2.close()

