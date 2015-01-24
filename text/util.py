#!/usr/bin/python
# -*- coding: utf-8 -*-

import nkf
import pickle

# ファイルを読み込み，文字コード変換
def file_read(file_path):
    # ファイルオープン
    contents = open(file_path).read()
    contents = nkf.nkf("-w -d", contents) \
        .decode("utf_8")
    return contents

# ファイルを読み込み，文字コード変換
# ファイルオブジェクトから取得
def file_read_from_file(file):
    # ファイルオープン
    contents = file.read()
    contents = nkf.nkf("-w -d", contents) \
        .decode("utf_8")
    return contents

def file_list(directory_path):
    import os
    file_list = os.listdir(directory_path)
    absolute_filepath = [directory_path+"/"+file_name for file_name in file_list]
    return absolute_filepath

def pickle_save(obj, file_path):
    f = open(file_path, "wb")
    pickle.dump(obj, f)
    f.close()

def pickle_load(file_path):
   f = open(file_path, "r")
   obj = pickle.load(f)
   f.close()
   return obj

if __name__ == '__main__':
    a = [1, 2, 3]
    pickle_save(a, "test/data/a")
    print pickle_load("test/data/a")


