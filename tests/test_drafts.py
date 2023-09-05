import os
import unittest

from sleeper_api import SleeperAPI


draft_id = os.environ["TEST_DRAFT_ID"]
api = SleeperAPI()


class TestDrafts(unittest.TestCase):
    def test_get_draft(self):
        draft = api.get_draft(draft_id)
        self.assertTrue(isinstance(draft, dict) and draft)

    def test_get_draft_picks(self):
        draft_picks = api.get_draft_picks(draft_id)
        self.assertTrue(isinstance(draft_picks, list) and draft_picks)
