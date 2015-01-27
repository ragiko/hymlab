#!/usr/bin/python
# -*- coding: utf-8 -*-

from math import log
from hymlab.text.text import *
from hymlab.text.feature.feature import *

class TfIdf(Feature):
    """
    - 抽象クラス
    参考: http://doloopwhile.hatenablog.com/entry/20090627/1275175981

    - TF-IDFモジュール
    nltkのパクリ
    """
    # TODO: init idf other dir
    def __init__(self, text_collection):
        super(TfIdf, self).__init__(text_collection)

        # ここで分離すべき
        self._idf_cache = {}

    def calc_tf(self, term, text):
        """
        The frequency of the term in text.

        NOTE: floatしてなかったからgitのコードは間違っていると思う
        """
        return float(text.count(term)) / float(len(text))

    def calc_idf(self, term):
        """ The number of texts in the corpus divided by the
        number of texts that the term appears in.
        If a term does not appear in the corpus, 0.0 is returned. """
        # idf values are cached for performance.
        idf = self._idf_cache.get(term)
        if idf is None:
            matches = len([True for text in self._tc.words_list() if term in text])
            # FIXME Should this raise some kind of error instead?
            idf = (log(float(len(self._tc.words_list())) / matches) if matches else 0.0)
            self._idf_cache[term] = idf
        return idf

    def calc_tf_idf(self, term, text):
        return self.calc_tf(term, text) * self.calc_idf(term)

    def tf(self):
        """
        - tfのアクセッサー

        input: [["w1", "w2"], ["w3", "w1"], ...]
        :return: [Vsm1, Vsm2, Vsm3, ...]
        """
        vecs = []
        for text in self._tc.list():
            vec = {} # document vector
            for word in text.words():
                vec[word] = self.calc_tf(word, text.words())
            vecs.append(Vsm(text, vec))
        return VsmList(vecs)

    def idf(self):
        """
        - idfのアクセッサー

        input: [["w1", "w2"], ["w3", "w1"], ...]
        :return: {"w1": 0.22231, "w2": 0.65433, ...}
        """
        if self._idf_cache != {}:
            return self._idf_cache

        for word in self._tc.vocab():
            # _idf_cacheにidfデータが保存される
            self.calc_idf(word)

        return self._idf_cache

    def tf_idf(self):
        """
        - tfidfのアクセッサー

        input: [["w1", "w2"], ["w3", "w1"], ...]
        :return: [Vsm1, Vsm2, Vsm3, ...]
        """
        vecs = []
        for text in self._tc.list():
            vec = {} # document vector
            for word in text.words():
                vec[word] = self.calc_tf_idf(word, text.words())
            vecs.append(Vsm(text, vec))
        return VsmList(vecs)

if __name__ == "__main__":
    from hymlab.text.vital import pp
    from hymlab.text.text import *
    from math import log
    import unittest

    class TfIdfTestCase(unittest.TestCase):
        def setUp(self):
            self.tc = TextCollection([
                u"我が輩は猫である。猫である。",
                u"我が輩は猫である",
                u"名前はまだ無い"])

        def tearDown(self):
            pass
       
        def test_idf_correct_calc(self):
            r = TfIdf(self.tc)
            self.assertEqual(r.calc_idf(u"猫"), log(3.0/2.0))
            self.assertEqual(r.calc_idf(u"輩"), log(3.0/2.0))
            self.assertEqual(r.calc_idf(u"名前"), log(3.0/1.0))

        def test_idf_not_value(self):
            r = TfIdf(self.tc)
            self.assertEqual(r.calc_idf(u"我"), 0.0)

        def test_tfidf_correct_calc(self):
            r = TfIdf(self.tc)
            # [u'輩', u'猫', u'猫']
            self.assertEqual(r.calc_tf_idf(u"猫",  self.tc.words_list()[0]), (2.0/3.0)*log(3.0/2.0))
            # [u'輩', u'猫']
            self.assertEqual(r.calc_tf_idf(u"猫",  self.tc.words_list()[1]), (1.0/2.0)*log(3.0/2.0))
            # [u'名前']
            self.assertEqual(r.calc_tf_idf(u"名前",  self.tc.words_list()[2]), (1.0/1.0)*log(3.0/1.0))

        def test_tfidf_correct_calc(self):
            r = TfIdf(self.tc)
            # [u'輩', u'猫', u'猫']
            self.assertEqual(r.calc_tf_idf(u"猫",  self.tc.words_list()[0]), (2.0/3.0)*log(3.0/2.0))
            # [u'輩', u'猫']
            self.assertEqual(r.calc_tf_idf(u"猫",  self.tc.words_list()[1]), (1.0/2.0)*log(3.0/2.0))
            # [u'名前']
            self.assertEqual(r.calc_tf_idf(u"名前",  self.tc.words_list()[2]), (1.0/1.0)*log(3.0/1.0))

        def test_tf(self):
            """
            tf関数が正しく動作しているかどうか
            """
            r = TfIdf(self.tc)
            # [u'輩', u'猫', u'猫']
            self.assertEqual(r.tf()[0].vec[u"猫"], 2.0/3.0)
            # [u'輩', u'猫']
            self.assertEqual(r.tf()[1].vec[u"猫"], 1.0/2.0)

        def test_tf_for_text(self):
            """
            tf関数が正しく動作しているかどうか
            text objに対するテスト
            """
            r = TfIdf(self.tc)
            pp(r.tf()[0].text)
            # [u'輩', u'猫', u'猫']
            # self.assertEqual(r.tf()[0].text, 2.0/3.0)

        def test_idf(self):
            """
            idf関数が正しく動作しているかどうか
            """
            r = TfIdf(self.tc)
            self.assertEqual(r.idf()[u"猫"], log(3.0/2.0))

        def test_tf_idf(self):
            """
            tf_idf関数が正しく動作しているかどうか
            """
            r = TfIdf(self.tc)
            # [u'輩', u'猫', u'猫']
            self.assertEqual(r.tf_idf()[0].vec[u"猫"], (2.0/3.0)*log(3.0/2.0))

    unittest.main()
