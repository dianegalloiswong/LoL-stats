from __future__ import print_function
import os
import json
import unittest
import abc

import riotwatcher
import data_path



default_report_freq = 100
default_summoner_id = 30890339
default_n_ids_min = 10

default_summoner_ids_directory = data_path.summoner_ids_dir
default_champions_usage_directory = data_path.champions_usage_dir


class DataCollector:
    __metaclass__ = abc.ABCMeta

    def __init__(self, riot=None, report_callback=None, report_freq=default_report_freq):
        if riot is None:
            riot = riotwatcher.RiotWatcher()
        self.riot = riot
        if report_callback is None:
            report_callback = print
        self.report_callback = report_callback
        self.report_freq = report_freq

class SummonerIdsCollector(DataCollector):
    def __init__(self, riot=None, report_callback=None, report_freq=default_report_freq):
        DataCollector.__init__(self, riot=riot, report_callback=report_callback, report_freq=report_freq)

    def match_id_to_summoner_ids(self, match_id):
        self.riot.wait()
        try:
            match_detail = self.riot.get_match(match_id)
            return [participantIdentity['player']['summonerId'] for participantIdentity in
                    match_detail['participantIdentities']]
        except riotwatcher.LoLException as e:
            print('LoLException: ' + str(e) + ', in match_id_to_summoner_ids with match_id = ' + str(match_id))
            return []

    def summoner_id_to_match_ids(self, summoner_id):
        self.riot.wait()
        try:
            match_history = self.riot.get_match_list(summoner_id, ranked_queues=['RANKED_SOLO_5x5'], seasons=['SEASON2015'])
            # return [match_summary['matchId'] for match_summary in match_history['matches'] if match_summary['season']=='SEASON2015']
            return [match_summary['matchId'] for match_summary in match_history['matches']]
        except riotwatcher.LoLException as e:
            print('LoLException: ' + str(e) + ', in summoner_id_to_match_ids with summoner_id = ' + str(summoner_id))
            return []

    def collect_summoner_ids(self, n_ids_min, initial_summoner_id):
        summoner_ids = set()
        match_ids = set()
        pending_summoner_ids = [initial_summoner_id]
        pending_match_ids = []
        while len(summoner_ids) < n_ids_min and len(pending_summoner_ids) > 0:
            for s_id in pending_summoner_ids:
                for m_id in self.summoner_id_to_match_ids(s_id):
                    if m_id not in match_ids:
                        match_ids.add(m_id)
                        pending_match_ids.append(m_id)
                if 5 * len(match_ids) > n_ids_min:
                    break
            del pending_summoner_ids[:]
            for m_id in pending_match_ids:
                for s_id in self.match_id_to_summoner_ids(m_id):
                    if s_id not in summoner_ids:
                        summoner_ids.add(s_id)
                        if len(summoner_ids) % self.report_freq == 0:
                            self.report_callback('Collecting summoner ids: {}/{} done'.format(len(summoner_ids), n_ids_min))
                        pending_summoner_ids.append(s_id)
                if len(summoner_ids) > n_ids_min:
                    break
            del pending_match_ids[:]
        return summoner_ids


    def make_summoner_ids(self, initial_id=default_summoner_id, n_min=default_n_ids_min, name=None):
        if name is None:
            name = 'init{}min{}'.format(initial_id, n_min)
        data = self.collect_summoner_ids(n_min, initial_id)
        data = list(data)
        summoner_ids = SummonerIds.Cons(initial_id, n_min, name, data)
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




    
class DataWrapper:
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, infos, data, name):
        self.infos = infos
        self.data = data
        self.name = name

    @staticmethod
    @abc.abstractmethod
    def default_directory():
        raise NotImplementedError

    def get_info(self, key):
        return self.infos.get(key)


class SummonerIds(DataWrapper):
    def __init__(self, dic, data):
        DataWrapper.__init__(self, dic, data, dic['name'])

    @staticmethod
    def default_directory():
        return data_path.summoner_ids_dir
    
    @classmethod
    def Cons(cls, initial_summoner_id, n_summoners_required, name, data):
        d = {'class': 'SummonerIds',
             'n_summoners': len(data),
             'name': name,
             'initial_summoner_id': initial_summoner_id,
             'n_summoners_required': n_summoners_required}
        si = SummonerIds(d, data)
        return si
        

class DataFilesHandler:
    def __init__(self, directory=None):
        self.directory = directory

    class UndefinedFilenameError(Exception):
        pass
    
    def decide_filename(self, default_name, default_directory,
                        enforce_name, enforce_directory, enforce_fullname):
        if enforce_fullname is not None:
            return enforce_fullname
        name = default_name
        directory = default_directory
        if enforce_name is not None:
            name = enforce_name
        if self.directory is not None:
            directory = self.directory
        if enforce_directory is not None:
            directory = enforce_directory
        if name is None or directory is None:
            raise self.UndefinedFilenameError
        return os.path.join(directory, name)

    def dump(self, datawrapper, enforce_name=None, enforce_directory=None, enforce_fullname=None):
        filename = self.decide_filename(datawrapper.name, datawrapper.default_directory,
                                        enforce_name, enforce_directory, enforce_fullname)
        s1 = json.dumps(datawrapper.infos)
        s2 = json.dumps(datawrapper.data)
        with open(filename, 'w') as f:
            f.write(s1+'\n'+s2)
        return filename

    def readlines(self, name=None, enforce_directory=None, fullname=None):
        filename = self.decide_filename(None, None, name, enforce_directory, fullname)
        with open(filename, 'r') as f:
            s1 = f.readline()
            s2 = f.readline()
        return s1, s2

    def load_cls(self, cls, name=None, enforce_directory=None, fullname=None):
        s1, s2 = self.readlines(name=name, enforce_directory=enforce_directory, fullname=fullname)
        dic = json.loads(s1)
        data = json.loads(s2)
        return cls(dic, data)

    def load_infos(self, name=None, enforce_directory=None, fullname=None):
        s1, s2 = self.readlines(name=name, enforce_directory=enforce_directory, fullname=fullname)
        return json.loads(s1)

def make_ClsFilesHandler(cls):
    class ClsFilesHandler(DataFilesHandler):
        def __init__(self, directory=None):
            DataFilesHandler.__init__(self, directory=directory)
            if self.directory is None:
                self.directory = cls.default_directory()

        def load(self, name=None, enforce_directory=None, fullname=None):
            return self.load_cls(cls, name=name, enforce_directory=enforce_directory, fullname=fullname)

    return ClsFilesHandler

SummonerIdsFilesHandler = make_ClsFilesHandler(SummonerIds)




class TestCollectSummonerIds(unittest.TestCase):

    name = 'TestCollectSummonerIds'

    reports = []

    def send_report(self, s):
        self.reports.append(s)

    def test(self):
        n_min = 30
        self.reports = []
        collector = SummonerIdsCollector(report_freq=10, report_callback=self.send_report)
        summoner_ids = collector.make_summoner_ids(n_min=n_min, name=self.name)
        self.assertGreaterEqual(summoner_ids.get_info('n_summoners'), n_min)
        for i in [1,2,3]:
            j = 10*i
            self.assertEqual(self.reports.pop(0), 'Collecting summoner ids: {}/{} done'.format(j, n_min))

class TestSummonerIdsFilesHandler(unittest.TestCase):

   name = 'test'

   def test(self):
       collector = SummonerIdsCollector()
       summoner_ids = collector.make_summoner_ids(name=self.name)
       h = SummonerIdsFilesHandler()
       h.dump(summoner_ids)
       summoner_ids1 = h.load(self.name)
       self.assertEqual(summoner_ids.infos, summoner_ids1.infos)
       self.assertEqual(summoner_ids.data, summoner_ids1.data)



if __name__ == "__main__":

    unittest.main()

