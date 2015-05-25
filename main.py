import json
from riotwatcher import RiotWatcher
from get_champions_usage import store_champions_usage




f = open('riot_api_key', 'r')
key = json.load(f)
f.close()
riot = RiotWatcher(key)
store_champions_usage('summoner_ids', 'champions_usage', riot)