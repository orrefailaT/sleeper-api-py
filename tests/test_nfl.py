import unittest

from sleeper_api import SleeperAPI


api = SleeperAPI()


class TestNfl(unittest.TestCase):
    def test_nfl_state(self):
        nfl_state = api.get_nfl_state()
        self.assertTrue(isinstance(nfl_state, dict) and nfl_state)

    def test_players(self):
        players = api.get_players()
        self.assertTrue(isinstance(players, dict) and players)
