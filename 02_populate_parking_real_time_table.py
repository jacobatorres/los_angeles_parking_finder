from general_functions import *
from datetime import datetime

data_code_dictionary = {

	"business": ["6rrh-rzua", ["location_account", "naics", "primary_naics_description", "location"]],

	"parking_spot_loc": ["s49e-q6j2", ["spaceid", "latlng"]],

	"parking_spot_archived": ["cj8s-ivry", ["SpaceID", "EventTime_Local", "EventTime_UTC", "OccupancyState"]], # will scrape separately

	"parking_spot_realtime": ["e7h6-4a3e", ["spaceid", "eventtime", "occupancystate"]],

	"crime": ["amvf-fr72", ["rpt_id", "lat", "lon", "arst_date"]]

}

def get_data_from_la_city(client, url_suffix, limit, offset, orderby):
	return client.get(url_suffix, limit = limit, offset = offset, order = orderby)


app_val_token = get_secret("app_token_value", "us-east-1")
lacity_password = get_secret("data_lacity_password_value", "us-east-1")
client = connect_to_la_city_api(app_val_token, lacity_password)

psql_password = get_secret("psql_password_value", "us-east-1")
conn = connect_to_psql_db(psql_password)

limit_value = 50

# get data up until 15 mins ago
exit_flag = True
while exit_flag:

	for offsetval in range(0, 3000, limit_value):
		print("limit is {}, offsetval is {}".format(limit_value, offsetval))
		parking_rt_results = get_data_from_la_city(client, data_code_dictionary['parking_spot_realtime'][0], limit_value, offsetval, "eventtime DESC")
		results_df_2 = pd.DataFrame.from_records(parking_rt_results)

		mini_counter = 0

		while mini_counter < limit_value:
			try:
				space_id = results_df_2.loc[mini_counter]['spaceid']
				event_time = results_df_2.loc[mini_counter]['eventtime']
				occupancy_state = results_df_2.loc[mini_counter]['occupancystate']

				date_obj = datetime.strptime(event_time, '%Y-%m-%dT%H:%M:%S.%f')
				date_now = datetime.utcnow()

				diff = date_now - date_obj

				if diff.total_seconds() > 900:
					print("ok, data is older than 15 mins, exiting")
					exit_flag = False
					break

				insert_sql_statement = "INSERT INTO parking_real_time (space_id, event_time, occupancy_state) VALUES (%s, %s, %s);"
				params = (space_id, event_time, occupancy_state)
				run_sql(conn, insert_sql_statement, params)

			except Exception as e:
				print("Skipping, error when parsing this value")
				print(e)

			mini_counter += 1

		print("last data timestamp" + event_time)

		if exit_flag == False:
			break







