import json

import riotwatcher


report_freq = 10

def get_champions_usage_one_summoner(riot, summoner_id):
    riot.wait()
    champions = riot.get_ranked_stats(summoner_id)['champions']
    champions = [(x['id'], x['stats']) for x in champions]
    return dict([(id, st['totalSessionsPlayed']) for (id, st) in champions])

def collect_champions_usage(riot, summoner_ids):
    usage_list = []
    for id in summoner_ids:
        try:
            usage = get_champions_usage_one_summoner(riot, id)
            usage_list.append((id, usage))
            if len(usage_list)%report_freq==0:
                print(str(len(usage_list))+' done')
        except riotwatcher.LoLException as e:
            print('LoLException: '+str(e)+', in get_champions_usage_one_summoner with summoner_id = '+str(id))
    return dict(usage_list)


def store_champions_usage(filefrom, fileto, riot):
    """
    Reads a list of summoner ids from file called filefrom,
    collects number of game with each champion for each of them
    and stores this in a new file called fileto.
    :param filefrom:
    :param fileto:
    :param riot:
    :return:

    >>> from riotwatcher import RiotWatcher
    >>> from data_path import test_store_champions_usage_data, test_store_champions_usage_result
    >>> riot = RiotWatcher()
    >>> store_champions_usage(test_store_champions_usage_data, test_store_champions_usage_result, riot)
    10 done
    """
    with open(filefrom,'r') as ffrom:
        summoner_ids = json.load(ffrom)
    champions_usage = collect_champions_usage(riot, summoner_ids)
    with open(fileto, 'w') as fto:
        json.dump(champions_usage,fto)





def setup_test_data():
    import riotwatcher, collect_summoner_ids, data_path
    riot = riotwatcher.RiotWatcher()
    with open(data_path.test_store_champions_usage_data, 'w') as f:
        collect_summoner_ids.store_summoner_ids(f,riot, 1, 30890339)

if __name__ == "__main__":
    #setup_test_data()
    import doctest
    doctest.testmod()