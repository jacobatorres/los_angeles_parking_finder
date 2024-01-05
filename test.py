import pandas as pd
from sodapy import Socrata
import boto3




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


app_val_token = get_secret("app_token", "us-east-1")
lacity_password = get_secret("data_lacity_pw", "us-east-1")

# from https://dev.socrata.com/foundry/data.lacity.org/e7h6-4a3e
client = Socrata(
		"data.lacity.org",
		app_val_token,
		username="jacobangelo_torres@yahoo.com",
		password=lacity_password,
		timeout=10
)

results = client.get("e7h6-4a3e", limit=100)
print("here")
results_df = pd.DataFrame.from_records(results)



print(results_df)