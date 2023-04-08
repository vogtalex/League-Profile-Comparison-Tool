import pandas as pd
from riotwatcher import LolWatcher, ApiError
import os

api_key = os.environ['api_key']
watcher = LolWatcher(api_key)

class summoner():
    def __init__(self, username, region):
        self.username = username
        self.region = region
        self.puuid = self.find_summoner_puuid()
    
    def find_summoner_puuid(self):
        summoner_info = watcher.summoner.by_name(self.region, self.username)
        return summoner_info['puuid']
    
    def get_partial_match_history(self, num_games):
        partial_match_history = []
        iterator = 0
        match_flag = True
        while match_flag == True:
            count = num_games
            if num_games >= 100:
                count = 100
                num_games -= 100
            my_matches = watcher.match.matchlist_by_puuid(self.region, self.puuid, count=count, start=iterator)
            for match in my_matches:
                partial_match_history.append(match)
            iterator += count
            if my_matches == []:
                match_flag = False
        return partial_match_history
    
    def get_full_match_history(self):
        full_match_history = []
        iterator = 0
        match_flag = True
        while match_flag == True:
            my_matches = watcher.match.matchlist_by_puuid(self.region, self.puuid, count=100, start=iterator)
            for match in my_matches:
                full_match_history.append(match)
            iterator += 100
            if my_matches == []:
                match_flag = False
        return full_match_history
    


test_summoner = summoner('loomith', 'na1')
match_history = test_summoner.get_partial_match_history(500)

print(len(match_history))

# fetch last match detail
# last_match = full_match_history[0]
# match_detail = watcher.match.by_id(my_region, last_match)

# participants = []
# for row in match_detail['info']['participants']:
#     participants_row = {}
#     participants_row['user'] = row['summonerName']
#     participants_row['champion'] = row['championName']
#     participants_row['level'] = row['champLevel']
#     participants_row['spell1'] = row['summoner1Id']
#     participants_row['spell2'] = row['summoner2Id']
#     participants_row['win'] = row['win']
#     participants_row['kills'] = row['kills']
#     participants_row['deaths'] = row['deaths']
#     participants_row['assists'] = row['assists']
#     participants_row['totalDamageDealt'] = row['totalDamageDealt']
#     participants_row['goldEarned'] = row['goldEarned']
#     participants_row['champLevel'] = row['champLevel']
#     participants_row['totalMinionsKilled'] = row['totalMinionsKilled']
#     participants_row['item0'] = row['item0']
#     participants_row['item1'] = row['item1']
#     participants.append(participants_row)
# df = pd.DataFrame(participants)
# print(df)
# print(len(full_match_history))

# versions = watcher.data_dragon.versions_for_region(my_region)
# champions_version = versions['n']['champion']