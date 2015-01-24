#!/usr/bin/python
# -*- coding: utf-8 -*-

from abc import abstractmethod, ABCMeta #2.6以上限定

class Vsm(object):
    """
    ベクトル空間モデル
    TODO: featureにしたい

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
    3. 結果をまとめる
    """
    def __init__(self, text_collection):
        __metaclass__ = ABCMeta

        # 委譲
        self._tc = text_collection
        deligates = "list words_list".split()
        for name in deligates:
            method = getattr(self._tc, name)
            setattr(self, name, method)

    @abstractmethod
    def vecs(self):
        """
        サブモジュールのベクトル計算結果
        :return:
        """
        pass

    def run(self):
        return [Vsm(text, vec) for text, vec  in zip(self._tc.list(), self.vecs())]


