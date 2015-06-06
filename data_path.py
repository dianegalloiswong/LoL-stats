import os

data_dir = os.path.join(os.path.dirname(__file__),'data')

summoner_ids_master =  os.path.join(data_dir,'summoner_ids_master')
champions_usage_master =  os.path.join(data_dir,'champions_usage_master')
summoner_ids_challenger =  os.path.join(data_dir,'summoner_ids_challenger')
champions_usage_challenger =  os.path.join(data_dir,'champions_usage_challenger')

test_data_dir = os.path.join(os.path.dirname(__file__),'test_data')

test_store_summoner_ids_result = os.path.join(test_data_dir,'test_store_summoner_ids_result')
test_store_champions_usage_data = os.path.join(test_data_dir,'test_store_champions_usage_data')
test_store_champions_usage_result = os.path.join(test_data_dir,'test_store_champions_usage_result')