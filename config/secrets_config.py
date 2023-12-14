import boto3
import json

# Create a Secrets Manager client
client = boto3.client('secretsmanager')

def get_secret(secret_name):
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except Exception as e:
        print(f"Error retrieving secret: {e}")
        raise e
    else:
        # Depending on whether the secret is a string or binary, one of these fields will be populated
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
            return json.loads(secret)
        else:
            binary_secret_data = get_secret_value_response['SecretBinary']
            # Your logic to handle binary data here

db_url = get_secret("MongoDbConnectionString")["mongodb_connection_string"]
candidate_key = get_secret("CandidateKey")["authflow_candidate_key"]
