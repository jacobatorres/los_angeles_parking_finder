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

limit_value = 50

def get_data_from_la_city(client, url_suffix, limit, offset, orderby):
	return client.get(url_suffix, limit = limit, offset = offset, order = orderby)


# https://dev.socrata.com/docs/queries/offset
# 35200 rows as of this writing
for i in range(0,35300, limit_value):

	try:
		print("limit is {}, offset is {}".format(limit_value, i))
		business_results_2 = get_data_from_la_city(client, data_code_dictionary['parking_spot_loc'][0], limit_value, i, "SpaceID ASC")
		results_df_2 = pd.DataFrame.from_records(business_results_2)
		# print(results_df_2)

		mini_counter = 0
		while mini_counter < limit_value:

			try:
				space_id = results_df_2.loc[mini_counter]['spaceid']
				lat = float(results_df_2.loc[mini_counter]['latlng']['latitude'])
				lng = float(results_df_2.loc[mini_counter]['latlng']['longitude'])
				# print("{} {} {}".format(space_id, lat, lng))

				insert_sql_statement = "INSERT INTO parking_location (space_id, lat, lng) VALUES (%s, %s, %s);"
				params = (space_id, lat, lng)
				run_sql(conn, insert_sql_statement, params)

			except Exception as e:
				print("Skipping, error when running SQL: {}".format(e))

			mini_counter += 1
	except Exception as e:
		print("probably indexing error, skipping")
		break

populate_geom_column_sql = "UPDATE parking_location SET geom = ST_SetSRID(ST_MakePoint(lng,lat), 4326)"
run_sql(conn, populate_geom_column_sql)


