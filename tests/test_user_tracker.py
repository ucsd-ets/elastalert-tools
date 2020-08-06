from elastalert_tools.user_tracker import UserTracker

import unittest, datetime, time, oo_tools

class TestUserTracker(unittest.TestCase):
    def setUp(self):
        self.ut = UserTracker()
        self.testuser = 'tuser1'

    def test_track(self):
        self.ut.track(self.testuser)
        assert isinstance(self.ut.users[self.testuser], datetime.datetime)
    
    def test_user_exists(self):
        # user doesnt exist
        assert not self.ut.user_exists(self.testuser)
        
        # user exists
        self.ut.track(self.testuser)
        assert self.ut.user_exists(self.testuser)

    def test_user_expired(self):
        self.ut.track(self.testuser)

        # user was added definitely within 3 seconds
        deltatime = datetime.timedelta(seconds=3)
        assert not self.ut.user_expired(self.testuser, deltatime)

        # testuser expired after waiting
        time.sleep(3)
        assert self.ut.user_expired(self.testuser, deltatime)

    def test_save_load(self):
        assert isinstance(self.ut, oo_tools.save.Saver)