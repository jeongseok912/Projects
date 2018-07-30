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

# 소셜러스 구독자 랭킹
# return
# [[이름, 카테고리, 채널ID],
# [이름, 카테고리, 채널ID],
# ...
# [이름, 카테고리, 채널ID]]
def getSocialerusRanking():
    chromedriver = '../chromedriver.exe'
    chromeBrowser = webdriver.Chrome(chromedriver)
    chromeBrowser.get("https://socialerus.com/ranking/total_ranking.asp?pb_orderBy=CR_SBUSCRIBER_COUNT")
    try:
        # Explicit Waits
        # WebDriverWait는 성공적으로 반환될 때까지 0.5초마다 ExpectedCondition을 호출한다.
        # ExpectedCondition의 정상 리턴값 : true or not null

        # TODO - 네트워크 예외 처리
        # 3초 내에 반환 요소를 못찾으면 3초 기다린 후 TimeoutException을 던짐
        wait = WebDriverWait(chromeBrowser, 3)
        wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.ranking_c_name')))

        while True:
            chromeBrowser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#btnMore'))).click()
    except ElementNotVisibleException:
        print("element not visible!")
    except TimeoutException:
        print("Check network status!!")
    finally:
        html = chromeBrowser.page_source # str
        srDoc = BeautifulSoup(html, 'html.parser') # bs4.BeautifulSoup
        dataAreas = srDoc.select('#dataArea > div > a') # list
        chromeBrowser.quit()

    rankingList = []
    for dataArea in dataAreas:
        srElement = dataArea.select_one('.ranking_c_name')
        category = dataArea.select_one('.cg_name')
        channelID = dataArea.attrs['href'].split('c_channelid=')[1]
        # dataArea.get('href').split('c_channelid=')[1] 도 동일
        iArr = [srElement.text, category.text, channelID]
        rankingList.append(iArr)
    return rankingList

class Channel():
    channelID = ''
    channelTitle = ''
    subscribers = 0
    # 홈
    # 동영상
    # 재생목록
    # 커뮤니티
    # 채널
    # 정보
    tab = ''
    # 콘텐츠 선택
    ## 동영상
    ### 인기 업로드
    ### 업로드한 동영상
    ### 좋아요 표시한 동영상
    ### 게시된 동영상
    ### 생방송 중
    ### 예정된 실시간 스트림
    ### 이전 실시간 스트림
    ## 재생목록
    ### 생성된 재생목록
    ### 단일 재생목록
    ### 저장된 재생목록
    ### 여러 재생목록
    ### 게시된 재생목록
    ## 채널
    ### 구독정보
    ### 맞춤 분류
    ## 기타
    ### 최근 활동
    ### 최근 동영상
    homeTab = ''
    homeTab_sections = ''
    # 전체 동영상
    # 업로드한 동영상
    # ...
    # 실시간 스트림

    # 인기 동영상
    # 추가된 날짜(오래된순)
    # 추가된 날짜(최신순)
    videoTab = ''
    # 최근 추가된 동영상순
    ## 만든 날짜(오래된 순)
    ## 만든 날짜(최신순)
    playlistTab = ''
    # 모든 재생목록
    # 생성된 재생목록
    # ...
    playlistTab_sections = ''
    channelTab = ''
    channelTab_recommendChannel = ''
    cummunityTab = ''
    informTab = ''
    informTab_desc = ''
    informTab_country = ''
    informTab_link = ''
    informTab_registerDate = ''
    informTab_viewCount = 0

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

    def setChannelID(self, channelID):
        self.channelID = channelID

    def getChannelID(self):
        return self.channelID

    def setChannelTitle(self, channelURL):
        try:
            chromedriver = '../chromedriver.exe'
            chromeBrowser = webdriver.Chrome(chromedriver)
            chromeBrowser.get(channelURL)
            self.channelTitle = WebDriverWait(chromeBrowser, 3).until(EC.presence_of_element_located((By.ID, 'channel-title'))).text
        except:
            print("empty!")
        finally:
            chromeBrowser.quit()

    def getChannelTitle(self):
        return self.channelTitle

############################################################################################################################
# Main
############################################################################################################################
ch = Channel()

# 몽고DB connection
conn = pymongo.MongoClient('localhost', 27017)
db = conn.get_database('youtube_channel')
collection = db.get_collection('channel')

'''
print('### 소셜러스 구독자 랭킹에서 데이터 가져오기 ###')
startTime = time.time()
rankingList = getSocialerusRanking()

endTime = time.time()
print('경과 시간 : ' + str(round((endTime-startTime)/60, 2)) + '분')
print('유튜버 수 : ' + str(len(rankingList)) + '명')
# 7.28 2627
# 7.29 2624
# 7.30 2623

# 채널제목, 채널카테고리, 채널ID 저장
for i in range(len(rankingList)-1):
    collection.insert_one(
        {"CID": rankingList[i][2],
         "CName": rankingList[i][0],
         "Category": rankingList[i][1]
         })
'''
selectAll = collection.find({}) # return type : cursor

start = time.time()

for selectOne in selectAll:
    ch.setChannelID(selectOne['CID'])
    channelURL = 'https://www.youtube.com/channel/' + ch.getChannelID()
    ch.setChannelTitle(channelURL)
    collection.update({'_id': selectOne['_id']}, {'$set': {'ChannelName': ch.getChannelTitle()}})
    print(ch.getChannelTitle())

print(collection.count())

end = time.time()

print('경과 시간 : ' + str(round((start-end)/60,2)) + '분')





