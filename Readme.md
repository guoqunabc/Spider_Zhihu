### 知乎用户爬虫项目

- potential_usr.py
  - 通过滚雪球增量抽样预选取潜在用户样本，并查看粉丝数分布情况
  - 无实际作用
- get_usr.py
  - 通过滚雪球随机增量抽样，得到10W用户的基本资料与url
  - 
- user_split.py
  - 将10W用户根据粉丝数，划为分布相似的3部分
  - 输出：./name_list_1.json, name_list_2.json, name_list_3.json
- scan_follower.py
  - 定时扫描列表中用户的粉丝数
  - 输出：./data_panel/*.json