import unittest

from urllib.parse import urljoin
from elastalert_tools.datahub import *


class TestRequestor(unittest.TestCase):
    def setUp(self):
        self.testurl = 'https://jsonplaceholder.typicode.com/'
        self.requestor = Requestor({'Authorization': 'token test'}, self.testurl)
        
        
    def test_get(self):
        res = self.requestor.get('posts')
        assert isinstance(res, list)
    
    def test_post(self):
        res = self.requestor.post('posts')
        assert isinstance(res, dict)
        
    def test_delete(self):
        route = urljoin(self.testurl, 'posts/1')
        res = self.requestor.delete(route)
        assert isinstance(res, dict)
        
class TestDatahub(unittest.TestCase):
    def setUp(self):
        self.datahub = Datahub()
    
    def test_users(self):
        assert isinstance(self.datahub.users, Requestor)