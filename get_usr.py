# -*- coding: utf-8 -*-
'''
对知乎用户进行滚雪球抽样，直到得到12W有效用户
'''
import os, time, requests, json, math, random, logging, datetime
from collections import deque

#  默认参数
BASE_URL = 'https://www.zhihu.com/api/v4'
FILE_PATH = '/home/madoka/Workspace/zhihu/data'
KEYS_LIST = ['id', 'name', 'url_token', 'type', 'gender',
             'answer_count', 'follower_count', 'following_count',
             'thanked_count', 'voteup_count']
BASE_QUERY = ['gender', 'voteup_count', 'thanked_count',
              'follower_count', 'following_count', 'answer_count']
MAX_QUERY = 100010  ### 限制最大获取长度
MAX_MAP = MAX_QUERY + 1000  ### 最大获取长度+1000
logging.basicConfig(filename='./log/log%s.log' % datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), level = logging.WARNING)

# 请求头
def create_headers():
    AUTHORIZATION = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    REFERER = 'https://www.zhihu.com/signup?next=%2F'
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    headers = {
            "User-Agent": USER_AGENT,
            "Referer": REFERER,
            "authorization": AUTHORIZATION}
    return headers
BASE_HEADERS = create_headers()

# 生成用户信息查询url
def create_member_url(token):
    url = '%s/%s/%s%s' % (BASE_URL, 'members', token, '?include=')
    for i in BASE_QUERY:
        url = url + i + ','
    url = url.rstrip(',')
    return url

# 获取用户信息
def get_member_profile(token):
    url = create_member_url(token)
    res = requests.get(url, headers = BASE_HEADERS)
    data_raw = res.json()
    data = {key: value for key, 
            value in data_raw.items() if key in KEYS_LIST}
    data['time'] = time.asctime()
    time.sleep(random.uniform(0.2, 0.4))
    return data

# 生成粉丝查询url
def create_follower_url(token):
    url = '%s/%s/%s/%s' % (BASE_URL, 'members', token, 'followers?include=data[*].')
    for i in BASE_QUERY:
        url = url + i + ','
    url = url.rstrip(',')
    return url

# 获取粉丝信息，仅获取首页，即<=20
def get_follower(token):
    url_head = create_follower_url(token)
    url = '%s%s' % (url_head, '&offset=0&limit=20')
    res = requests.get(url, headers = BASE_HEADERS)
    data_raw = res.json()
    data = {}
    try:
        for i in data_raw['data']:
            data_temp = {key: value for key, 
                value in i.items() if key in KEYS_LIST}
            data_temp['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data[data_temp['url_token']] = data_temp
    except:
        print('get_follower error')
    time.sleep(random.uniform(0.2, 0.4))
    return data

# 生成关注者查询url
def create_followee_url(token):
    url = '%s/%s/%s/%s' % (BASE_URL, 'members', token, 'followees?include=data[*].')
    for i in BASE_QUERY:
        url = url + i + ','
    url = url.rstrip(',')
    return url

# 获取关注者信息，仅获取首页，即<=20
def get_followee(token):
    url_head = create_followee_url(token)
    url = '%s%s' % (url_head, '&offset=0&limit=20')
    res = requests.get(url, headers = BASE_HEADERS)
    data_raw = res.json()
    data = {}
    try:
        for i in data_raw['data']:
            data_temp = {key: value for key, 
                value in i.items() if key in KEYS_LIST}
            data_temp['time'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data[data_temp['url_token']] = data_temp
    except:
        print('get_followee error')
    time.sleep(random.uniform(0.2, 0.4))
    return data

# 存储json文件
def save_json(data, token):
    file_name = '%s/%s.json' % (FILE_PATH, token)
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=4)

#########################################################################
if __name__ == '__main__':
    seed_user = ['excited-vczh', 'zhang-jia-wei', 'jian-bing-pu-ti', 'liao-bu-qi-de-su-xiao-jie', 'magasa', 'yie-jia-tong']
    queue = deque(seed_user)
    hash_map = []
    while True:
        try:
            token = queue.popleft()
            if token in hash_map:
                continue
        except IndexError:
            print('IndexError')
            break
        try:
            data = get_member_profile(token)
            save_json(data, token)
            hash_map.append(token)
            data_num = len(hash_map)
            queue_num = len(queue)
            print(token, data_num, queue_num)
            if data_num >= MAX_QUERY:
                save_json(hash_map, 'hash_map_name_list')
                print('Finished!')
                break    
            if (queue_num + data_num) < MAX_MAP:
                followees = get_followee(token)
                count = 0
                for i in followees:
                    if i in hash_map:
                        continue
                    count += 1
                    if count > 6:
                        break
                    queue.append(i)
        except:
            print('Some Error! Continue...')

