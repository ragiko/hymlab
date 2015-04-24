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

def dir_read_join(directory_path, join_str="."):
    """
    ディレクトリー内のファイル内容を結合して返却
    :param file_path:
    :return: string
    """
    contents_list = [file_read(file_path) for file_path in file_list(directory_path)]
    return join_str.join(contents_list)

def file_list(directory_path):
    import os
    file_list = os.listdir(directory_path)
    absolute_filepath = [directory_path+"/"+file_name for file_name in file_list]
    return absolute_filepath

def dir_list(directory_path):
    """
    フォルダ内のディレクトリの名前のみ表示
    :param directory_path: 
    :return:
    """
    import os
    paths = os.listdir(directory_path)
    
    dir_paths = []
    for name in paths:
        abs_path = directory_path+"/"+name
        if os.path.isdir(abs_path) == True:
            dir_paths.append(abs_path)
    dir_paths.sort() # sort
    return dir_paths

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


