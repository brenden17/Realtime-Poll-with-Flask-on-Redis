import unittest
from datetime import datetime, timedelta

from extensions import *

class PollTestCase(unittest.TestCase):
    def setUp(self):
        self.PA = PollAnalytics('test')

    def _tearDown(self):
        self.PA.delete_all_events('test')

    def test_create_event(self):
        poll_item(1, 'test')
        poll_item(2, 'test')
        d = datetime.today() - timedelta(days=4)
        poll_item(3, 'test', target_time=d)
        d = datetime.today() - timedelta(days=3)
        poll_item(4, 'test', target_time=d)

    def _test_all_events(self):
        EA = EventAnalytics('test')
        EA.fetch_daily(last=7)

if __name__ == '__main__':
    unittest.main()