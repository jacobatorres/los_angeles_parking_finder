from psql_create_tables import create_parking_location_table, create_parking_rt_table, business_location_table
from general_functions import *

app_val_token = get_secret("app_token_value", "us-east-1")
lacity_password = get_secret("data_lacity_password_value", "us-east-1")
client = connect_to_la_city_api(app_val_token, lacity_password)


psql_password = get_secret("psql_password_value", "us-east-1")
conn = connect_to_psql_db(psql_password)

# create business table, parking table, crime table
run_sql(conn, create_parking_location_table)

run_sql(conn, create_parking_rt_table)

run_sql(conn, business_location_table)

