import gensim
from gensim.corpora.dictionary import Dictionary
from __future__ import with_statement

from collections import Mapping, defaultdict
import sys
import logging
import itertools

from six import PY3, iteritems, iterkeys, itervalues, string_types
from six.moves import xrange
from six.moves import zip as izip
"""
Our documents are already in the form of word-frequency pairs (given as a dictionary) instead of a list of words.
This class is a gensim dictionary whose doc2bow method is adapted to this.
"""


class MyDictionary(gensim.corpora.dictionary.Dictionary):

    def doc2bow(self, document, allow_update=False, return_missing=False):
        """
        Convert `document` (a list of words) into the bag-of-words format = list
        of `(token_id, token_count)` 2-tuples. Each word is assumed to be a
        **tokenized and normalized** string (either unicode or utf8-encoded). No further preprocessing
        is done on the words in `document`; apply tokenization, stemming etc. before
        calling this method.

        If `allow_update` is set, then also update dictionary in the process: create
        ids for new words. At the same time, update document frequencies -- for
        each word appearing in this document, increase its document frequency (`self.dfs`)
        by one.

        If `allow_update` is **not** set, this function is `const`, aka read-only.
        """

        if not isinstance(document, dict):
            raise TypeError("doc2bow expects a word-frequency dictionary on input, not a single string")
        # # Construct (word, frequency) mapping.
        # counter = defaultdict(int)
        # for w in document:
        #     counter[w if isinstance(w, unicode) else unicode(w, 'utf-8')] += 1

        token2id = self.token2id
        if allow_update or return_missing:
            missing = dict((w, freq) for w, freq in iteritems(document) if w not in token2id)
            if allow_update:
                for w in missing:
                    # new id = number of ids made so far;
                    # NOTE this assumes there are no gaps in the id sequence!
                    token2id[w] = len(token2id)

        result = dict((token2id[w], freq) for w, freq in iteritems(document) if w in token2id)

        if allow_update:
            self.num_docs += 1
            self.num_pos += sum(itervalues(document))
            self.num_nnz += len(result)
            # increase document count for each unique token that appeared in the document
            dfs = self.dfs
            for tokenid in iterkeys(result):
                dfs[tokenid] = dfs.get(tokenid, 0) + 1

        # return tokenids, in ascending id order
        result = sorted(iteritems(result))
        if return_missing:
            return result, missing
        else:
            return result