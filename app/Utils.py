import os
COGNITO_region =os.environ['COGNITO_region']
COGNITO_userPoolId =os.environ['COGNITO_userPoolId']
COGNITO_client_id =  os.environ['COGNITO_client_id']

PSQL_DATABASE = os.environ.get("PSQL_DATABASE")
PSQL_HOST = os.environ.get("PSQL_HOST")
PSQL_PASSWORD = os.environ.get("PSQL_PASSWORD")
PSQL_PORT = os.environ.get("PSQL_PORT")
PSQL_USER = os.environ.get("PSQL_USER")
CONNECTION_MAX_OVERFLOW = os.environ.get("CONNECTION_MAX_OVERFLOW")
CONNECTION_POOL_SIZE = os.environ.get("CONNECTION_POOL_SIZE")

database_url = f'postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DATABASE}'
