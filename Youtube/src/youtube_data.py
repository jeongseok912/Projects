# created by jeongseok
# jeongseok912@gmail.com
# 2018.07.29

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, ElementNotVisibleException
import pymongo


# 소셜러스 구독자 랭킹
def getSocialerusRanking():
    chromedriver = '../chromedriver.exe'
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("disable-gpu")
    chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36")
    chromeBrowser = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
    chromeBrowser.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    chromeBrowser.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return [1,2,3,4,5]}})")
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
    except TimeoutException as t:
        print(t)
    except ElementNotVisibleException as e:
        print(e)
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

def enableGetSocialerusData(triger):
    if triger == True:
        # 소셜러스 구독자 랭킹에서 데이터 가져오기
        print('\n### 소셜러스 구독자 랭킹에서 데이터 가져오기 ###')
        rankingList = getSocialerusRanking()
        print('유튜버 수 : ' + str(len(rankingList)) + '명')

        # MongoDB에 랭킹 데이터 저장
        print('\n### 몽고DB에 랭킹데이터 저장하기 ###')
        for i in range(len(rankingList) - 1):
            collection.insert_one(
                {"CID": rankingList[i][0],
                 "Category": rankingList[i][1]})

class Channel:
    def __init__(self):
        self.Home = ''
        self.Home_title = ''

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

    def setChannelHomeURL(self, channelID):
        self.Home = 'https://www.youtube.com/channel/' + channelID

    def getChannelHomeURL(self):
        return self.Home

    def popupChannel(self):
        self.chromeBrowser.get(self.Home)

    def getChannelTitle(self):
        try:
            chTitleElement = WebDriverWait(self.chromeBrowser, 3).until(EC.presence_of_element_located((By.ID, 'channel-title')))
            if chTitleElement is not None:
                self.Home_title = chTitleElement.text
            else:
                self.Home_title = ''
        except Exception as e:
            print(e)
        return self.Home_title

    def getSubscriberNum(self):
        return int(self.chromeBrowser.find_element_by_css_selector('#subscriber-count').text[4:-1].replace(',',''))

    def hasHomeVideoPlayer(self):
        try:
            self.chromeBrowser.find_element_by_css_selector('ytd-channel-video-player-renderer')
            return True
        except NoSuchElementException:
            return False

    def getHomeSectionNum(self):
        return len(self.chromeBrowser.find_elements_by_css_selector('#image-container'))

    def getRecommendChannel(self):
        self.Home_recommendChannel = []
        elements = self.chromeBrowser.find_elements_by_css_selector('ytd-vertical-channel-section-renderer')
        for element in elements:
            if element.find_element_by_css_selector('#title').text != '관련 채널':
                self.Home_recommendChannel.append(element.find_element_by_css_selector('#title').text)
                recoInfos = element.find_elements_by_css_selector('#channel-info')
                for recoInfo in recoInfos:
                    self.Home_recommendChannel.append(recoInfo.get_attribute('href'))
        return self.Home_recommendChannel

    def getVideoNum(self, cid):
        search_query = 'https://www.youtube.com/results?search_query=' + cid
        self.chromeBrowser.get(search_query)
        return int(self.chromeBrowser.find_element_by_css_selector('#video-count').text[4:-1].replace(',', ''))

############################################################################################################################
# Main
############################################################################################################################
# 몽고DB connection
conn = pymongo.MongoClient('localhost', 27017)
db = conn.get_database('youtube')
collection = db.get_collection('channel')

# 소셜러스 데이터 가져올지 트리거
enableGetSocialerusData(False)

# 채널 데이터 가져오기
print('\n### 채널 데이터 가져오기 ###')
selectAll = collection.find({}, no_cursor_timeout=True).limit(5) # return type: cursor
cnt = 0

ch = Channel()
for selectOne in selectAll:
    ch.setChannelHomeURL(selectOne['CID'])
    ch.popupChannel()
    if ch.hasHomeVideoPlayer() == True:
        totalSectionNum = ch.getHomeSectionNum() + 1
    else:
        totalSectionNum = ch.getHomeSectionNum()
    print('###' + ch.getChannelTitle() + '###')
    print('-----------------------')
    ch.getRecommendChannel()
    # 가져온 데이터 저장
    collection.update({'_id': selectOne['_id']}, {'$set': {
        'ChannelTitle': ch.getChannelTitle(),
        'Subscriber': ch.getSubscriberNum(),
        'HomeTab': {'SectionNum': ch.getHomeSectionNum(),
                    'VideoPlayer': ch.hasHomeVideoPlayer(),
                    'TotalSectionNum': totalSectionNum,
                    'recommendChannel': ch.getRecommendChannel()},
        'VideoTab': {'videoNum': ch.getVideoNum(ch.getChannelTitle())
                     }
        }})
    cnt += 1
print('cnt : ' + str(cnt))
del ch
selectAll.close()





