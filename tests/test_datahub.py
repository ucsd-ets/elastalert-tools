import unittest

from urllib.parse import urljoin
from elastalert_tools.datahub import *


do_not_skip_live_tests = os.environ.get('LIVE_DATAHUB_TEST') is ''

# class TestRequestor(unittest.TestCase):
#     def setUp(self):
#         self.testurl = 'https://jsonplaceholder.typicode.com/'
#         self.requestor = Requestor({'Authorization': 'token test'}, self.testurl)
        
        
#     def test_get(self):
#         res = self.requestor.get('posts')
#         assert isinstance(res, list)
    
#     def test_post(self):
#         res = self.requestor.post('posts')
#         assert isinstance(res, dict)
        
#     def test_delete(self):
#         route = urljoin(self.testurl, 'posts/1')
#         res = self.requestor.delete(route)
#         assert isinstance(res, dict)


class BaseDatahub(unittest.TestCase):
    def setUp(self):
        self.datahub = Datahub()
        
class TestOfflineDatahub(BaseDatahub):   
    def test_users(self):
        assert isinstance(self.datahub.users, Requestor)

@unittest.skipIf(do_not_skip_live_tests, 'skipping live tests')
class TestLiveDatahub(BaseDatahub):
    
    def test_get(self):
        assert isinstance(self.datahub.users.get(), list)
        
        assert isinstance(self.datahub.users.get('test'), dict)
        
    def test_create_delete(self):
        self.datahub.users.create('test2')
        assert isinstance(self.datahub.users.get('test2'), dict)
        
        # delete the user
        assert self.datahub.users.delete('test2').status_code == 204
