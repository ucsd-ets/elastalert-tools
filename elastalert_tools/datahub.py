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
        
    def _parse_url(self, subroute):
            if subroute == '':
                # must strip away trailing slash
                return self.baseurl[:-1]
            
            return urljoin(self.baseurl, subroute)
        
    @property
    def baseurl(self):
        return self._baseurl
    
    @baseurl.setter
    def baseurl(self, baseurl):
        if not baseurl.endswith('/'):
            raise DatahubAPIError(f'baseurl must end with a trail slash, not = {baseurl}')
        
        self._baseurl = baseurl
    
    def get(self, subroute=''):
        try:
            url = self._parse_url(subroute)

            r = requests.get(url, headers=self.auth)
            return r.json()

        except Exception as e:
            raise DatahubAPIError(f'error = {e}')
    
    def delete(self, subroute):
        if subroute == '':
            raise DatahubAPIError('You must specify a user to create')
        r = requests.delete(urljoin(self.baseurl, subroute), headers=self.auth)
        return r
    
    def create(self, subroute):
        if subroute == '':
            raise DatahubAPIError('You must specify a user to create')

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
        return Requestor(self.auth_headers, urljoin(self.baseurl, 'users/'))
