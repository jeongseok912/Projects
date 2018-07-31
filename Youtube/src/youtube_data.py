# created by jeongseok
# jeongseok912@gmail.com
# 2018.07.29

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
import pymongo
import time
import datetime

# 소셜러스 구독자 랭킹
# return type: list
# return valye: [channelID, category]
def getSocialerusRanking():
    chromedriver = '../chromedriver.exe'
    chromeBrowser = webdriver.Chrome(chromedriver)
    chromeBrowser.get("https://socialerus.com/ranking/total_ranking.asp?pb_orderBy=CR_SBUSCRIBER_COUNT")


    try:
        while True:
            # Explicit Waits
            # WebDriverWait는 성공적으로 반환될 때까지 0.5초마다 ExpectedCondition을 호출한다.
            # ExpectedCondition의 정상 리턴값 : true or not null
            # 3초 내에 반환 요소를 못찾으면 3초 기다린 후 TimeoutException을 던짐
            btn = WebDriverWait(chromeBrowser, 3).until(EC.presence_of_element_located((By.ID, 'btnMore')))
            if chromeBrowser.find_element_by_id('btnMore').get_attribute('style') != '':
                break
            else:
                btn.click()
    except TimeoutException:
        print(TimeoutException)
    finally:
        html = chromeBrowser.page_source # str
        srDoc = BeautifulSoup(html, 'html.parser') # bs4.BeautifulSoup
        dataAreas = srDoc.select('#dataArea > div > a') # list
        chromeBrowser.quit()

    rankingList = []
    for dataArea in dataAreas:
        # srElement = dataArea.select_one('.ranking_c_name')
        channelID = dataArea.attrs['href'].split('c_channelid=')[1]
        category = dataArea.select_one('.cg_name')
        # dataArea.get('href').split('c_channelid=')[1] 도 동일
        iArr = [channelID, category.text]
        rankingList.append(iArr)
    return rankingList

class Channel():
    def __init__(self):
        self.channelID = ''
        self.channelTitle = ''
        self.subscribers = 0
        self.tab = ''
        self.homeTab = ''
        self.homeTab_sections = ''
        self.videoTab = ''
        self.playlistTab = ''
        self.playlistTab_sections = ''
        self.channelTab = ''
        self.channelTab_recommendChannel = ''
        self.cummunityTab = ''
        self.informTab = ''
        self.informTab_desc = ''
        self.informTab_country = ''
        self.informTab_link = ''
        self.informTab_registerDate = ''
        self.informTab_viewCount = 0
        self.chromedriver = '../chromedriver.exe'
        self.chromeBrowser = webdriver.Chrome(self.chromedriver)

    def __del__(self):
        self.chromeBrowser.quit()

    def setChannelID(self, channelID):
        self.channelID = channelID

    def getChannelID(self):
        return self.channelID

    def setChannelTitle(self, channelURL):
        try:
            self.chromeBrowser.get(channelURL)
            chTitle = WebDriverWait(self.chromeBrowser, 3).until(EC.presence_of_element_located((By.ID, 'channel-title')))
            if chTitle is not None:
                self.channelTitle = chTitle.text
            else:
                self.channelTitle = ''
        except Exception:
            print(Exception)

    def getChannelTitle(self):
        return self.channelTitle
############################################################################################################################
# Main
############################################################################################################################
startTime = time.time()
# 몽고DB connection
conn = pymongo.MongoClient('localhost', 27017)
db = conn.get_database('youtube_channel')
collection = db.get_collection('channel')

# 소셜러스 구독자 랭킹에서 데이터 가져오기
print('\n### 소셜러스 구독자 랭킹에서 데이터 가져오기 ###')
rankingList = getSocialerusRanking()
point1 = time.time()
print('%s seconds' %  (point1 - startTime))
print('유튜버 수 : ' + str(len(rankingList)) + '명')

# MongoDB에 랭킹 데이터 저장
print('\n### 몽고DB에 랭킹데이터 저장하기 ###')
for i in range(len(rankingList)-1):
    collection.insert_one(
        {"CID": rankingList[i][0],
         "Category": rankingList[i][1]})
point2 = time.time()
print('%s seconds' %  (point1 - point2))
print('total %s seconds' %  (point1 - startTime))

# 채널 타이틀 가져오기
print('\n### 채널 타이틀 가져오기 ###')
selectAll = collection.find({}, no_cursor_timeout=True) # return type: cursor
start = time.time()
t = 0
cnt = 0
ch = Channel()
for selectOne in selectAll:
    ch.setChannelID(selectOne['CID'])
    channelURL = 'https://www.youtube.com/channel/' + ch.getChannelID()
    ch.setChannelTitle(channelURL)
    collection.update({'_id': selectOne['_id']}, {'$set': {'ChannelName': ch.getChannelTitle()}})
    print(ch.getChannelTitle())
    cnt += 1
print('cnt : ' + str(cnt))
del ch
selectAll.close()
endTime = time.time()
print('%s seconds' %  (endTime - point2))
print('total %s seconds' %  (endTime - startTime))




