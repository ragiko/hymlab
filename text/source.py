#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from hymlab.text.util import *

class TextSource:
    """
    Textクラスの入力ソース
    """
    def __init__(self, file_or_str):
        self.file_or_str = file_or_str
        self.file_path = ""
        if (isinstance(self.file_or_str, file)):
            self.file_path = os.path.abspath(self.file_or_str.name)
            # 開きっぱなしのファイルのclose
            if (self.file_or_str.closed == False):
                self.file_or_str.close()

    def is_file(self):
        return self.file_path != ""

    def is_str(self):
        return self.file_path == ""

    def to_str(self):
        if self.is_file():
            return file_read(self.file_path)
        else:
            return self.file_or_str

class TextCollectionSource:
    """
    TextCollectionクラスの入力ソース
    """
    def __init__(self, path_or_sentences):
        self.path_or_sentences = path_or_sentences

    def is_path(self):
        return isinstance(self.path_or_sentences, str)

    def is_sentences(self):
        return isinstance(self.path_or_sentences, list)

if __name__ == "__main__":
    # from file
    print Source(open("test/data/a.txt")).to_str()
    # from str
    print Source("我が輩は猫である").to_str()


