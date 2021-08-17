import json
from flask import request, _request_ctx_stack
from functools import wraps
from jose import jwt
from urllib.request import urlopen


AUTH0_DOMAIN = 'jackq.eu.auth0.com'
ALGORITHMS = ['RS256']
API_AUDIENCE = 'capstone'


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
        auth = request.headers.get('Authorization', None)

        if not auth:
            raise AuthError({
                'success': False,
                'description': 'Authorization header is expected.'
                }, 401)

        if auth:
            bearer_token = auth.split()
            if bearer_token[0].lower() != "bearer":
                raise AuthError({
                    'success': False,
                    'description': 'Bearer token not found'
            }, 401)

            elif len(bearer_token) == 1:
                raise AuthError({
                    'success': False,
                    'description': 'Bearer token not found'
            }, 401)

            elif len(bearer_token)>2:
                raise AuthError({
                    'success': False,
                    'description': 'Bearer token not found'
            }, 401)

            token = bearer_token[1]
            return token
        

def check_permissions(permission, payload):

    if permission in payload['permissions']:
        return True
    
    else:
         raise AuthError({
            'success': False,
            'description': 'Permission not found'
            }, 401)


def verify_decode_jwt(token):
    jsonurl = urlopen(f'http://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    unverified_header = jwt.get_unverified_header(token)

    rsa_key = {}

    if 'kid' not in unverified_header:
        raise AuthError({
            'success': False,
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }
    
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms = ALGORITHMS,
                audience = API_AUDIENCE,
                issuer = 'https://' + AUTH0_DOMAIN + '/'
            )

            return payload
        
        except jwt.ExpiredSignatureError:
            raise AuthError({
                'success': False,
                'description': 'Token expired',
        }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'success': False,
                'description': 'Incorrect claims'
        }, 401)

        except Exception:
            raise AuthError({
                'success': False,
                'description': 'Unable to parse authentication token'
        }, 400)
    if not rsa_key:
        raise AuthError({
            'success': False,
            'description': 'Unable to find RSA Key'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
            
        return wrapper
    return requires_auth_decorator