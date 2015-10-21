from __future__ import with_statement
import gensim
from my_gensim_dict import MyDictionary


class ChampionUsageCorpus(gensim.corpora.textcorpus.TextCorpus):

    def __init__(self, input=None):
        super(ChampionUsageCorpus, self).__init__(input)
        self.dictionary = MyDictionary()

    def get_texts(self):
        """
        Iterate over the collection, yielding one document at a time. A document
        is a sequence of words (strings) that can be fed into `Dictionary.doc2bow`.

        Override this function to match your input (parse input files, do any
        text preprocessing, lowercasing, tokenizing etc.). There will be no further
        preprocessing of the words coming out of this function.
        """
        #take a dictionary, make sure champion ids are properly encoded strings
        raise NotImplementedError

    def __len__(self):
        if not hasattr(self, 'length'):
            # cache the corpus length
            self.length = sum(1 for _ in self.get_texts())
        return self.length
