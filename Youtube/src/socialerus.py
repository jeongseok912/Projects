from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
import pymongo
import time

conn = pymongo.MongoClient('localhost', 27017)
db = conn.get_database('youtube')
collection = db.get_collection('channel')

def getSpendTime(start, end):
    spendTime_sec = int(end - start)
    if spendTime_sec < 60:
        print('경과 시간 : ' + str(spendTime_sec) + '초')
    elif spendTime_sec >= 60:
        print('경과 시간 : ' + str(int(spendTime_sec/60)) + '분 ' + str(int(spendTime_sec%60)) + '초')
    elif spendTime_sec >= 3600:
        print('경과 시간 : ' + str(int(spendTime_sec/3600)) + '시간 ' + str(int((spendTime_sec%3600)/60)) + '분 ' + str(int((spendTime_sec%3600)%60)) + '초')

# 소셜러스 구독자 랭킹
def getSocialerusRanking():
    chromedriver = '../chromedriver.exe'
    # NonHeadless
    chromeBrowser = webdriver.Chrome(chromedriver)

    '''
    # Headless
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("headless")
    chrome_options.add_argument("window-size=1920x1080")
    chrome_options.add_argument("disable-gpu")
    chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36")
    chromeBrowser = webdriver.Chrome(chromedriver, chrome_options=chrome_options)
    chromeBrowser.execute_script("Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
    chromeBrowser.execute_script("Object.defineProperty(navigator, 'plugins', {get: function() {return [1,2,3,4,5]}})")
    '''
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
        iArr = [channelID, category.text]
        rankingList.append(iArr)
    return rankingList

def enableGetSocialerusData(triger):
    if triger == True:
        # 소셜러스 구독자 랭킹에서 데이터 가져오기
        start = time.clock()
        print('\n### 소셜러스 구독자 랭킹에서 데이터 가져오기 ###')
        rankingList = getSocialerusRanking()
        print('수집 유튜버 수 : ' + str(len(rankingList)) + '명')

        # MongoDB에 랭킹 데이터 저장
        for i in range(len(rankingList)):
            collection.insert_one(
                {"CID": rankingList[i][0],
                 "Category": rankingList[i][1]})
        end = time.clock()
        getSpendTime(start, end)

if __name__ == '__main__':
    pass