import os
import json
import unittest
import abc

import riotwatcher
import data_path

report_freq = 100








def match_id_to_summoner_ids(riot, match_id):
    riot.wait()
    try:
        match_detail = riot.get_match(match_id)
        return [participantIdentity['player']['summonerId'] for participantIdentity in
                match_detail['participantIdentities']]
    except riotwatcher.LoLException as e:
        print('LoLException: ' + str(e) + ', in match_id_to_summoner_ids with match_id = ' + str(match_id))
        return []


def summoner_id_to_match_ids(riot, summoner_id):
    riot.wait()
    try:
        match_history = riot.get_match_list(summoner_id, ranked_queues=['RANKED_SOLO_5x5'], seasons=['SEASON2015'])
        # return [match_summary['matchId'] for match_summary in match_history['matches'] if match_summary['season']=='SEASON2015']
        return [match_summary['matchId'] for match_summary in match_history['matches']]
    except riotwatcher.LoLException as e:
        print('LoLException: ' + str(e) + ', in summoner_id_to_match_ids with summoner_id = ' + str(summoner_id))
        return []


def collect_summoner_ids(riot, n, initial_summoner_id):
    summoner_ids = set()
    match_ids = set()
    pending_summoner_ids = [initial_summoner_id]
    pending_match_ids = []
    while len(summoner_ids) < n and len(pending_summoner_ids) > 0:
        for s_id in pending_summoner_ids:
            for m_id in summoner_id_to_match_ids(riot, s_id):
                if m_id not in match_ids:
                    match_ids.add(m_id)
                    pending_match_ids.append(m_id)
            if 5 * len(match_ids) > n:
                break
        pending_summoner_ids.clear()
        for m_id in pending_match_ids:
            for s_id in match_id_to_summoner_ids(riot, m_id):
                if s_id not in summoner_ids:
                    summoner_ids.add(s_id)
                    if len(summoner_ids) % report_freq == 0:
                        print(str(len(summoner_ids)) + ' done')
                    pending_summoner_ids.append(s_id)
            if len(summoner_ids) > n:
                break
        pending_match_ids.clear()
    return summoner_ids



def collect_master_summoner_ids():
    riot = riotwatcher.RiotWatcher()
    riot.wait()
    resp = riot.get_master()
    ids = [int(entry['playerOrTeamId']) for entry in resp['entries']]
    print(len(ids))
    print(ids)
    with open(data_path.summoner_ids_master, 'w') as f:
        json.dump(ids, f)





class DataSet(metaclass=abc.ABCMeta):

    def __init__(self, name, initial_summoner_id, n_ids_min, data):
        self.name = name
        self.filename = self.name_to_filename(name)
        self.initial_summoner_id = initial_summoner_id
        self.n_ids_min = n_ids_min
        self.data = data

    @staticmethod
    @abc.abstractmethod
    def directory():
        return ''

    @classmethod
    def name_to_filename(cls, name):
        filename = os.path.join(cls.directory(), name)
        return filename

    @classmethod
    @abc.abstractmethod
    def from_dict_and_data(cls, dic, data):
        raise NotImplementedError

    @classmethod
    def load(cls, name):
        filename = cls.name_to_filename(name)
        with open(filename, 'r') as f:
            s = f.readline()
            dic = json.loads(s)
            data = json.load(f)
        x = cls.from_dict_and_data(dic, data)
        return x

    @abc.abstractmethod
    def to_dict(self):
        raise NotImplementedError

    def dump(self):
        d = self.to_dict()
        s = json.dumps(self.data)
        with open(self.filename, 'w') as f:
            json.dump(d, f)
            f.write('\n' + s)


class SummonerIds(DataSet):
    def __init__(self, initial_summoner_id, n_ids_min, name, data):
        DataSet.__init__(self, name, initial_summoner_id, n_ids_min, data)
        self.actual_n_ids = len(data)

    @staticmethod
    def directory():
        return data_path.summoner_ids_dir

    @classmethod
    def collect(cls, initial_id=30890339, n_min=10, name=None, riot=None):
        if name is None:
            name = 'init{}min{}'.format(initial_id, n_min)
        if riot is None:
            riot = riotwatcher.RiotWatcher()
        data = collect_summoner_ids(riot, n_min, initial_id)
        data = list(data)
        summoner_ids = SummonerIds(initial_id, n_min, name, data)
        return summoner_ids

    @classmethod
    def from_dict_and_data(cls, dic, data):
        summoner_ids = SummonerIds(dic['initial_summoner_id'], dic['n_ids_min'], dic['name'], data)
        return summoner_ids


    def to_dict(self):
        d = {'actual_n_ids': self.actual_n_ids,
             'name': self.name,
             'initial_summoner_id': self.initial_summoner_id,
             'n_ids_min': self.n_ids_min}
        return d


class TestSummonerIds(unittest.TestCase):
    def test(self):
        name = 'test'
        summoner_ids = SummonerIds.collect(name=name)
        summoner_ids.dump()
        summoner_ids1 = SummonerIds.load(name)
        self.assertEqual(summoner_ids.to_dict(), summoner_ids1.to_dict())
        self.assertEqual(summoner_ids.data, summoner_ids1.data)

if __name__ == "__main__":

    unittest.main()

    # name = 'test'
    # summoner_ids = SummonerIds.collect(name=name)
    # summoner_ids.dump()
    # summoner_ids1 = SummonerIds.load(name)

    # import doctest
    # doctest.testmod()


