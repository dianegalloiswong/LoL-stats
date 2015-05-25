import json
from riotwatcher import LoLException, RiotWatcher


report_freq = 10

def get_champions_usage_one_summoner(riot, summoner_id):
    riot.wait()
    champions = riot.get_ranked_stats(summoner_id)['champions']
    champions = [(x['id'], x['stats']) for x in champions]
    return dict([(id, st['totalSessionsPlayed']) for (id, st) in champions])

def get_champions_usage(riot, summoner_ids):
    usage_list = []
    for id in summoner_ids:
        try:
            usage = get_champions_usage_one_summoner(riot, id)
            usage_list.append((id, usage))
            if len(usage_list)%report_freq==0:
                print(str(len(usage_list))+' done')
        except LoLException as e:
            print('LoLException: '+str(e)+', in get_champions_usage_one_summoner with summoner_id = '+str(id))
    return dict(usage_list)


def store_champions_usage(filefrom, fileto, riot):
    ffrom = open(filefrom, 'r')
    summoner_ids = json.load(ffrom)
    ffrom.close()
    champions_usage = get_champions_usage(riot, summoner_ids)
    fto = open(fileto, 'w')
    json.dump(champions_usage,fto)
    fto.close()




if __name__ == '__main__':
    f = open('riot_api_key', 'r')
    key = json.load(f)
    f.close()
    riot = RiotWatcher(key)
    store_champions_usage('test_get_summoner_ids', 'test_get_champions_usage', riot)
