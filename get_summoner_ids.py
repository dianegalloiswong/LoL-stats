import json
from riotwatcher import LoLException, RiotWatcher

report_freq = 100


def match_id_to_summoner_ids(riot, match_id):
    riot.wait()
    try:
        match_detail = riot.get_match(match_id)
        return [participantIdentity['player']['summonerId'] for participantIdentity in match_detail['participantIdentities']]
    except LoLException as e:
        print('LoLException: '+str(e)+', in match_id_to_summoner_ids with match_id = '+str(match_id))
        return []

def summoner_id_to_match_ids(riot, summoner_id):
    riot.wait()
    try:
        match_history = riot.get_match_history(summoner_id, ranked_queues=['RANKED_SOLO_5x5'])
        return [match_summary['matchId'] for match_summary in match_history['matches'] if match_summary['season']=='SEASON2015']
    except LoLException as e:
        print('LoLException: '+str(e)+', in summoner_id_to_match_ids with summoner_id = '+str(summoner_id))
        return []

def get_summoner_ids(riot, n, initial_summoner_id):
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
            if 5*len(match_ids) > n:
                break
        pending_summoner_ids.clear()
        for m_id in pending_match_ids:
            for s_id in match_id_to_summoner_ids(riot, m_id):
                if s_id not in summoner_ids:
                    summoner_ids.add(s_id)
                    if len(summoner_ids)%report_freq==0:
                        print(str(len(summoner_ids))+' done')
                    pending_summoner_ids.append(s_id)
            if len(summoner_ids) > n:
                break
        pending_match_ids.clear()
    return summoner_ids

def store_summoner_ids(filename, riot, n, initial_summoner_id):
    summoner_ids = list(get_summoner_ids(riot, n, initial_summoner_id))
    f = open(filename, 'w')
    json.dump(summoner_ids,f)
    f.close()



if __name__ == '__main__':
    f = open('riot_api_key', 'r')
    key = json.load(f)
    f.close()
    riot = RiotWatcher(key)
    store_summoner_ids('test_get_summoner_ids', riot, 20, 30890339)
