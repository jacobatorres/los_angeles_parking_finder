from general_functions import *

data_code_dictionary = {

	"business": ["6rrh-rzua", ["location_account", "naics", "primary_naics_description", "location"]],

	"parking_spot_loc": ["s49e-q6j2", ["spaceid", "latlng"]],

	"parking_spot_archived": ["cj8s-ivry", ["SpaceID", "EventTime_Local", "EventTime_UTC", "OccupancyState"]], # will scrape separately

	"parking_spot_realtime": ["e7h6-4a3e", ["spaceid", "eventtime", "occupancystate"]],

	"crime": ["amvf-fr72", ["rpt_id", "lat", "lon", "arst_date"]]

}



app_val_token = get_secret("app_token_value", "us-east-1")
lacity_password = get_secret("data_lacity_password_value", "us-east-1")
client = connect_to_la_city_api(app_val_token, lacity_password)


psql_password = get_secret("psql_password_value", "us-east-1")
conn = connect_to_psql_db(psql_password)

limit_offset_counter = 1

# https://dev.socrata.com/docs/queries/offset
for i in range(0,10, limit_offset_counter):
	business_results_2 = get_data_from_la_city(client, data_code_dictionary['business'][0], limit_offset_counter, i, "location_account ASC")
	results_df_2 = pd.DataFrame.from_records(business_results_2)

	mini_counter = 0
	while mini_counter < limit_offset_counter:

		try:
			location_id = results_df_2.loc[mini_counter]['location_account']
			naics = int(float(results_df_2.loc[mini_counter]['naics']))
			lat = float(results_df_2.loc[mini_counter]['location_1']['latitude'])
			lng = float(results_df_2.loc[mini_counter]['location_1']['longitude'])
			print("{} {} {} {}".format(location_id, naics, lat, lng))
			
			insert_sql_statement = "INSERT INTO business_location (location_id, naics_code, lat, lng) VALUES (%s, %s, %s, %s);"
			params = (location_id, naics, lat, lng)
			run_sql(conn, insert_sql_statement, params)

		except Exception as e:
			print(e)
			print("skipping")

		mini_counter += 1



populate_geom_column_sql = "UPDATE business_location SET geom = ST_SetSRID(ST_MakePoint(lng,lat), 4326)"
run_sql(conn, populate_geom_column_sql)


	# break
	# print(csv_file + ": running sql...")
	# run_sql(conn, insert_sql_statement, params)




