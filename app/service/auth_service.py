
from pycognito import Cognito
import app.Utils as utils

class AuthService:

    def __init__(self):
        pass
    def authenticate_cognito_user(self,username, password ):
        u = Cognito(utils.COGNITO_userPoolId, utils.COGNITO_client_id,
                    username=username)
        try:
            u.authenticate(password=password)
        except:
            return 'Incorrect username or password.'
        return u.access_token
