from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup

class Channel:
    def __init__(self):
        self.channelId = ''
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
        self.videoTab = self.Home + '/videos'
        self.channelId = channelID

    def getChannelHomeURL(self):
        return self.Home

    def popupChannelHome(self):
        self.chromeBrowser.get(self.Home)

    def getChannelTitle(self):
        try:
            chTitleElement = WebDriverWait(self.chromeBrowser, 10).until(EC.presence_of_element_located((By.ID, 'channel-title')))
            if chTitleElement is not None:
                self.Home_title = chTitleElement.text
            else:
                self.Home_title = ''
        except Exception as e:
            print(e)
        finally:
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
        elements = self.chromeBrowser.find_elements_by_css_selector('ytd-vertical-channel-section-renderer')
        for element in elements:
            if element.find_element_by_css_selector('#title').text != '관련 채널':
                yield element.find_element_by_css_selector('#title').text
                recoInfos = element.find_elements_by_css_selector('#channel-info')
                for recoInfo in recoInfos:
                    yield recoInfo.get_attribute('href')

    def getVideoNum(self):
        search_query = 'https://www.youtube.com/results?search_query=' + self.Home_title
        self.chromeBrowser.get(search_query)
        return int(self.chromeBrowser.find_element_by_css_selector('#video-count').text[4:-1].replace(',', ''))

    def getVideoData(self):
        self.chromeBrowser.get(self.videoTab)
        lastHeight = self.chromeBrowser.execute_script("return document.documentElement.scrollHeight")
        print('lastHeight : ' + str(lastHeight))
        while True:
            self.chromeBrowser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            self.chromeBrowser.implicitly_wait(0.5)
            newHeight = self.chromeBrowser.execute_script("return document.documentElement.scrollHeight")
            print('newHeight : ' + str(newHeight))
            if newHeight == lastHeight:
                break
            lastHeight = newHeight
        page = self.chromeBrowser.page_source
        html = BeautifulSoup(page, 'html.parser')
        for href in html.select('#thumbnail'):
            href.get('href')
        for video_title in html.select('#video-title'):
            print(video_title.text)
        print(len(html.select('#video-title')))
