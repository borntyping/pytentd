'''
Test cases for the user profile data
'''

import unittest

from tentd.data import dbm
from tentd.data.user import User

class UserDataTest(unittest.TestCase):
    '''This test case verifies the functionality of the users data objects
    '''

    @classmethod
    def setUpClass(self):
        '''Configure test database, open connections
        ''' 
        config = {
			'driver': 'sqlite',
			'path': ':memory:'
		}
        
        self.engine = dbm.connect(config)
        dbm.install_tables(self.engine)
        self.session = dbm.open_session(self.engine)
        
    @classmethod
    def tearDownClass(self):
        '''Close database connections, discard resources
        '''

    @classmethod
    def test_create_user(self):        
        u = User("James Ravenscroft")
        self.session.add(u)

        our_user = self.session.query(User).filter_by(name='James Ravenscroft').first() 
        
        return u is our_user

if __name__ == "__main__":
    unittest.main()
