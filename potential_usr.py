# -*- coding: utf-8 -*-
# 通过滚雪球增量抽样选取潜在用户样本，并查看粉丝数分布情况
import json, os
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

FILE_PATH = 'E:/WorkspacePy/aliyun/user_data'

def read_my_file(token):
    file_name = '%s/%s' % (FILE_PATH, token)
    with open(file_name, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

def token_name(file_dir):   
    for root, dirs, files in os.walk(file_dir):  
        return files

def show_dist(data):
    plt.hist(data)
    plt.show()

if __name__ == '__main__':
    token_list = token_name(FILE_PATH)
    data_all = {}
    broken_name = []
    for i in token_list:
        try:
            data = read_my_file(i)
            data_all[data['url_token']] = data
        except:
            broken_name.append(i)
    
    follower_all = []
    gender_all = []
    voteup_all = []
    following_all = []
    answer_all = []
    for i in data_all.keys():
        follower_all.append(data_all[i]['follower_count'])
        gender_all.append(data_all[i]['gender'])
        voteup_all.append(data_all[i]['voteup_count'])
        following_all.append(data_all[i]['following_count'])
        answer_all.append(data_all[i]['answer_count'])
    
    data_pd = pd.DataFrame({'follower_count':follower_all,
                                'following_count':following_all,
                                'answer_count':answer_all,
                                'voteup_count':voteup_all,
                                'gender':gender_all,
                                })
    
    summary = data_pd.describe([])
    summary = summary.transpose()
    print(summary)
    show_dist(data_pd)
    follower_np = np.array(follower_all)
    print('Total samples:', len(follower_np))
    temp = len(follower_np[follower_np == 0])
    print('Follower [0, 0]:', temp)
    temp = len(follower_np[follower_np<=100]) - len(follower_np[follower_np == 0])
    print('Follower (0,100]:', temp)
    temp = len(follower_np[follower_np<=1000]) - len(follower_np[follower_np <= 100])
    print('Follower (100,1000]:', temp)
    temp = len(follower_np[follower_np<=2000]) - len(follower_np[follower_np <= 1000])
    print('Follower (1000,2000]:', temp)
    temp = len(follower_np[follower_np<=5000]) - len(follower_np[follower_np <= 2000])
    print('Follower (2000,5000]:', temp)
    temp = len(follower_np[follower_np<=10000]) - len(follower_np[follower_np <= 5000])
    print('Follower (5000,10000]:', temp)
    temp = len(follower_np[follower_np<=20000]) - len(follower_np[follower_np <= 10000])
    print('Follower (10000, 20000]:', temp)
    temp = len(follower_np[follower_np<=30000]) - len(follower_np[follower_np <= 20000])
    print('Follower (20000, 30000]:', temp)
    temp = len(follower_np[follower_np<=40000]) - len(follower_np[follower_np <= 30000])
    print('Follower (30000, 40000]:', temp)
    temp = len(follower_np[follower_np<=50000]) - len(follower_np[follower_np <= 40000])
    print('Follower (40000, 50000]:', temp)
    temp = len(follower_np[follower_np<=100000]) - len(follower_np[follower_np <= 50000])
    print('Follower (50000, 100000]:', temp)
    temp = len(follower_np[follower_np>100000])
    print('Follower (100000+]:', temp)
    