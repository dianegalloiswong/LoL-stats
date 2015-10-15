import json, riotwatcher, collect_summoner_ids, collect_champions_usage




riot = riotwatcher.RiotWatcher()


#store_summoner_ids('summoner_ids_plat', riot, 10000, 30890339)

#store_champions_usage('summoner_ids', 'champions_usage', riot)

# for i in reversed(range(10)):
#     print('i = '+str(i))
#     store_champions_usage('data/summoner_ids_plat_'+str(i), 'data/champions_usage_plat_'+str(i), riot)



#collect_summoner_ids.collect_master_summoner_ids()

from data_path import summoner_ids_master, champions_usage_master
collect_champions_usage.store_champions_usage(summoner_ids_master, champions_usage_master, riot)







