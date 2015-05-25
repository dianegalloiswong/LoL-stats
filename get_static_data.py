import json
from riotwatcher import RiotWatcher

f = open('riot_api_key', 'r')
key = json.load(f)
f.close()


def get_id_to_name(riot:RiotWatcher):
    champs_by_id = riot.static_get_champion_list(data_by_id=True)['data']
    id_to_name = dict()
    for champ in champs_by_id:
        id_to_name[champs_by_id[champ]['id']] = champs_by_id[champ]['name']
    d = open('id_to_name', 'w')
    json.dump(id_to_name, d)
    d.close()
    return id_to_name


def make_columns_to_id(id_to_name):
    columns_to_id = dict()
    c = 0
    for id in id_to_name:
        columns_to_id[c] = id
        c = c + 1
    c = open('columns_to_id', 'w')
    json.dump(columns_to_id, c)
    c.close()
    return columns_to_id

if __name__ == '__main__':
    m=get_id_to_name(RiotWatcher(key))
    make_columns_to_id(m)