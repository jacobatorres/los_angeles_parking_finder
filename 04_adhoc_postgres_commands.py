from general_functions import *
import datetime

psql_password = get_secret("psql_password_value", "us-east-1")
conn = connect_to_psql_db(psql_password)

time_30_min_ago = datetime.datetime.now() - datetime.timedelta(hours = 0.5)
time_30_min_ago_str = time_30_min_ago.strftime("%Y-%m-%d %H:%M:%S -0700")

delete_sql = """
DELETE
FROM public.parking_real_time
where event_time  < '{}'
;
""".format(time_30_min_ago_str)

print(delete_sql)
run_sql(conn, delete_sql)