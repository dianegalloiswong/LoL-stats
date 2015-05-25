import json
from riotwatcher import RiotWatcher

f = open('riot_api_key', 'r')
key = json.load(f)
f.close()

def getIdToName(riot:RiotWatcher):
    champsById = riot.static_get_champion_list(data_by_id=True)['data']
    idToName = dict()
    for champ in champsById:
            idToName[champsById[champ]['id']]=champsById[champ]['name']
    d = open('id_to_name','w')
    json.dump(idToName, d)
    d.close()

if __name__ == '__main__':
    getIdToName(RiotWatcher(key))