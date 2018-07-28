# 전체 유튜버 그룹
# created by jeongseok
# jeongseok912@gmail.com
# 2018.07.25
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
import groupA

res = requests.get("https://namu.wiki/w/%EC%9C%A0%ED%8A%9C%EB%B8%8C/%EC%9C%A0%EB%AA%85%20%EC%B1%84%EB%84%90%20%EB%B0%8F%20%EB%8F%99%EC%98%81%EC%83%81")
soup = BeautifulSoup(res.content, 'html.parser')

# 나무위키 유튜버 리스트 크롤링
namu_channelLists = soup.select('div.wiki-content.clearfix > div > div > ul > li > p')

## 국내 유튜버 리스트 추출 전처리
for i in range(5):
    namu_channelLists.remove(namu_channelLists[0])
tmp_list = []
for namu_channelList in namu_channelLists:
    tmp_list.append(namu_channelList.get_text().split(' - ')[0])

# "Against The Current" 전까지 가져오기
tmp_channelLists = tmp_list[0:515] # 국내 유튜버 리스트
print(tmp_channelLists)

for i in range(len(groupA.sbRank)):
    for j in range(len(tmp_channelLists)):
        if groupA.sbRank[i] == tmp_channelLists[j]:
            print(groupA.sbRank[i])

# 몽고DB
'''
mongoClient = MongoClient('localhost', 27017)
## db와 collection 제어는 즉시 이루어지지 않고 데이터 입/출력 작업 실행 시 접근된다.
db = mongoClient.youtube_channel
collection = db.groupB

channelLists = list()
for i in range(len(tmp_channelLists)):
    channelLists.append({'channelName':tmp_channelLists[i]})

collection.insert_many(channelLists)
'''