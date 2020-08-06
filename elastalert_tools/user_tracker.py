from oo_tools.save import Saver

import datetime

class UserTracker(Saver):
    def __init__(self, filepath='/var/lib/elastalert-tools/usertracker.obj'):
        # users[username] = 'last time email sent as datetime
        self.users = {}
        self.filepath = filepath

    def track(self, user):
        self.users.update({
            user: datetime.datetime.now()
        })
    
    def user_exists(self, user):
        try:
            self.users[user]
            return True

        except KeyError:
            return False

    def user_expired(self, user, delta_time):
        try:
            last_email_sent = self.users[user]
            now = datetime.datetime.now()
            time_differential = now - last_email_sent

            if time_differential < delta_time:
                return False
            
            return True

        except KeyError:
            raise KeyError('User not tracked')