# created by jeongseok
# jeongseok912@gmail.com
# 2018.07.29

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException
import time

# 소셜러스 구독자 랭킹
def getSocialerusRanking():
    chromedriver = '../chromedriver.exe'
    chromeBrowser = webdriver.Chrome(chromedriver)
    chromeBrowser.get("https://socialerus.com/ranking/total_ranking.asp?pb_orderBy=CR_SBUSCRIBER_COUNT")
    try:
        # Explicit Waits
        # WebDriverWait는 성공적으로 반환될 때까지 0.5초마다 ExpectedCondition을 호출한다.
        # ExpectedCondition의 정상 리턴값 : true or not null

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

############################################################################################################################
# Main
############################################################################################################################
print('### 소셜러스 구독자 랭킹에서 데이터 가져오기 ###')
startTime = time.time()
rankingList = getSocialerusRanking()

endTime = time.time()
print('경과 시간 : ' + str(round((endTime-startTime)/60, 2)) + '분')
print('유튜버 수 : ' + str(len(rankingList)) + '명')

# 7.28 2627
# 7.29 2624

