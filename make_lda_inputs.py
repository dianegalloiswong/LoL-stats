import numpy as np
import json
import lda
import pprint


def dict_to_inputs(summoners_to_stats:dict):
    f = open('id_to_name', 'r')
    id_to_name = json.load(f)
    f.close()
    f = open('columns_to_id', 'r')
    columns_to_id = json.load(f)
    f.close()
    # print(len(id_to_name))
    # print(len(columns_to_id))
    X = np.zeros((len(summoners_to_stats), len(id_to_name)), dtype='int32')
    l = 0
    for summ in summoners_to_stats:
        d = summoners_to_stats[summ]
        for c in range(0, len(columns_to_id)):
            X[l, c] = d.get(str(columns_to_id[str(c)]), 0)
        l = l + 1
    ids = [columns_to_id[str(c)] for c in range(0, len(columns_to_id))]
    vocab = tuple(id_to_name[str(i)] for i in ids)
    return X, vocab


if __name__ == '__main__':
    with open('champions_usage') as f:
        summoners_to_stats = json.load(f)
    X, vocab = dict_to_inputs(summoners_to_stats)
    # for i in range(0, len(summoners_to_stats)-1):
    #     print(X[i])
    # np.savetxt("champ_usage_test.csv", X, delimiter="," )
    model = lda.LDA(n_topics=5, n_iter=1000, random_state=1)
    model.fit(X)
    topic_word = model.topic_word_
    n_top_words = 20
    for i, topic_dist in enumerate(topic_word):
        topic_words = np.array(vocab)[np.argsort(topic_dist)][:-n_top_words:-1]
        print('Topic {}: {}'.format(i, ' '.join(topic_words)))
