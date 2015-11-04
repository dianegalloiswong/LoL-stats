import json

import data_path
from collect_champions_usage import ChampionsUsage
from champion_usage_corpus import ChampionUsageCorpus
from my_lda_model import MyLdaModel


def make_corpus_master():
    infos = {'name': 'test_gensim_masters'}
    with open(data_path.champions_usage_master) as f:
        summoners_to_stats = json.load(f)
    cu = ChampionsUsage(infos, summoners_to_stats, True)
    return ChampionUsageCorpus(cu)

if __name__ == '__main__':
    corpus = make_corpus_master()
    lda = MyLdaModel(corpus, iterations=10, num_topics=5)
    lda.display()
