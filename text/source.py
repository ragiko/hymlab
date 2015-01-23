#!/usr/bin/python
# -*- coding: utf-8 -*-

from hymlab.text.util import *

class TextSource:
    """
    Textクラスの入力ソース
    """
    def __init__(self, file_or_str):
        self.file_or_str = file_or_str

    def is_file(self):
        return isinstance(self.file_or_str, file)

    def is_str(self):
        return isinstance(self.file_or_str, str)

    def to_str(self):
        if self.is_file():
            return file_read_from_file(self.file_or_str)
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


