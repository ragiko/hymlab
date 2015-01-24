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
        :return: (入力がNoneのときは強制的にFalseを返す)
        """
        if text is None:
            return False

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
        :return: 1から-1 (片方が零ベクトルのときはNoneを返す)
        """
        # 基底となる単語の和集合を計算
        keys = set( dict1.keys() ) | set( dict2.keys() )

        # 次元を揃えて，dictからコサイン類似度計算用のベクトルを生成
        vector1 = [ dict1.get(key, 0) for key in keys]
        vector2 = [ dict2.get(key, 0) for key in keys]

        # 零ベクトルの計算にはNoneを返却
        if (self.is_zero_vector(vector1) or self.is_zero_vector(vector2)):
            return None

        # cosine でコサイン距離を計算，1-cosineでコサイン類似度となる．
        sim = 1 - scipy.spatial.distance.cosine(vector1, vector2)

        return sim

    def is_zero_vector(self, vector):
        """
        :param vector: list
        :return:
        """
        zero_vec = [0.0] * len(vector)
        return zero_vec == vector

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

    def most_similarity_future_by_outer_feature(self, outer_vsm):
        """
        - 類似度を計算してランキング
        外部の文書に対して類似度を算出
        :param
        :return:
        """
        similarities = []
        for vsm in self.features:
            sim = self.dict_cosine(vsm.vec, outer_vsm.vec)
            sim_obj = self.Similarity(outer_vsm, vsm, sim)
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
            # directory base init
            tc = TextCollection("test/data")
            tfidf = TfIdf(tc).run()
            self.sim = Similarity(tfidf)

            # sentence base init
            tc_s = TextCollection([u"我が輩は猫である", u"我が輩は猫である", u"名前はまだない"])
            tfidf_s = TfIdf(tc_s).run()
            self.sim_s = Similarity(tfidf_s)

        def tearDown(self):
            pass

        def test_is_zero_vector_input_zero_vector(self):
            vector = [0,0.0,0]
            self.assertEqual(self.sim.is_zero_vector(vector), True)
            vector = [0,0,0]
            self.assertEqual(self.sim.is_zero_vector(vector), True)

        def test_is_zero_vector_input_not_zero_vector(self):
            vector = [1,0.0,0]
            self.assertEqual(self.sim.is_zero_vector(vector), False)

        def test_is_match(self):
            text = "path/to/file"
            self.assertEqual(self.sim.is_match("file", text), True)
            self.assertEqual(self.sim.is_match("aaa", text), False)

        def test_is_match_input_none(self):
            """
            テキストがNoneだったときにfalseを返す
            :return:
            """
            text = "path/to/file"
            self.assertEqual(self.sim.is_match("file", None), False)

        def test_dist_cosine_input_zero_vector(self):
            t = self.sim.dict_cosine({"a":0, "b":0}, {"a":1, "b":2})
            self.assertEqual(t, None)

        def test_find_future_by_file_is_exist(self):
            text = self.sim.find_feature_by_filename("a.txt")
            self.assertNotEqual(text, None)

        def test_find_future_by_file_not_exist(self):
            text = self.sim.find_feature_by_filename("abc.txt")
            self.assertEqual(text, None)

        def test_find_future_by_file_for_sentence_base_init(self):
            """
            文字列ベースで初期化した時、ファイルを検索できない
            :return:
            """
            text = self.sim_s.find_feature_by_filename("a.txt")
            self.assertEqual(text, None)

        def test_most_similarity_future_by_inner_filename(self):
            pass
            # res = self.sim.most_similarity_future_by_inner_filename("a.txt")
            # for sim in res:
            #     pp(sim.vsm1.text.words())
            #     pp(sim.vsm2.text.words())
            #     pp(sim.similarity)

        def test_most_similarity_future_by_outer_filename_only_sentence(self):
            pass
            # tc = TextCollection([u"我が輩は猫である"])
            # tfidf = TfIdf(tc).run()
            # res = self.sim.most_similarity_future_by_outer_feature(tfidf[0])
            # for sim in res:
            #     pp(sim.vsm1.text.words())
            #     pp(sim.vsm2.text.words())
            #     pp(sim.similarity)

        def test_test(self):
            # 文書集合を定義
            tc = TextCollection("test/data")

            # 特徴量を取得
            tfidf = TfIdf(tc).run()

            # a.txtに対する類似度を表示
            self.sim = Similarity(tfidf)
            res = self.sim.most_similarity_future_by_inner_filename("a.txt")

            for sim in res:
                print u"file A : %s" %  sim.vsm1.text.path
                print u"file B : %s" %  sim.vsm2.text.path
                print u"similarity : %s" %  sim.similarity
                print "\n"

    unittest.main()


