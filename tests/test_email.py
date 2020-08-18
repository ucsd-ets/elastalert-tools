# import unittest, unittest.mock

# from elastalert_tools import email

# class TestEmail(unittest.TestCase):
#     def setUp(self):
#         self.mock_message = unittest.mock.MagicMock()
#         self.mock_smtp = unittest.mock.MagicMock()
        
#         self.email = email.Email()
#         # self.email.message_obj = self.mock_message
#         # self.email.mock_smtp = self.mock_smtp
        
#     def test_message_calls(self):
#         self.email.send_html('wuykimpang@ucsd.edu', 'My test email', '<h1>My message</h1>')
        
#         assert False