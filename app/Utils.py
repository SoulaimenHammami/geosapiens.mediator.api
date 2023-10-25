import os
COGNITO_region =os.environ['COGNITO_region']
COGNITO_userPoolId =os.environ['COGNITO_userPoolId']
COGNITO_client_id =  os.environ['COGNITO_client_id']

PSQL_DATABASE = os.environ['PSQL_DATABASE']
PSQL_HOST = os.environ['PSQL_HOST']
PSQL_PASSWORD = os.environ['PSQL_PASSWORD']
PSQL_PORT = os.environ['PSQL_PORT']
PSQL_USER = os.environ['PSQL_USER']
CONNECTION_MAX_OVERFLOW = os.environ['CONNECTION_MAX_OVERFLOW']
CONNECTION_POOL_SIZE = os.environ['CONNECTION_POOL_SIZE']

print("printing values")
print("PSQL_DATABASE" , PSQL_DATABASE)
print("PSQL_HOST" , PSQL_HOST)
print("PSQL_PASSWORD" , PSQL_PASSWORD)
print("PSQL_PORT" , PSQL_PORT)
print("PSQL_USER" , PSQL_USER)
print("CONNECTION_MAX_OVERFLOW" , CONNECTION_MAX_OVERFLOW)
print("CONNECTION_POOL_SIZE" , CONNECTION_POOL_SIZE)
database_url = f'postgresql://{PSQL_USER}:{PSQL_PASSWORD}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DATABASE}'
