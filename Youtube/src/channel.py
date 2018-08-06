from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException, WebDriverException
from bs4 import BeautifulSoup

class SquenceError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Channel:
    def __init__(self):
        self.channelId = ''
        self.Home = ''
        self.Home_title = ''

        self.videoTab = ''
        self.videoNum = 0
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
        '''
        # headless
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("headless")
        self.chrome_options.add_argument("window-size=1920x1080")
        self.chrome_options.add_argument("disable-gpu")
        self.chrome_options.binary_location = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        self.chrome_options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36")
        self.chromeBrowser = webdriver.Chrome(self.chromedriver, chrome_options=self.chrome_options)
        self.chromeBrowser.execute_script(
            "Object.defineProperty(navigator, 'languages', {get: function() {return ['ko-KR', 'ko']}})")
        self.chromeBrowser.execute_script(
            "Object.defineProperty(navigator, 'plugins', {get: function() {return [1,2,3,4,5]}})")
        '''

    def __del__(self):
        self.chromeBrowser.quit()

    def setChannelHomeURL(self, channelID):
        self.Home = 'https://www.youtube.com/channel/' + channelID
        self.videoTab = self.Home + '/videos'
        self.channelId = channelID

    def popupChannelHome(self):
        try:
            self.chromeBrowser.get(self.Home)
        except WebDriverException:
            raise SquenceError('execute "setChannelHomeURL()" method!')

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

    def getVideoTabHTML(self):
        try:
            self.chromeBrowser.get(self.videoTab)
            WebDriverWait(self.chromeBrowser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#items > ytd-grid-video-renderer:nth-child(30)')))
            i = 30
            while True:
                self.chromeBrowser.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
                nth = '#items > ytd-grid-video-renderer:nth-child(' + str(i) + ')'
                WebDriverWait(self.chromeBrowser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, nth)))
                i += 30
        except TimeoutException as t:
            print(t)
        finally:
            page = self.chromeBrowser.page_source
            self.videoTab_html = BeautifulSoup(page, 'html.parser')

    def getVideoNum(self):
        search_query = 'https://www.youtube.com/results?search_query=' + self.Home_title
        self.chromeBrowser.get(search_query)
        return int(self.chromeBrowser.find_element_by_css_selector('#video-count').text[4:-1].replace(',', ''))
        #return len(self.videoTab_html.select('#video-title'))

    def getVideoListData(self):
        i = 0
        for href in self.videoTab_html.select('#thumbnail'):
            span = self.videoTab_html.select('#metadata-line > span:nth-of-type(1)')[i]
            viewNum = 0
            if span.text[-2:-1] == '만':
                if span.text[-4:-5] == '.':
                    span.text[4:-2].replace('.', '') + '000'
                viewNum = int(span.text[4:-2] + '0000')
            elif span.text[-2:-1] == '천':
                viewNum = int(span.text[4:-2] + '000')
                span.text[4:-2].
            yield {
                    'URL': 'https://www.youtube.com' + href.get('href'),
                    'Title': self.videoTab_html.select('#video-title')[i].text,
                    'ViewCount': viewNum,
                    'ElapsedTime': self.videoTab_html.select('#metadata-line > span:nth-of-type(2)')[i].text
                   }
            i += 1

    def moveToVideo(self, url):
        self.chromeBrowser.get(url)
        print(WebDriverWait(self.chromeBrowser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#container > h1 > yt-formatted-string'))).text)
        print(self.chromeBrowser.find_element_by_css_selector('#count > yt-view-count-renderer > span.view-count.style-scope.yt-view-count-renderer').text)



if __name__ == '__main__':
    pass
