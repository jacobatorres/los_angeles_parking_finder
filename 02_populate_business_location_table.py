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
# 585000 rows as of this writing
for i in range(0,102800, limit_value):
	break

	try:
		print("limit is {}, offset is {}".format(limit_value, i))
		business_results_2 = get_data_from_la_city(client, data_code_dictionary['business'][0], limit_value, i, "location_account ASC")
		results_df_2 = pd.DataFrame.from_records(business_results_2)

		mini_counter = 0
		while mini_counter < limit_value:

			try:
				location_id = results_df_2.loc[mini_counter]['location_account']
				naics_raw = str(results_df_2.loc[mini_counter]['naics'])
				naics = int(float(naics_raw))
				lat = float(results_df_2.loc[mini_counter]['location_1']['latitude'])
				lng = float(results_df_2.loc[mini_counter]['location_1']['longitude'])
				business_name = results_df_2.loc[mini_counter]['business_name']

				if naics_raw[:2] in ['42', '44', '45', '71', '81']:		
					insert_sql_statement = "INSERT INTO business_location (location_id, naics_code, lat, lng, business_name) VALUES (%s, %s, %s, %s, %s);"
					params = (location_id, naics, lat, lng, business_name)
					run_sql(conn, insert_sql_statement, params)

			except Exception as e:
				print("Skipping, error when running SQL: {}".format(e))

			mini_counter += 1
	except Exception as e:
		print("probably indexing error, skipping")
		break


print("update to add in column")
populate_geom_column_sql = "UPDATE business_location SET geom = ST_SetSRID(ST_MakePoint(lng,lat), 4326)"
run_sql(conn, populate_geom_column_sql)


