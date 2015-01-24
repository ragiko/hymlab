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
        self.words_cache = None # cache

    def text(self):
        if self.str is None:
            self.str = self.source.to_str()
        return self.str

    def words(self, content_poslist=[u"名詞"]):
        """
        キャッシュするとめちゃくちゃ早くなる
        """
        if self.words_cache is None: # cache
            contents = self.text()
            # 形態素解析し，結果をWordクラスの配列に格納
            words = mecabutil.get_words(contents)
            # 形態素解析結果から，名詞の単語の表層のみを抽出
            self.words_cache = [word.base_form for word in words if word.pos in content_poslist]
        return self.words_cache


    def __getstate__(self):
        """
        - pickle化するときにself.sourceを保持しない
        fileは保存できないので
        参考: http://docs.python.jp/3/library/pickle.html
        """
        # Copy the object's state from self.__dict__ which contains
        # all our instance attributes. Always use the dict.copy()
        # method to avoid modifying the original state.
        state = self.__dict__.copy()
        # Remove the unpicklable entries.
        del state['source']
        return state

    def __setstate__(self, state):
        # Restore instance attributes (i.e., filename and lineno).
        self.__dict__.update(state)
        # Restore the previously opened file's state. To do so, we need to
        # reopen it and read from it until the line count is restored.

class TextCollection:
    """
    input1: directroy path
    input2: ["sentence1", "sentence2"]
    TODO: input3 file path
    """
    def __init__(self, path_or_sentences):
        self.path_or_sentences = path_or_sentences
        self.source = TextCollectionSource(path_or_sentences)
        self.list_cache = None

    def list(self):
        """
        :return: Textオブジェクトのリスト
        """
        if self.list_cache is None: # cache
            if self.source.is_path():
                dir_path = self.path_or_sentences
                list = file_list(dir_path)
                self.list_cache = [Text(open(path)) for path in list]
            else:
                sentences = self.path_or_sentences
                self.list_cache = [Text(str) for str in sentences]

        return self.list_cache

    def words_list(self):
        """
        文書の単語のリスト
        :return:
        """
        return [text.words() for text in self.list()]

__all__ = ["Text", "TextCollection"]

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

