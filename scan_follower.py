# -*- coding: utf-8 -*-
# 定时扫描列表中用户的粉丝数
import time, requests, json, datetime, logging
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

BASE_PATH = '.'
FILE_PATH = '%s/%s' % (BASE_PATH, 'data_panel')
NAMELIST_FILE = '%s/%s' % (BASE_PATH, 'name_list_1.json') #### 名单

BASE_URL = 'https://www.zhihu.com/api/v4'
KEYS_LIST = ['url_token', 'answer_count', 'follower_count',
             'following_count','thanked_count', 'voteup_count']
BASE_QUERY = ['gender', 'voteup_count', 'thanked_count',
              'follower_count', 'following_count', 'answer_count']

TIME_NOW = datetime.datetime.now().strftime("%Y-%m-%d %H-%M")
LOG_NAME = './log/log%s.log' % (TIME_NOW)
logging.basicConfig(filename = LOG_NAME, filemode="w+", level = logging.WARNING)
TIMEOUT = 3

### 代理 蘑菇代理
appKey = "eFE4TGhLZ08yNjVJVllUbTpGbDkzNEx3WWp3cXhtejdE"
ip_port = 'transfer.mogumiao.com:9001'
proxy = {"http": "http://" + ip_port, "https": "https://" + ip_port}


def create_headers():
    AUTHORIZATION = 'oauth c3cef7c66a1843f8b3a9e6a1e3160e20'
    REFERER = 'https://www.zhihu.com/signup?next=%2F'
    USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
    headers = {
            "User-Agent": USER_AGENT,
            "Referer": REFERER,
            "authorization": AUTHORIZATION,
            "Proxy-Authorization": 'Basic '+ appKey}
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
    try_count = 0
    while True:
        try:
            res = requests.get(url, headers = BASE_HEADERS, proxies=proxy, verify=False, allow_redirects=False, timeout=TIMEOUT) #### 核心请求
            try_count += 1
            if res.ok:
                data_raw = res.json()
                data = {key: value for key, 
                        value in data_raw.items() if key in KEYS_LIST}
                print(token, 'requests answer:', res)
                return data
            if try_count > 5:
                return {}
            print(token, 'requests answer:', res, 'retring...', try_count)
        except OSError:
            print(token, 'ProxyError!')
            time.sleep(0.5)


# 初始化文件夹并新建空json
def init_zhihu(user_list):
    for i in user_list:
        file_name = '%s/%s%s' % (FILE_PATH, user_list[i], '.json')
        try:
            with open(file_name, 'r', encoding='utf-8') as f:
                pass
        except:
            data = {}
            with open(file_name, 'w+', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=4)

# 循环扫描
def scan_zhihu(user_list):
    for i in user_list:
        try:
            file_name = '%s/%s%s' % (FILE_PATH, user_list[i], '.json')
            with open(file_name, 'r', encoding='utf-8') as f:
                data = json.load(f)
            data_new = get_member_profile(user_list[i])
            time_now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            data[time_now] = data_new
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, sort_keys=True, indent=4)
            print(time_now, user_list[i], len(data))
        except Exception as err:
            logging.warning('%s %s %s!', time_now, user_list[i], err)
            print('%s %s %s!', time_now, user_list[i], err)
        time.sleep(0.5)
        

# 主程序
if __name__ == '__main__':
    file_name = NAMELIST_FILE
    with open(file_name, 'r', encoding='utf-8') as f:
        user_list = json.load(f)
    init_zhihu(user_list)
    while True:
        scan_zhihu(user_list)