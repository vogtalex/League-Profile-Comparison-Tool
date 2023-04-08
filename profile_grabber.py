import pandas as pd
from riotwatcher import LolWatcher, ApiError
import os

api_key = os.environ['api_key']
watcher = LolWatcher(api_key)
my_region = 'na1'

me = watcher.summoner.by_name(my_region, 'loomith')
print(me)

full_match_history = []
my_matches = watcher.match.matchlist_by_puuid(my_region, me['puuid'], count=100)
for match in my_matches:
    full_match_history.append(match)
iterator = 100

while my_matches != []:
    my_matches = watcher.match.matchlist_by_puuid(my_region, me['puuid'], count=100, start=iterator)
    for match in my_matches:
        full_match_history.append(match)
    iterator += 100

# fetch last match detail
last_match = full_match_history[0]
match_detail = watcher.match.by_id(my_region, last_match)

participants = []
for row in match_detail['info']['participants']:
    participants_row = {}
    participants_row['user'] = row['summonerName']
    participants_row['champion'] = row['championName']
    participants_row['level'] = row['champLevel']
    participants_row['spell1'] = row['summoner1Id']
    participants_row['spell2'] = row['summoner2Id']
    participants_row['win'] = row['win']
    participants_row['kills'] = row['kills']
    participants_row['deaths'] = row['deaths']
    participants_row['assists'] = row['assists']
    participants_row['totalDamageDealt'] = row['totalDamageDealt']
    participants_row['goldEarned'] = row['goldEarned']
    participants_row['champLevel'] = row['champLevel']
    participants_row['totalMinionsKilled'] = row['totalMinionsKilled']
    participants_row['item0'] = row['item0']
    participants_row['item1'] = row['item1']
    participants.append(participants_row)
df = pd.DataFrame(participants)
# print(df)
print(len(full_match_history))

# versions = watcher.data_dragon.versions_for_region(my_region)
# champions_version = versions['n']['champion']