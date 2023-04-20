import requests
import datetime
import json
import random
import pprint

class RecentMatch():
    
    def __init__(self, **kwargs) -> None:
        self._match_id: int = kwargs["match_id"]
        self._hero_name, self._hero_legs, self._hero_primary_stat, self.hero_roles = self._get_hero_name(kwargs["hero_id"])
        self._gpm: int = kwargs["gold_per_min"]
        self._last_hits: int = kwargs["last_hits"]
        self._player_team: bool = self._get_player_team(kwargs["player_slot"])
        self._player_damage: int = kwargs["hero_damage"]
        self._player_healing: int = kwargs["hero_healing"]
        self._radiant_win: bool = kwargs["radiant_win"]
        self._player_win: bool = self._did_player_win()
        self._party_size: int = kwargs["party_size"]
        self._deaths: int = kwargs["deaths"]
        self._assists: int = kwargs["assists"]
        self._kills: int = kwargs["kills"]
        self._tower_damage: int = kwargs["tower_damage"]
        
    def get_match_description(self, player_name: str = False) -> dict:
        return {
            "player_win": self._player_win,
            "player_hero": self._hero_name,
            "player_damage": self._player_damage,
            "player_healing": self._player_healing,
            "player_kills": self._kills,
            "player_deaths": self._deaths,
            "player_name": player_name
        }
        
        
    def _get_player_team(self, player_slot: int) -> bool:
        """
        returns True if the player is on the radiant team, False if the player is on the dire team.
        
        player_slot: int
            The player slot of the player.
            
        """
        
        return player_slot < 128
        
    def _did_player_win(self) -> bool:
        if self._player_team == self._radiant_win:
            return True
        
        return False
        
    def _get_hero_name(self, hero_id: int) -> str | None:
        response = requests.get(f"https://api.opendota.com/api/heroes", timeout=5)
        all_heroes = json.loads(response.content)
        hero = [hero for hero in all_heroes if hero["id"] == hero_id][0]
        
        return (hero["localized_name"], hero["legs"], hero["primary_attr"], hero["roles"])



class Player():
    
    def __init__(self, api_token: str, webhook_link: str, player_id: int, player_name: str) -> None:
        
        """
        
            api_token: str
                The API token for the Steam API.
                
            webhook_link: str
                The webhook link for the Discord webhook.
                
            player_id: int
                The open dota ID of the player to be trolled.
                
            player_name: str
                The name of the player to be trolled.
                
        
        """
        
        self._api_token: str = api_token
        self._webhook_link: str = webhook_link
        self._player_id: int = player_id
        self._last_post_id: int = None
        
    def flame_time(self):
        player_recent_matches = self._api_pull()
        # pprint.pprint(player_recent_matches)
        
        parsed_matches = [RecentMatch(**match).get_match_description() for match in player_recent_matches]
        
        pprint.pprint(parsed_matches)
    
    def _api_pull(self):
        
        response = requests.get(f"https://api.opendota.com/api/players/{self._player_id}/recentMatches", 
                                timeout=5)
        
        return json.loads(response.content)
    
        
    
    def _send_message(self, message: str):
        payload = {"content": message}
        
        # requests.post(self._webhook_link, data=payload, timeout=5)
        print(payload)
    
    def _handle_last_post(self):
        pass
    
jon = Player(
    "https://api.opendota.com/api/players/201991637/recentMatches",
    "https://discordapp.com/api/webhooks/701825259510169621/dfdtTvNzUz_Z0QOwq4YV5dhslUtpKKMjNs6Aef7XwgmAbAuHqWc8ovaHTtFnepQ1f1lL",
    201991637,
    "jon"
)

jon.flame_time()