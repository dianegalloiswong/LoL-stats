import sys
import os
import numpy
import json
import pprint

import lda

import data_path


def dict_to_inputs(summoners_to_stats:dict):
    with open(data_path.file_champion_id_to_name, 'r') as f:
        id_to_name = json.load(f)
    with open(data_path.columns_to_id, 'r') as f:
        columns_to_id = json.load(f)
    # print(len(id_to_name))
    # print(len(columns_to_id))
    X = numpy.zeros((len(summoners_to_stats), len(id_to_name)), dtype='int32')
    l = 0
    for summ in summoners_to_stats:
        d = summoners_to_stats[summ]
        for c in range(0, len(columns_to_id)):
            X[l, c] = d.get(str(columns_to_id[str(c)]), 0)
        l = l + 1
    ids = [columns_to_id[str(c)] for c in range(0, len(columns_to_id))]
    vocab = tuple(id_to_name[str(i)] for i in ids)
    return X, vocab

def lda_inputs(filename):
    with open(filename) as f:
        summoners_to_stats = json.load(f)
    return dict_to_inputs(summoners_to_stats)

def run_lda(filename,filetoname=None,n_topics=10,n_iter=100,n_topic_words=20):
    if filetoname==None:
        filetoname=os.path.join(data_path.lda_results,'default'+str(numpy.random.randint(0,100)))
    fileto = open(filetoname, "w")
    former_out = sys.stdout
    sys.stdout = fileto

    sys.stderr = fileto
    print('Data file: '+str(filename))
    print('{} topics, {} iterations, {} words displayed per topic'.format(n_topics, n_iter, n_topic_words))
    print()
    X, vocab = lda_inputs(filename)
    model = lda.LDA(n_topics=n_topics, n_iter=n_iter, random_state=1)
    model.fit(X)
    topic_word = model.topic_word_
    for i, topic_dist in enumerate(topic_word):
        topic_words = numpy.array(vocab)[numpy.argsort(topic_dist)][:-n_topic_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
    fileto.close()
    return filetoname

def run_lda_masters(filetoname=None,n_topics=10,n_iter=100,n_topic_words=20):
    filetoname = run_lda(data_path.champions_usage_master,
                         filetoname=filetoname,
                         n_topics=n_topics,n_iter=n_iter,n_topic_words=n_topic_words)
    return filetoname

if __name__ == '__main__':
    f = run_lda_masters()
    print(f)

    # with open('data/champions_usage_master') as f:
    #     summoners_to_stats = json.load(f)
    # with open('data/champions_usage_challenger') as f:
    #     summoners_to_stats.update(json.load(f))
    # # d = dict()
    # # for i in list(range(5))+list(range(7,10)):
    # #     d.update(fromfile('data/champions_usage_plat_'+str(i)))
    # # summoners_to_stats = d
    #
    # X, vocab = dict_to_inputs(summoners_to_stats)
    # # for i in range(0, len(summoners_to_stats)-1):
    # #     print(X[i])
    # # np.savetxt("champ_usage_test.csv", X, delimiter="," )
    # model = lda.LDA(n_topics=10, n_iter=100, random_state=1)
    # model.fit(X)
    # topic_word = model.topic_word_
    # n_top_words = 20
    # for i, topic_dist in enumerate(topic_word):
    #     topic_words = numpy.array(vocab)[numpy.argsort(topic_dist)][:-n_top_words:-1]
    #     print('Topic {}: {}'.format(i, ' '.join(topic_words)))
