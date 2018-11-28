# -*- coding: utf-8 -*-
# 将10W用户根据粉丝数，划为分布相似的3部分
import os, time, requests, json, math, random, datetime
from collections import deque
import numpy as np

BASE_PATH = 'E:/WorkspacePy/aliyun'
FILE_PATH = 'E:/WorkspacePy/aliyun/user_data'

def token_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        return files

def read_my_file(token):
    file_name = '%s/%s' % (FILE_PATH, token)
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def write_my_file(file_name, data):
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=4)

# 主程序
if __name__ == '__main__':
    token_list = token_name(FILE_PATH)    
    data_follower = {}
    broken_name = []
    for i in token_list:
        try:
            data = read_my_file(i)
            data_follower[data['url_token']] = data['follower_count']
        except:
            broken_name.append(i)
    name_pairs = sorted(data_follower.items(), key = lambda item:item[1])
    name_num = len(name_pairs)
    
    name_list_1 = {}
    name_list_2 = {}
    name_list_3 = {}
    count = 0
    while True:
        if count < name_num:
            name_list_1[count] = name_pairs[count][0]
            count += 1
        else:
            break
        if count < name_num:
            name_list_2[count] = name_pairs[count][0]
            count += 1
        else:
            break
        if count < name_num:
            name_list_3[count] = name_pairs[count][0]
            count += 1
        else:
            break
    print(name_num, len(name_list_1), len(name_list_2), len(name_list_3))
    file_name_1 = 'E:/WorkspacePy/aliyun/name_list_1.json'
    file_name_2 = 'E:/WorkspacePy/aliyun/name_list_2.json'
    file_name_3 = 'E:/WorkspacePy/aliyun/name_list_3.json'
    write_my_file(file_name_1, name_list_1)
    write_my_file(file_name_2, name_list_2)
    write_my_file(file_name_3, name_list_3)
    
    