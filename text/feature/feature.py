#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import abstractmethod, ABCMeta #2.6以上限定
from gensim import corpora, matutils

class VsmList(object):
    def __init__(self, vsm_list):
        """
        input vsm_list: [Vsm1, Vsm2, ...]
        """
        self.vsm_list = vsm_list
        self.words_list = [vsm.text.words() for vsm in self.vsm_list]
        self.dictionary = corpora.Dictionary(self.words_list)

    def __getitem__(self, idx):
        return self.vsm_list[idx]

    def __iter__(self):  
        for vsm in self.vsm_list:
            yield vsm

    def token_list(self):
        """
        wordのリストを番号順に表示
        """
        t = self.dictionary.token2id
        # valueでsortして表示
        return [k for k, v in sorted(t.items(), key=lambda x:x[1])]

    def dist2vec(self, dist):
        """
        dist の文書ベクトル(dist)を、純粋なベクトル(list)に変換
        """
        # [(id, vec), (id, vec), ...]
        t = [(self.dictionary.token2id.get(word, 0), vec) for (word, vec) in dist.items()]
        dense = list(matutils.corpus2dense([t], num_terms=len(self.dictionary)).T[0])
        return dense

    def vector_list(self):
        """
        vectorを返却できるモデル
        """
        res = []
        for vsm in self.vsm_list:
            res.append(self.dist2vec(vsm.vec))
        return res

class Vsm(object):
    """
    ベクトル空間モデル
    TODO: のvector

    :param text - Textオブジェクト
    :param vec - {"w1": 0.21, "w2": 0.421}
    """
    def __init__(self, text, vec):
        self.text = text
        self.vec = vec
        
class Feature(object): # object継承しないとsuper呼べない
    """
    ベクトル空間モデルの特徴量 (ex: tf-idf, pmi)

    TODO: 委譲あたりのコードを修正したい
    TODO: 素性抽出器みたいな名前にしたい

    - 処理の流れ
    1. textの取得
    2. 特徴量抽出 (subclass)
    """
    def __init__(self, text_collection):
        __metaclass__ = ABCMeta

        # 委譲
        self._tc = text_collection
        deligates = "list words_list".split()
        for name in deligates:
            method = getattr(self._tc, name)
            setattr(self, name, method)

if __name__ == "__main__":
    import hymlab.text as ht
    from hymlab.text.text import *
    from hymlab.text.vital import pp
    import unittest
    import numpy as np

    class VsmTestCase(unittest.TestCase):
        def setUp(self):
            self.tc = TextCollection([
                u"我が輩は猫である。猫である。",
                u"我が輩は猫である",
                u"名前はまだ無い"])
            self.features = ht.TfIdf(self.tc).tf_idf()
            self.vsm_list = VsmList(self.features)

        def tearDown(self):
            pass
       
        def test_vector(self):
            error_decimals = 4 # 丸める桁数

            # neko = u'猫'
            neko = self.vsm_list.token_list()[0]
            # 一文書目の猫のtfidf
            dist_tfidf = round(self.vsm_list[0].vec[neko], error_decimals)
            vec_tfdif = round(self.vsm_list.vector_list()[0][0], error_decimals)
            self.assertEqual(dist_tfidf, vec_tfdif)

    unittest.main()

    # VSM: 単語リストのみを作成
    # VSM: pure_vectorを作成 <= vectorはcorpusありきでinitすべき
    # VSM: initがpure_vector_or_dict_vec
    
    pass
