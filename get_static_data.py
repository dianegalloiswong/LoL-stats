import json

import riotwatcher
import data_path


def get_id_to_name(riot:riotwatcher.RiotWatcher):
    champs_by_id = riot.static_get_champion_list(data_by_id=True)['data']
    id_to_name = dict()
    for champ in champs_by_id:
        id_to_name[champs_by_id[champ]['id']] = champs_by_id[champ]['name']
    with open(data_path.file_champion_id_to_name,'w') as f:
        json.dump(id_to_name, f)
    return id_to_name


def make_columns_to_id(id_to_name):
    columns_to_id = dict()
    c = 0
    for id in id_to_name:
        columns_to_id[c] = id
        c += 1
    with open(data_path.columns_to_id,'w') as f:
        json.dump(columns_to_id, f)
    return columns_to_id

def main():
    id_to_name = get_id_to_name(riotwatcher.RiotWatcher())
    make_columns_to_id(id_to_name)

if __name__ == '__main__':
    main()