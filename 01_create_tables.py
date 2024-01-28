from psql_create_tables import create_business_data_table_txt, create_parking_data_table_txt, create_crime_data_table_txt
from general_functions import *

data_code_dictionary = {

	"business": ["r4uk-afju", ["location_account", "naics", "location"]],

	"parking_spot_loc": ["s49e-q6j2", ["spaceid", "latlng"]],

	"parking_spot_archived": ["cj8s-ivry", ["SpaceID", "EventTime_Local", "EventTime_UTC", "OccupancyState"]], # will scrape separately

	"parking_spot_realtime": ["e7h6-4a3e", ["spaceid", "eventtime", "occupancystate"]],

	"crime": ["amvf-fr72", ["rpt_id", "lat", "lon", "arst_date"]]

}


app_val_token = get_secret("app_token_value", "us-east-1")
lacity_password = get_secret("data_lacity_password_value", "us-east-1")
client = connect_to_la_city_api(app_val_token, lacity_password)

business_results = get_data_from_la_city(client, data_code_dictionary['business'][0], 10)
show_data_sample(business_results, data_code_dictionary['business'][1])

parking_spot_loc_results = get_data_from_la_city(client, data_code_dictionary['parking_spot_loc'][0], 10)
show_data_sample(parking_spot_loc_results, data_code_dictionary['parking_spot_loc'][1])

parking_spot_realtime_results = get_data_from_la_city(client, data_code_dictionary['parking_spot_realtime'][0], 10)
show_data_sample(parking_spot_realtime_results, data_code_dictionary['parking_spot_realtime'][1])

crime_results = get_data_from_la_city(client, data_code_dictionary['crime'][0], 10)
show_data_sample(crime_results, data_code_dictionary['crime'][1])


psql_password = get_secret("psql_password_value", "us-east-1")
conn = connect_to_psql_db(psql_password)

# create business table, parking table, crime table
run_sql(conn, create_business_data_table_txt)

run_sql(conn, create_parking_data_table_txt)

run_sql(conn, create_crime_data_table_txt)






