import json
from riotwatcher import RiotWatcher
from get_summoner_ids import store_summoner_ids
from get_champions_usage import store_champions_usage


def data_collection_test(riot):
    store_summoner_ids('test/test_get_summoner_ids', riot, 20, 30890339)
    store_champions_usage('test/test_get_summoner_ids', 'test/test_get_champions_usage', riot)

f = open('riot_api_key', 'r')
key = json.load(f)
f.close()
riot = RiotWatcher(key)

#data_collection_test(riot)

#store_summoner_ids('summoner_ids_plat', riot, 10000, 30890339)

#store_champions_usage('summoner_ids', 'champions_usage', riot)

for i in range(10):
    store_champions_usage('data/summoner_ids_plat_'+str(i), 'data/champions_usage_plat_'+str(i), riot)