import data_path
from gensim import models
import json
from collect_champions_usage import ChampionsUsage
from champion_usage_corpus import ChampionUsageCorpus

def make_corpus_master(info):
    with open(data_path.champions_usage_master) as f:
        summoners_to_stats=json.load(f)
    cu = ChampionsUsage(info, summoners_to_stats, True)
    print json.dumps(cu.data)
    return ChampionUsageCorpus(cu)

if __name__ == '__main__':
    d={'name' : 'test_gensim_masters'}
    corpus=make_corpus_master(d)
    with open(data_path.file_champion_id_to_name) as fid2name:
        id2name = json.load(fid2name)
    lda = models.LdaModel(corpus, id2word=corpus.dictionary,iterations=2500, num_topics=10)
    print("lda done")
    for i in range(0,10):
        t=lda.show_topic(i)
        #t=[(id2name[c].encode('ascii'),p) for (p,c) in t]
        print t

    #for doc in corpus.get_texts():
    #    print(json.dumps(doc))
