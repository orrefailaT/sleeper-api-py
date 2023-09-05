# Sleeper API Python Wrapper

Wraps the [Sleeper API](https://docs.sleeper.com/) to allow for easy use in Python projects. Features 1-to-1 mappings for all API endpoints, with helper methods for aggregating season data.

## Installation
To install, run `$ pip install git+https://github.com/orrefailaT/sleeper-api-py.git` (PYPI coming soon!)

## Usage
### Create an API class instance
```
from sleeper_api import SleeperAPI
api = SleeperAPI()
```

### User Data
```
user_id = "1234567890"

# get a user
user = api.get_user(user_id)

# get all of a user's leagues for current season
user_leagues = api.get_user_leagues(user_id)

# or for a specific season
user_leagues_2022 = api.get_user_leagues(user_id, 2022)

# or for all seasons
all_user_leagues = api.get_all_user_leagues(user_id)
```

### League Data
```
league_id = "9876543210"

# get a single league
league = api.get_league(league_id)

# get all leagues in a dynasty league
leagues = api.get_league_history(league_id)

# get all users in a league
users = api.get_users(league_id)

# get all rosters in a league
rosters = api.get_rosters(league_id)

# get transactions in a league for a single week
transactions = api.get_transactions(league_id, 1)

# or all transactions for the whole season
season_transactions = api.get_season_transactions(league_id)

# get matchups for a single week
matchups = api.get_matchups(league_id, 1)

# or all matchups for the whole season
season_matcups = api.get_season_matchups(league_id)
```

### Draft Data
```
user_id = "1234567890"
league_id = "9876543210"

# get all drafts for a user for the current season
user_drafts = api.get_user_drafts(user_id)

# or for a specific season
user_drafts_2022 = api.get_user_drafts(user_id, 2022)

# or for a specific league
league_drafts = api.get_drafts(league_id)

# get a specific draft
draft_id = league_drafts[0]["draft_id"]
draft = api.get_draft(draft_id)

# get picks for a draft
draft_picks = api.get_draft_picks(draft_id)
```

### Player Data
This API response has data on all current NFL players, and therefor is very large. The official Sleeper docs as that users only make one request to this endpoint per day, as this is how often the data is updated. To help with this, this python wrapper will default to saving the response data to a JSON file. After the intial request, using the `get_players` method read from this file instead of calling the API again, unless the file is over a day old or the user specifies to ignore the locally saved file. 
```
# get player data, hits API endpoint and saves result to a file
players = api.get_players()

# this will read from the file instead of the api
players = api.get_players()


# default filepath is `players.json`, but this can be overridden
api.get_players(filepath="/tmp/players.json")

# skip checking for a local file and hit api.
api.get_players(force_update=True)

# ignore file altogether, don't check and dont save
players = api.get_players(save_local=False)
```