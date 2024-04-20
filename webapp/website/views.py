from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages 
from django.http import JsonResponse, HttpResponse
from geopy.distance import geodesic
from website.models import BusinessLocation
import json, math
import boto3, psycopg2

def get_secret(secret_name, region):
	print("Getting secret {} from {}".format(secret_name, region))

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


def run_sql(conn, sql_to_run, params = ()):
	try:
		cur = conn.cursor()
		cur.execute(sql_to_run, params)
		conn.commit()
		return cur.fetchall()

	except Exception as e:
		print("Error when running the sql: {}".format(e))
		conn.rollback()
		return e


def home(request):
	# if log in, show data, else just the outside

	if request.method == "POST":
		username = request.POST['username']
		password = request.POST['password']

		# authenticate
		user = authenticate(request, username=username, password=password)

		if user is not None:
			login(request, user)
			messages.success(request, "You're logged in!")
			return redirect("home")
		else:
			messages.success(request, "Error when logging in, please try again")
			return redirect("home")
	
	else:
		# just see the gomr
		return render(request, 'home.html', {})

def logout_user(request):
	logout(request)
	messages.success(request, "You're logged out!")
	return redirect('home')


def nearest_station(request):

	latitude = request.GET.get('latitude')
	longitude = request.GET.get('longitude')
	input_location = latitude, longitude


	knn_query = "SELECT ST_Distance(geom, 'SRID=4326;POINT({lng} {lat})'::geography) / 1000 as distance, lng, lat, business_name from business_location ORDER BY geom <-> 'SRID=4326;POINT({lng} {lat})'::geography limit 3".format(lng=longitude, lat=latitude)

	psql_password = get_secret("psql_password_value", "us-east-1")
	conn = connect_to_psql_db(psql_password)


	results_sql = run_sql(conn, knn_query)
	print(results_sql)

	list_to_return = []

	for datapoint in results_sql:
		datapoint_dist = datapoint[0]
		datapoint_lng = datapoint[1]
		datapoint_lat = datapoint[2]
		datapoint_business_name = datapoint[3]
		# datapoint_business_name = business name

		list_to_return.append([datapoint_lat, datapoint_lng, round(datapoint_dist, 2), datapoint_business_name])


	response = JsonResponse(list_to_return, safe=False)

	return response














