"""
Handler functions for Jupyterhub's API

Do not LOG at this level, only raise errors or return if successful

Jupyterhub API specs https://jupyterhub.readthedocs.io/en/stable/_static/rest-api/index.html
"""
import requests, os
from urllib.parse import urljoin

class DatahubAPIError(Exception):
    pass

class Requestor:
    def __init__(self, auth_headers=None, baseurl=None):
        self.auth = auth_headers
        self.baseurl = baseurl
    
    def get(self, subroute):
        try:
            
            r = requests.get(urljoin(self.baseurl, subroute), headers=self.auth)
            return r.json()

        except Exception as e:
            raise DatahubAPIError(f'error = {e}')
    
    def delete(self, subroute):
        r = requests.delete(urljoin(self.baseurl, subroute), headers=self.auth)
        return r.json()
    
    def post(self, subroute):
        r = requests.post(urljoin(self.baseurl, subroute), headers=self.auth)
        return r.json()

class Datahub:
    def __init__(self):
        self.baseurl = os.environ['JUPYTERHUB_BASEURL']
        self.jupyterhub_api_token = os.environ['JUPYTERHUB_API_TOKEN']
        self.auth_headers = {
            'Authorization': f'token {self.jupyterhub_api_token}'
        }
    
    @property
    def users(self):
        return Requestor(self.auth_headers, self.baseurl)
