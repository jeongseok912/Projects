from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotVisibleException

# 소셜러스 구독자 랭킹
def getSocialerusRanking():
    # NonHeadless
    chromeBrowser = webdriver.Chrome('../chromedriver.exe')

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

if __name__ == '__main__':
    print('execute the \"mainProcess.py\"!')
    exit()