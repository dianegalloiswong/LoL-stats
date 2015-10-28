from __future__ import print_function

from gensim import models


class MyLdaModel(models.LdaModel):
    def __init__(self, corpus, iterations = 100, num_topics = 10):
        models.LdaModel.__init__(self, corpus, id2word=corpus.dictionary,iterations=iterations, num_topics=num_topics)
        self.infos = corpus.input.infos

    def print_topic(self, topicid, topn=10, align=False):
        """
        Return the result of `show_topic`, but formatted as a single string.
        Override method of LdaModel to modify formatting.
        """
        if align:
            return 'Topic {:2d}:   '.format(topicid) + ' '.join(['{:>12s}({:.1f})'.format(word, 100*prob) for prob,word in self.show_topic(topicid, topn)])
        return 'Topic {}:   '.format(topicid) + '  '.join(['{:s}({:.1f})'.format(word, 100*prob) for prob,word in self.show_topic(topicid, topn)])

    def display_topics(self, num_topics=10, num_words=10, display_func=print):
        for s in self.print_topics(num_topics=num_topics, num_words=num_words):
            display_func(s)
