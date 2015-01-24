#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
from abc import abstractmethod, ABCMeta #2.6以上限定

class Feature(object): # object継承しないとsuper呼べない
    """
    TODO: 委譲あたりのコードを修正したい
    1. textの取得
    2. 特徴量抽出 (subclass)
    3. 結果をまとめる
    """
    pass

    def __init__(self, text_collection):
        __metaclass__ = ABCMeta

        # 委譲
        self._tc = text_collection
        deligates = "list words_list".split()
        for name in deligates:
            method = getattr(self._tc, name)
            setattr(self, name, method)

        # rubyのstruct
        # http://d.hatena.ne.jp/saitodevel01/20100605/1275728303
        self.Feature = namedtuple("Vsm", "text vec")

    @abstractmethod
    def vecs(self):
        """
        サブモジュールのベクトル計算結果
        :return:
        """
        pass

    def run(self):
        return [self.Feature(text, vec) for text, vec  in zip(self._tc.list(), self.vecs())]


