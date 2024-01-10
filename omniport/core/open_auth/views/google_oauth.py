from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist
import requests
from rest_framework.decorators import action
from cryptography.fernet import Fernet
import random
import string
import datetime
import swapper
from django.contrib.auth import login, logout
from rest_framework import status
from session_auth.models import SessionMap
from core.utils.logs import get_logging_function
from session_auth.serializers.login import LoginSerializer

session_auth_log = get_logging_function('session_auth')

Person = swapper.load_model('kernel', 'Person')

from open_auth.google_oauth_env import GOOGLE_AUTH_ENV

class GoogleOAuthViewSet(ViewSet):
    @action(detail=False, methods=['get'])
    def get_authorization_code(self, request):
        key = Fernet.generate_key()
        fernet = Fernet(key)

        random_state = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(8))
        enc_state = str(fernet.encrypt(random_state.encode()))

        timestamp = str(datetime.datetime.now())
        request.session[f'gauth_state_{timestamp}'] = enc_state

        state = f"{enc_state}__timestamp__{timestamp}"
        redirect_uri = GOOGLE_AUTH_ENV['REDIRECT_URI']
        AUTH_URL = f"{GOOGLE_AUTH_ENV['OAUTH_URL']}?response_type=code&client_id={GOOGLE_AUTH_ENV['CLIENT_ID']}&redirect_uri={redirect_uri}&state={state}&scope=openid%20profile%20email"
        return redirect(AUTH_URL)
    
    @action(detail=False, methods=['get'])
    def authenticate_user(self, request):
        state_param = request.query_params.get('state')
        state_timestamp = state_param.split('__timestamp__')[1]
        state = f"{request.session[f'gauth_state_{state_timestamp}']}__timestamp__{state_timestamp}"
        if state_param != state:
            del request.session[f'gauth_state_{state_timestamp}']
            # return Response('Errored authorization grant')
            return redirect(GOOGLE_AUTH_ENV['AUTH_FRONTEND_REDIRECT_URL'])
        
        del request.session[f'gauth_state_{state_timestamp}']

        error = request.query_params.get('error')
        if error is not None:
            # return Response(error)
            return redirect(GOOGLE_AUTH_ENV['AUTH_FRONTEND_REDIRECT_URL'])
        
        auth_code = request.query_params.get('code')

        token_request_headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        token_request_data = {
            'grant_type': 'authorization_code',
            'code': auth_code,
            'client_id': GOOGLE_AUTH_ENV['CLIENT_ID'],
            'client_secret': GOOGLE_AUTH_ENV['CLIENT_SECRET'],
            'redirect_uri': GOOGLE_AUTH_ENV['REDIRECT_URI']
        }

        try:
            token_response = requests.post(
                url=GOOGLE_AUTH_ENV['OAUTH_TOKEN_URL'],
                data=token_request_data,
                headers=token_request_headers
            )
        except Exception:
            # return Response('Unable to retrieve access token')
            pass
        else:
            if token_response.status_code == 200:
                token_response_data = token_response.json()
                api_request_headers = {
                    'Authorization': f"{token_response_data['token_type']} {token_response_data['access_token']}"
                }

                try:
                    api_response = requests.get(
                        url=GOOGLE_AUTH_ENV['OAUTH_RESOURCE_URL'],
                        headers=api_request_headers
                    )
                except Exception:
                    # return Response('Unable to access user details through google')
                    pass
                else:
                    if api_response.status_code == 200:
                        api_response_data = api_response.json()

                        if api_response_data['verified_email']:
                            try:
                                person = Person.objects.get(contact_information__institute_webmail_address=api_response_data['email'])
                            except ObjectDoesNotExist:
                                # return Response('Cannot identify user')
                                pass
                            else:
                                # Couldn't login user by extracting username and password from person.user 
                                # because authenticate() function doesn't take encrypted password as password arguement

                                # After calling login here and printing request.user.is_authenticated, it shows True
                                # But when I request from frontend to check the user's authentication status, I am getting False as response
                                login(request=request, user=person.user, backend='django.contrib.auth.backends.ModelBackend')
                                # return Response("Successfully found user")
                                # print(request.user.is_authenticated)
                                return redirect(GOOGLE_AUTH_ENV['AUTH_FRONTEND_REDIRECT_URL'])

        # return Response('Unable to authenticate user')
        return redirect(GOOGLE_AUTH_ENV['AUTH_FRONTEND_REDIRECT_URL'])
    
    @action(detail=False, methods=['get'])
    def check_auth_status(self, request):
        print(request.user.is_authenticated)
        return Response(request.user.is_authenticated, status=status.HTTP_200_OK)
