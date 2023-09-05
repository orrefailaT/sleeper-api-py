import os
import unittest

from sleeper_api import SleeperAPI

user_id = os.environ["TEST_USER_ID"]
api = SleeperAPI()


class TestUsers(unittest.TestCase):
    def test_get_user(self):
        user = api.get_user(user_id)
        self.assertTrue(isinstance(user, dict) and user)

    def test_get_user_leagues(self):
        user_leagues = api.get_user_leagues(user_id, 2023)
        self.assertTrue(isinstance(user_leagues, list) and user_leagues)

    def test_get_all_user_leagues(self):
        all_user_leagues = api.get_all_user_leagues(user_id)
        self.assertTrue(isinstance(all_user_leagues, list) and all_user_leagues)

    def test_get_user_drafts(self):
        user_drafts = api.get_user_drafts(user_id, 2023)
        self.assertTrue(isinstance(user_drafts, list) and user_drafts)


if __name__ == "__main__":
    unittest.main()
