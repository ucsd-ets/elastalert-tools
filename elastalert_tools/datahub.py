"""
Handler functions for Jupyterhub's API

Do not LOG at this level, only raise errors or return if successful

Jupyterhub API specs https://jupyterhub.readthedocs.io/en/stable/_static/rest-api/index.html
"""
import requests
import os

BASEURL = 'https://datahub.ucsd.edu/hub/api'
BASEURL = os.environ['JUPYTERHUB_BASEURL']
JUPYTERHUB_API_TOKEN = os.environ['JUPYTERHUB_API_TOKEN']
HEADERS = {
    'Authorization': f'token {JUPYTERHUB_API_TOKEN}'
}
USERROUTE = BASEURL + f'/users/'

class APIError(Exception):
    pass

def get_user(username):
    try:
        userroute = USERROUTE + username
        r = requests.get(userroute, headers=HEADERS)
        result = r.json()

        result['name']
        return result
    
    except Exception as e:
        raise APIError(f'Could not find user = {username}. Error returned {str(e)}. status_code = f{result.status_code}')

def delete_user(username):
    try:
        userroute = USERROUTE + username
        r = requests.get(userroute, headers=HEADERS)
        result = r.json()

        username = result['name']
        del_user = requests.delete(userroute, headers=HEADERS)

        if del_user.ok:
            return
        else:
            raise APIError(f"Could not delete user {username}. JSON returned from delete process = {del_user}")

    except Exception as e:
        raise APIError(f'Could not find user = {username}. Error returned {str(e)}')

def create_user(username):
    try:
        userroute = USERROUTE + username
        r = requests.post(BASEURL + f'/users/{username}')
        result = r.json()

        return f'User = {username} created at {result["created"]}'
    
    except KeyError:
        return f'User = {username} already exists'
    
    except Exception as e:
        raise APIError(f'Unknown exception at datahub.create_user = {str(e)}')
