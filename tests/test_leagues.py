import os
import unittest

from sleeper_api import SleeperAPI

league_id = os.environ["TEST_LEAGUE_ID"]
api = SleeperAPI()


class TestLeagues(unittest.TestCase):
    def test_get_league(self):
        league = api.get_league(league_id)
        self.assertTrue(isinstance(league, dict) and league)

    def test_get_league_history(self):
        league_history = api.get_league_history(league_id)
        self.assertTrue(isinstance(league_history, list) and league_history)

    def test_get_users(self):
        users = api.get_users(league_id)
        self.assertTrue(isinstance(users, list) and users)

    def test_get_rosters(self):
        rosters = api.get_rosters(league_id)
        self.assertTrue(isinstance(rosters, list) and rosters)

    def test_get_transactions(self):
        transactions = api.get_transactions(league_id, 1)
        self.assertTrue(isinstance(transactions, list) and transactions)

    def test_get_season_transactions(self):
        season_transactions = api.get_season_transactions(league_id)
        self.assertTrue(isinstance(season_transactions, list) and season_transactions)

    def test_get_matchups(self):
        matchups = api.get_matchups(league_id, 1)
        self.assertTrue(isinstance(matchups, list) and matchups)

    def test_get_season_matchups(self):
        season_matchups = api.get_season_matchups(league_id)
        self.assertTrue(isinstance(season_matchups, dict) and season_matchups)

    def get_drafts(self):
        drafts = api.get_drafts(league_id)
        self.assertTrue(isinstance(drafts, dict) and drafts)


if __name__ == "__main__":
    unittest.main()
