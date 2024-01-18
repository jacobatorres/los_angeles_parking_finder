import boto3
from sodapy import Socrata
import pandas as pd
import psycopg2

def get_secret(secret_name, region):
	print("stats are  {} {}".format(secret_name, region))

	session = boto3.session.Session()
	client = session.client(
		service_name='secretsmanager',
		region_name=region,
	)


	try:
		get_secret_value_response = client.get_secret_value(
			SecretId=secret_name
		)
	except ClientError as e:
		if e.response['Error']['Code'] == 'ResourceNotFoundException':
			print("The requested secret " + secret_name + " was not found")
		elif e.response['Error']['Code'] == 'InvalidRequestException':
			print("The request was invalid due to:", e)
		elif e.response['Error']['Code'] == 'InvalidParameterException':
			print("The request had invalid params:", e)
		elif e.response['Error']['Code'] == 'DecryptionFailure':
			print("The requested secret can't be decrypted using the provided KMS key:", e)
		elif e.response['Error']['Code'] == 'InternalServiceError':
			print("An error occurred on service side:", e)
	else:
		# Secrets Manager decrypts the secret value using the associated KMS CMK
		# Depending on whether the secret was a string or binary, only one of these fields will be populated
		if 'SecretString' in get_secret_value_response:
			text_secret_data = get_secret_value_response['SecretString']
		else:
			binary_secret_data = get_secret_value_response['SecretBinary']

		# Your code goes here.

	return get_secret_value_response['SecretString']

def connect_to_la_city_api(app_val_token, lacity_password):
	# LADOT Parking Meter Occupancy
	client = Socrata(
			"data.lacity.org",
			app_val_token,
			username="jacobangelo_torres@yahoo.com",
			password=lacity_password,
			timeout=10
	)
	return client

def get_data_from_la_city(client, url_suffix, limit_value):
	return client.get(url_suffix, limit=limit_value)

def show_data_sample(data, columns):
	results_df = pd.DataFrame.from_records(data)
	print(results_df[columns])

def connect_to_psql_db(psql_password):
	client = boto3.client('rds')
	response = client.describe_db_instances()
	db_endpoint = ""
	for db_instance in response['DBInstances']:
		db_endpoint = db_instance['Endpoint']['Address']
		if "terraform" in db_endpoint:
			break 

	try:
		conn = psycopg2.connect(
				host=db_endpoint,
				database="tutorial", 
				user="da_admin",
				password=psql_password)
		print("was able to connect")
	except Exception as e:
		print("error when connecting")
		print(e)
		exit(1)

	return conn

def run_sql(conn, sql_to_run):
	try:
		cur = conn.cursor()
		cur.execute(sql_to_run)
		conn.commit()
		print("sql successfully ran:")
		print(sql_to_run)
	except Exception as e:
		print("error when running the sql: ")
		print(sql_to_run)
		print(e)
		exit(1)

