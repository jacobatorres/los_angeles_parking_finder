from general_functions import *

psql_password = get_secret("psql_password_value", "us-east-1")
conn = connect_to_psql_db(psql_password)


run_sql(conn, "CREATE INDEX IF NOT EXISTS business_location_index ON business_location using GIST (geom);")

run_sql(conn, "CREATE INDEX IF NOT EXISTS parking_location_index ON parking_location using GIST (geom);")