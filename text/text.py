#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from hymlab.text.util import *
from hymlab.text import mecabutil
from hymlab.text.source import *

class Text:
    def __init__(self, file_or_str):
        self.source = TextSource(file_or_str)
        self.path = None # ファイルのパス
        if self.source.is_file():
            self.path = file_or_str.name
        self.str = None # cache

    def text(self):
        if self.str is None:
            self.str = self.source.to_str()
        return self.str

    def words(self, content_poslist=[u"名詞"]):
        contents = self.text()
        # 形態素解析し，結果をWordクラスの配列に格納
        words = mecabutil.get_words(contents)
        # 形態素解析結果から，名詞の単語の表層のみを抽出
        words = [word.base_form for word in words if word.pos in content_poslist]
        return words

class TextCollection:
    """
    input1: directroy path
    input2: ["sentence1", "sentence2"]
    """
    def __init__(self, path_or_sentences):
        self.path_or_sentences = path_or_sentences
        self.source = TextCollectionSource(path_or_sentences)

    def list(self):
        """
        :return: Textオブジェクトのリスト
        """
        if self.source.is_path():
            dir_path = self.path_or_sentences
            list = file_list(dir_path)
            return [Text(open(path)) for path in list]
        else:
            sentences = self.path_or_sentences
            return [Text(str) for str in sentences]

    def words_list(self):
        """
        文書の単語のリスト
        :return:
        """
        return [text.words() for text in self.list()]

if __name__ == "__main__":
    from hymlab.text.vital import pp

    doc = Text(open("test/data/a.txt"))
    # pp(doc.text().encode('utf_8'))
    # pp(doc.words([u"名詞"]))

    #///////////////////////////////
    # init string
    #///////////////////////////////
    # docs = TextCollection("test/data")
    docs = TextCollection([u"我が輩は猫である", u"名前はまだ無い"])
    # pp(docs.list()[0])
    # pp(docs.words_list())
    # pp([(doc.path, doc.text()) for doc in docs.list()])
    pp(docs.words_list())

    #///////////////////////////////
    # init file
    #///////////////////////////////
    docs = TextCollection("test/data")
    # pp([(doc.path, doc.text(), doc.words()) for doc in docs.list()])
    pp(docs.words_list())

