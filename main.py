import json
from riotwatcher import RiotWatcher
from collect_summoner_ids import store_summoner_ids
from collect_champions_usage import store_champions_usage




riot = RiotWatcher()


#store_summoner_ids('summoner_ids_plat', riot, 10000, 30890339)

#store_champions_usage('summoner_ids', 'champions_usage', riot)

# for i in reversed(range(10)):
#     print('i = '+str(i))
#     store_champions_usage('data/summoner_ids_plat_'+str(i), 'data/champions_usage_plat_'+str(i), riot)


# riot.wait()
# resp = riot.get_master()
# ids = [int(entry['playerOrTeamId']) for entry in resp['entries']]
# print(len(ids))
# print(ids)
# from data_path import summoner_ids_master
# with open(summoner_ids_master, 'w') as f:
#     json.dump(ids, f)


from data_path import summoner_ids_master, champions_usage_master
store_champions_usage(summoner_ids_master, champions_usage_master, riot)







