import os
import json

import riotwatcher
import data_path
from collect_summoner_ids import DataWrapper

report_freq = 10

class ChampionsUsage(DataWrapper):
    """
    This implements champion usage as a dictionary of dictionaries (summoner ID/document).
    """

    def __init__(self, dic, data, use_names=False):
        DataWrapper.__init__(self, dic, data, dic['name'])
        if use_names:
            self.use_champion_names()

    @staticmethod
    def default_directory():
        return data_path.champions_usage_dir

    def __iter__(self):
        for summ in self.data:
            yield self.data[summ]

    def use_champion_names(self):
        for summ in self.data:
            self.data[summ]=translate_dict(self.data[summ])



def translate_dict(dic):
        with open(data_path.file_champion_id_to_name) as fdic:
            id_to_name = json.load(fdic)
        l = [(id_to_name[ch_id], dic[ch_id]) for ch_id in dic if ch_id != '0']
        return dict(l)

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

    >>> riot = riotwatcher.RiotWatcher()
    >>> store_champions_usage(data_path.test_store_champions_usage_data, data_path.test_store_champions_usage_result, riot)
    10 done
    """
    with open(filefrom,'r') as ffrom:
        summoner_ids = json.load(ffrom)
    champions_usage = collect_champions_usage(riot, summoner_ids)
    with open(fileto, 'w') as fto:
        json.dump(champions_usage,fto)


def champions_usage_draft(name, riot):
    filefrom = os.path.join(data_path.summoner_ids_dir, name)
    with open(filefrom, 'r') as ff:
        summoner_ids = json.load(ff)
    champions_usage = collect_champions_usage(riot, summoner_ids)
    return champions_usage


def setup_test_data():
    import riotwatcher, collect_summoner_ids, data_path
    riot = riotwatcher.RiotWatcher()
    with open(data_path.test_store_champions_usage_data, 'w') as f:
        collect_summoner_ids.store_summoner_ids(f,riot, 1, 30890339)

if __name__ == "__main__":
    #setup_test_data()
    import doctest
    doctest.testmod()