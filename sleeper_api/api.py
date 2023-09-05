import json
from pathlib import Path
from time import time
from typing import Any, Optional, Union

from sleeper_api.session import APISession


class SleeperAPI:
    # https://docs.sleeper.app/
    def __init__(self, raise_errors: bool = True, **kwargs) -> None:
        self._session = APISession(raise_errors, **kwargs)
        self._nfl_state = self.get_nfl_state()

    _base_url = "https://api.sleeper.app/v1"

    def _get_week_count(self, season: Union[str, int]) -> int:
        season = int(season)
        create_season = int(self._nfl_state["league_create_season"])
        current_season = int(self._nfl_state["season"])
        current_week = self._nfl_state["leg"]
        season_type = self._nfl_state["season_type"]

        if season > create_season:
            raise ValueError(f"The {season} season has not started yet!")
        elif season == current_season:
            return current_week
        elif season == create_season and season_type == "regular":
            return current_week
        elif 2021 <= season < current_season:
            return 18
        elif season < 2021:
            return 17
        else:
            return 1

    def get_nfl_state(self) -> dict:
        url = f"{self._base_url}/state/nfl"
        data = self._session.call(url, log_null=True)
        if not (data and isinstance(data, dict)):
            raise ValueError("Failed to get NFL State.")
        return data

    def get_league(self, league_id: str) -> Optional[dict[str, Any]]:
        url = f"{self._base_url}/league/{league_id}"
        return self._session.call(url, log_null=True)

    def get_league_history(self, league_id: str) -> list[dict[str, Any]]:
        leagues_data = []
        while league_id and league_id != "0":
            league_data = self.get_league(league_id)
            if not league_data:
                break
            leagues_data.append(league_data)
            try:
                league_id = league_data.get("previous_league_id", "")
            except TypeError:
                self._session.logger.error(
                    f"{self._base_url}/league/{league_id}", 200, exc_info=True
                )
                break
        return leagues_data

    def get_user_leagues(
        self, user_id: Union[str, int], season: Union[str, int, None] = None
    ) -> Optional[list[dict[str, Any]]]:
        if season is None:
            season = self._nfl_state["season"]  # default to current season
        url = f"{self._base_url}/user/{user_id}/leagues/nfl/{season}"
        return self._session.call(url, log_null=False)

    def get_all_user_leagues(self, user_id: Union[str, int]) -> list[dict[str, Any]]:
        current_season = int(self._nfl_state["league_create_season"])
        season = 2017  # Sleeper's first season
        leagues_list = []
        while season <= current_season:
            data = self.get_user_leagues(user_id, season)
            leagues_list += data or []
            season += 1
        if not leagues_list:
            self._session.logger.missing([user_id], "User has no leagues!")
        return leagues_list

    def get_user(self, user_id: str) -> Optional[dict[str, Any]]:
        url = f"{self._base_url}/user/{user_id}"
        return self._session.call(url, log_null=True)

    def get_users(self, league_id: str) -> Optional[list[dict[str, Any]]]:
        url = f"{self._base_url}/league/{league_id}/users"
        return self._session.call(url, log_null=True)

    def get_rosters(self, league_id: str) -> Optional[list[dict[str, Any]]]:
        url = f"{self._base_url}/league/{league_id}/rosters"
        return self._session.call(url, log_null=True)

    def get_transactions(
        self, league_id: str, week: int
    ) -> Optional[list[dict[str, Any]]]:
        url = f"{self._base_url}/league/{league_id}/transactions/{week}"
        return self._session.call(url, log_null=False)

    def get_season_transactions(self, league_id: str) -> list[dict[str, Any]]:
        transactions_list = []
        for week in range(1, 19):
            transactions = self.get_transactions(league_id, week)
            if transactions:
                transactions_list += transactions
        return transactions_list

    def get_matchups(self, league_id: str, week: int) -> Optional[list[dict[str, Any]]]:
        url = f"{self._base_url}/league/{league_id}/matchups/{week}"
        return self._session.call(url, log_null=True)

    def get_season_matchups(self, league_id: str) -> dict[int, list[dict[str, Any]]]:
        matchups_dict = {}
        for week in range(1, 19):
            matchups = self.get_matchups(league_id, week)
            if matchups:
                matchups_dict[week] = matchups
        return matchups_dict

    def get_user_drafts(
        self, user_id: str, season: Union[str, int, None] = None
    ) -> Optional[list[dict]]:
        if season is None:
            season = self._nfl_state["season"]
        url = f"{self._base_url}/user/{user_id}/drafts/nfl/{season}"
        return self._session.call(url, log_null=True)

    def get_drafts(self, league_id: str) -> Optional[list[dict]]:
        url = f"{self._base_url}/league/{league_id}/drafts"
        return self._session.call(url, log_null=True)

    def get_draft(self, draft_id: str) -> Optional[dict]:
        url = f"{self._base_url}/draft/{draft_id}"
        return self._session.call(url, log_null=True)

    def get_draft_picks(self, draft_id: str) -> Optional[list[dict]]:
        url = f"{self._base_url}/draft/{draft_id}/picks"
        return self._session.call(url, log_null=True)

    def get_players(
        self,
        *,
        filepath: Union[str, Path] = "players.json",
        save_local: bool = True,
        force_update: bool = False,
        **kwargs,
    ) -> Optional[dict]:
        url = f"{self._base_url}/players/nfl"
        filepath = Path(filepath)
        cache_file_exists = filepath.is_file()

        if not save_local:
            return self._session.call(url, log_null=True)

        if (
            force_update
            or not cache_file_exists
            or time() < filepath.stat().st_mtime + 86400  # file older than one day
        ):
            data = self._session.call(url, log_null=True)
            with open(filepath, "w") as f:
                json.dump(data, f, **kwargs)
            return data

        with open(filepath, "r") as f:
            return json.load(f, **kwargs)
