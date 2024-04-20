from general_functions import *

psql_password = get_secret("psql_password_value", "us-east-1")
conn = connect_to_psql_db(psql_password)


run_sql(conn, " truncate table parking_real_time;")