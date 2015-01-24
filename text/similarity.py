#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import scipy.spatial.distance
from collections import namedtuple
from operator import attrgetter
from hymlab.text.text import *
from hymlab.text.feature.feature import *
from hymlab.text.feature.tfidf import *

class Similarity:
    """
    ベースはコサイン尺度
    """
    def __init__(self, features):
        self.features = features
        self.Similarity = namedtuple("Similarity", "vsm1 vsm2 similarity")

    def is_match(self, regexp, text):
        """
        テキストに対して正規表現が一致しているかどうか
        :param text:
        :param regexp:
        :return:
        """
        if re.search(regexp, text):
            return True
        else:
            return False

    def find_feature_by_filename(self, filename):
        """
        見つかったファイル名の先頭の特徴量を返す
        :param filename:
        :return:
        """
        vsm_list = [vsm for vsm in self.features if self.is_match(filename, vsm.text.path)]
        if len(vsm_list) == 0:
            return None
        return vsm_list[0]

    def dict_cosine(self, dict1, dict2):
        """
        @ 原先輩
        :param dict1:
        :param dict2:
        :return:
        """
        # 基底となる単語の和集合を計算
        keys = set( dict1.keys() ) | set( dict2.keys() )

        # 次元を揃えて，dictからコサイン類似度計算用のベクトルを生成
        vector1 = [ dict1.get(key, 0) for key in keys]
        vector2 = [ dict2.get(key, 0) for key in keys]

        # cosine でコサイン距離を計算，1-cosineでコサイン類似度となる．
        sim = 1 - scipy.spatial.distance.cosine(vector1, vector2)

        return sim

    def most_similarity_future_by_inner_filename(self, filename):
        """
        - 類似度を計算してランキング
        特徴量の内部のあるものに対して類似度を算出

        - sortの参考
        http://stackoverflow.com/questions/12087905/pythonic-way-to-sorting-list-of-namedtuples-by-field-name

        :param filename:
        :return:
        """
        similarities = []
        found_vsm = self.find_feature_by_filename(filename)
        for vsm in self.features:
            if vsm == found_vsm: # 自分の要素をはじく
                continue
            sim = self.dict_cosine(vsm.vec, found_vsm.vec)
            sim_obj = self.Similarity(found_vsm, vsm, sim)
            similarities.append(sim_obj)

        return sorted(similarities, key=attrgetter('similarity'), reverse=True)

    # あるファイルの特徴量を探す
    # cos尺度より似ている物を探す
    # ランキングして返却

if __name__ == '__main__':
    from hymlab.text.vital import pp
    import unittest

    class SimilarityTestCase(unittest.TestCase):
        def setUp(self):
            tc = TextCollection("test/data")
            tfidf = TfIdf(tc).run()
            self.sim = Similarity(tfidf)

        def tearDown(self):
            pass

        def test_is_match(self):
            text = "path/to/file"
            self.assertEqual(self.sim.is_match("file", text), True)
            self.assertEqual(self.sim.is_match("aaa", text), False)

        def test_find_future_by_file_is_exist(self):
            text = self.sim.find_feature_by_filename("a.txt")
            self.assertNotEqual(text, None)

        def test_find_future_by_file_not_exist(self):
            text = self.sim.find_feature_by_filename("abc.txt")
            self.assertEqual(text, None)

        def test_most_similarity_future_by_inner_filename(self):
            pass
            # res = self.sim.most_similarity_future_by_inner_filename("a.txt")
            # for sim in res:
            #     pp(sim.vsm1.text.words())
            #     pp(sim.vsm2.text.words())
            #     pp(sim.similarity)



    unittest.main()


