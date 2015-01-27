#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from hymlab.text.vital import *
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

            # []の入力ならばすべての単語を返す
            if (content_poslist == []):
                self.words_cache = [word.base_form for word in words]
            else: 
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

    def dump_texts(self):
        """
        テキストを出力する
        """
        texts = [text_obj.text() for text_obj in self.list()]
        for text in texts:
            pp(text)
            print "\n"

    def add_text_collection(self, other_text_collection):
        """
        テキストコレクションを追加
        NOTE: 自身のオブジェクトが変化
        """
        this_texts = self.list()
        other_texts =  [text for text in other_text_collection.list()]
        this_texts.extend(other_texts)
        self.list_cache = this_texts
        return self.list_cache 

    def dump_corpus(self, filepath, sent_end=""):
        """
        - コーパスを作成
        我が輩は猫である
        
        to

        我が 輩 は 猫 で ある

        NOTE: 文章の最後は.にする
        """
        f = open(filepath, "w")
        e = sent_end + "\n"
        s = e.join([" ".join(text.words([])) for text in self.list()]) + sent_end
        pp(filepath)
        f.write(s.encode("utf-8"))
        f.close()

__all__ = ["Text", "TextCollection"]

if __name__ == "__main__":
    from hymlab.text.vital import pp
    import unittest

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
    # pp(docs.words_list())

    #///////////////////////////////
    # init file
    #///////////////////////////////
    docs = TextCollection("test/data")
    # pp([(doc.path, doc.text(), doc.words()) for doc in docs.list()])
    # pp(docs.words_list())

    class TextCollectionTestCase(unittest.TestCase):
        def setUp(self):
            self.docs_from_dir = TextCollection("test/data")
        
        def tearDown(self):
            pass

        def test_dump(self):
            # self.docs_from_dir.dump_texts()
            pass

        def test_text_collection_add_texts(self):
            tc1 = TextCollection([u"我が輩は猫である", u"名前はまだ無い"]) 
            tc2 = TextCollection([u"我が輩は猫である", u"名前はまだ無い"]) 
            tc1.add_text_collection(tc2)
            self.assertEqual(len(tc1.list()), 4)

        def test_text_collection_dump_corpus(self):
            tc = TextCollection([u"我が輩は猫である", u"名前はまだ無い"]) 
            tc.dump_corpus(os.path.dirname(os.path.abspath(__file__))+"/test/tmp/dump_corpus.txt")
            pass

        def test_text_get_noun_words(self):
            t = Text(u"我が輩は猫である")
            self.assertEqual(len(t.words()), 2)

        def test_text_get_all_words(self):
            """
            []を渡すと単語をすべて返す
            """
            t = Text(u"我が輩は猫である")
            self.assertEqual(len(t.words([])), 6)

    unittest.main()
