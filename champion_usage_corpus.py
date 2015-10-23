from __future__ import with_statement
from gensim import interfaces, utils
from my_gensim_dict import MyDictionary
from collect_champions_usage import ChampionsUsage
import logging
import json
logger = logging.getLogger('champion_usage_corpus')

class ChampionUsageCorpus(interfaces.CorpusABC):
    def __init__(self, input=None):
        super(ChampionUsageCorpus, self).__init__()
        self.input = input
        self.dictionary = MyDictionary()
        self.metadata = False
        if input is not None:
            self.dictionary.add_documents(self.get_texts())
        else:
            logger.warning("No input document stream provided; assuming "
                           "dictionary will be initialized some other way.")

    def getstream(self):
        return utils.file_or_filename(self.input)

    def get_texts(self):
        """
        Iterate over the collection, yielding one document at a time. A document
        is a sequence of words (strings) that can be fed into `Dictionary.doc2bow`.

        Override this function to match your input (parse input files, do any
        text preprocessing, lowercasing, tokenizing etc.). There will be no further
        preprocessing of the words coming out of this function.
        """
        # take a dictionary, make sure champion ids are properly encoded strings

        if not isinstance (self.input, ChampionsUsage):
            raise TypeError("expecting ChampionsUsage")
        for summno, doc in enumerate(self.input):
            #remove total games played
            if '0' in doc:
                del doc['0']
            yield doc
        #check encoding ?

    def __iter__(self):
        """
        The function that defines a corpus.

        Iterating over the corpus must yield sparse vectors, one for each document.
        """
        for text in self.get_texts():
            if self.metadata:
                yield self.dictionary.doc2bow(text[0], allow_update=False), text[1]
            else:
                yield self.dictionary.doc2bow(text, allow_update=False)


    def __len__(self):
        if not hasattr(self, 'length'):
            # cache the corpus length
            self.length = sum(1 for _ in self.get_texts())
        return self.length

