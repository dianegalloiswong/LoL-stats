import os
import json
import unittest

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
    # print(str(len(summoner_ids))+' summoner ids collected')
    return summoner_ids


def store_summoner_ids(filename, riot, n, initial_summoner_id):
    """
    Collects at least n summoner ids, starting with initial_summoner_id,
     and stores them in a new file filename.
    :param filename:
    :param riot:
    :param n:
    :param initial_summoner_id:
    :return:

    >>> import riotwatcher, data_path
    >>> riot = riotwatcher.RiotWatcher()
    >>> store_summoner_ids(data_path.test_store_summoner_ids_result, riot, 20, 30890339)
    """
    summoner_ids = list(collect_summoner_ids(riot, n, initial_summoner_id))
    with open(filename, 'w') as f:
        json.dump(summoner_ids, f)


def collect_master_summoner_ids():
    riot = riotwatcher.RiotWatcher()
    riot.wait()
    resp = riot.get_master()
    ids = [int(entry['playerOrTeamId']) for entry in resp['entries']]
    print(len(ids))
    print(ids)
    with open(data_path.summoner_ids_master, 'w') as f:
        json.dump(ids, f)


# class SummonerIds:
#     def __init__(self, data, n_ids_min, initial_summoner_id, name=None):
#         self.data = list(data)
#         self.actual_n_ids = len(data)
#         self.n_ids_min = n_ids_min
#         self.initial_summoner_id = initial_summoner_id
#         if name is None:
#             name = 'init{}min{}'.format(initial_summoner_id, n_ids_min)
#         self.name = name
#         self.filename = os.path.join(data_path.summoner_ids_dir, name)
#
#     def to_dict(self):
#         d = {
#                 'actual_n_ids': self.actual_n_ids,
#                 'name': self.name,
#                 'initial_summoner_id': self.initial_summoner_id,
#                 'n_ids_min': self.n_ids_min,
#                 'data': json.dumps(self.data)
#             }
#         return d
#
#     def dump(self):
#         d = self.to_dict()
#         with open(self.filename, 'w') as f:
#             json.dump(d, f, indent=2)
#
#     def to_dict1(self):
#         d = {
#                 'actual_n_ids': self.actual_n_ids,
#                 'name': self.name,
#                 'initial_summoner_id': self.initial_summoner_id,
#                 'n_ids_min': self.n_ids_min
#             }
#         return d
#
#     def dump1(self):
#         d = self.to_dict1()
#         s1 = json.dumps(d)
#         s2 = json.dumps(self.data)
#         with open(self.filename, 'w') as f:
#             f.write(s1 + '\n' + s2)
#
# def summoner_ids_draft(n_ids_min, initial_summoner_id, name=None, riot=None):
#     if riot is None:
#         riot = riotwatcher.RiotWatcher()
#     data = collect_summoner_ids(riot, n_ids_min, initial_summoner_id)
#     si = SummonerIds(data,n_ids_min,initial_summoner_id,name=name)
#     si.dump1()
#     return si


class SummonerIds:
    def __init__(self, initial_summoner_id, n_ids_min, name, data):
        self.initial_summoner_id = initial_summoner_id
        self.n_ids_min = n_ids_min
        self.name = name
        self.filename = SummonerIds.name_to_filename(name)
        self.data = data
        self.actual_n_ids = len(data)

    @staticmethod
    def collect(initial_id=30890339, n_min=10, name=None, riot=None):
        if name is None:
            name = 'init{}min{}'.format(initial_id, n_min)
        if riot is None:
            riot = riotwatcher.RiotWatcher()
        data = collect_summoner_ids(riot, n_min, initial_id)
        data = list(data)
        summoner_ids = SummonerIds(initial_id, n_min, name, data)
        return summoner_ids

    @staticmethod
    def load(name):
        filename = SummonerIds.name_to_filename(name)
        with open(filename, 'r') as f:
            s = f.readline()
            d = json.loads(s)
            data = json.load(f)
        summoner_ids = SummonerIds(d['initial_summoner_id'], d['n_ids_min'], name, data)
        return summoner_ids

    @staticmethod
    def name_to_filename(name):
        filename = os.path.join(data_path.summoner_ids_dir, name)
        return filename

    def to_dict(self):
        d = {'actual_n_ids': self.actual_n_ids,
             'name': self.name,
             'initial_summoner_id': self.initial_summoner_id,
             'n_ids_min': self.n_ids_min}
        return d

    def dump(self):
        d = self.to_dict()
        s = json.dumps(self.data)
        with open(self.filename, 'w') as f:
            json.dump(d, f)
            f.write('\n' + s)

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

    # import doctest
    # doctest.testmod()


