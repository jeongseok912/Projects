from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import re
import time

def getSpendTime(start):
    end = time.clock()
    spendTime_sec = int(end - start)
    if spendTime_sec < 60:
        print('경과 시간 : ' + str(spendTime_sec) + '초')
    elif spendTime_sec >= 60:
        print('경과 시간 : ' + str(int(spendTime_sec/60)) + '분 ' + str(int(spendTime_sec%60)) + '초')
    elif spendTime_sec >= 3600:
        print('경과 시간 : ' + str(int(spendTime_sec/3600)) + '시간 ' + str(int((spendTime_sec%3600)/60)) + '분 ' + str(int((spendTime_sec%3600)%60)) + '초')

class SquenceError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Channel:

    def __init__(self):
        self.driver = webdriver.Chrome('../chromedriver.exe')
        self.channel_id = ''

        # 홈탭 변수
        self.home = ''
        self.home_src = ''
        self.home_parser = ''
        # 동영상탭 변수
        self.videoTab = ''
        self.videoTab_src = ''
        self.videoTab_parser = ''
        # 재생목록탭 변수
        self.playlistsTab = ''
        self.playlistsTab_src = ''
        self.playlistsTab_parser = ''
        # 토론탭 변수
        self.discussionTab = ''
        self.discussionTab_src = ''
        self.discussionTab_parser = ''
        # 커뮤니티탭 변수
        self.communityTab = ''
        self.communityTab_src = ''
        self.communityTab_parser = ''
        # 정보탭 변수
        self.aboutTab = ''
        self.aboutTab_src = ''
        self.aboutTab_parser = ''
        self.channel_title = ''
        self.subscriber_num = 0
        self.location = ''

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
        self.driver.quit()

    def scrollDown(self):
        last_height = self.driver.execute_script("return document.documentElement.scrollHeight")
        while True:
            self.driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
            try:
                wait(self.driver, 3).until(
                    lambda driver: driver.execute_script("return document.documentElement.scrollHeight") > last_height)
            except TimeoutException:
                break
            last_height = self.driver.execute_script("return document.documentElement.scrollHeight")

    def setChannelHomeURL(self, cid):
        self.home = 'https://www.youtube.com/channel/' + cid
        self.videoTab = self.home + '/videos?flow=grid&view=0'
        self.playlistsTab = self.home + '/playlists'
        self.discussionTab = self.home + '/discussion'
        self.communityTab = self.home + '/community'
        self.aboutTab = self.home + '/about'
        self.channel_id = cid

    def getAboutTabSource(self):
        try:
            self.driver.get(self.aboutTab)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.scrollDown()
            self.aboutTab_src = self.driver.page_source
            self.aboutTab_parser = BeautifulSoup(self.aboutTab_src, 'html.parser')
            self.channel_title = self.aboutTab_parser.select_one('#channel-title').text
            self.subscriber_num = int(self.aboutTab_parser.select_one('#subscriber-count').text[4:-1].replace(',', ''))
            loc_selector = '#details-container > table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > yt-formatted-string'
            if self.aboutTab_parser.select_one(loc_selector):
                self.location = self.aboutTab_parser.select_one(loc_selector).text
        except TimeoutException as t:
            print(str(t) + 'TimeoutException at ' + self.home)

    def getPageSource(self):
        try:
            # 홈 소스 가져오기
            self.driver.get(self.home)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.scrollDown()
            self.home_src = self.driver.page_source
            self.home_parser = BeautifulSoup(self.home_src, 'html.parser')

            # 비디오탭 소스 가져오기
            self.driver.get(self.videoTab)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.scrollDown()
            self.videoTab_src = self.driver.page_source
            self.videoTab_parser = BeautifulSoup(self.videoTab_src, 'html.parser')

            # 재생목록탭 소스 가져오기
            self.driver.get(self.playlistsTab)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.scrollDown()
            self.playlistsTab_src = self.driver.page_source
            self.playlistsTab_parser = BeautifulSoup(self.playlistsTab_src, 'html.parser')

            # 토론탭 소스 가져오기
            self.driver.get(self.discussionTab)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            if self.driver.find_elements_by_css_selector('#image-container') is None:
                self.scrollDown()
                self.discussionTab_src = self.driver.page_source
                self.discussionTab_parser = BeautifulSoup(self.discussionTab_src, 'html.parser')

            # 커뮤니티탭 소스 가져오기
            self.driver.get(self.communityTab)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            if self.driver.find_elements_by_css_selector('#image-container') is None:
                self.scrollDown()
                self.communityTab_src = self.driver.page_source
                self.communityTab_parser = BeautifulSoup(self.communityTab_src, 'html.parser')
        except Exception as e:
            print(e)

    def hasHomeVideoPlayer(self):
        print('hasHomeVideoPlayer()')
        try:
            self.chromeBrowser.find_element_by_css_selector('ytd-channel-video-player-renderer')
            return True
        except NoSuchElementException:
            return False

    def getHomeSectionNum(self):
        print('getHomeSectionNum()')
        return len(self.chromeBrowser.find_elements_by_css_selector('#image-container'))

    def getRecommendChannel(self):
        print('getRecommendChannel()')
        elements = self.chromeBrowser.find_elements_by_css_selector('ytd-vertical-channel-section-renderer')
        for element in elements:
            if element.find_element_by_css_selector('#title').text != '관련 채널':
                yield element.find_element_by_css_selector('#title').text
                recoInfos = element.find_elements_by_css_selector('#channel-info')
                for recoInfo in recoInfos:
                    yield recoInfo.get_attribute('href')

    def getVideoNum(self):
        print('getVideoNum()')
        search_query = 'https://www.youtube.com/results?search_query=' + self.Home_title
        self.chromeBrowser.get(search_query)
        self.videoNum = int(self.chromeBrowser.find_element_by_css_selector('#video-count').text[4:-1].replace(',', ''))
        return self.videoNum

    def getVideoTabHTML(self):
        print('getVideoTabHTML()')
        p1 = time.clock()
        self.chromeBrowser.get(self.videoTab)
        self.scrollDown()
        page = self.chromeBrowser.page_source
        self.videoTab_html = BeautifulSoup(page, 'html.parser')
        getSpendTime(p1)
        self.videoNum = len(self.chromeBrowser.find_elements_by_css_selector('#items > ytd-grid-video-renderer'))

    def getVideoTabData(self):
        print('getVideoTabData()')
        i = 0
        for href in self.videoTab_html.select('#thumbnail'):
            span = self.videoTab_html.select('#metadata-line > span:nth-of-type(1)')[i].text
            viewNum = 0
            tenThousand = re.compile('조회수 \d+만회')
            dotTenThousand = re.compile('조회수 \d+[.]\d+만회')
            thousand = re.compile('조회수 \d+천회')
            dotThousand = re.compile('조회수 \d+[.]\d+천회')
            count = re.compile('조회수 \d+회')

            if tenThousand.search(span):
                a = tenThousand.sub(span[4:-2] + '0000', span)
                viewNum = int(a)
            if dotTenThousand.search(span):
                b = dotTenThousand.sub(span[4:-4] + span[-3:-2] + '000', span)
                viewNum = int(b)
            if thousand.search(span):
                c = thousand.sub(span[4:-2] + '000', span)
                viewNum = int(c)
            if dotThousand.search(span):
                d = dotThousand.sub(span[4:-4] + span[-3:-2] + '00', span)
                viewNum = int(d)
            if count.search(span):
                e = span[4:-1]
                viewNum = int(e)
            yield {
                    'URL': 'https://www.youtube.com' + href.get('href'),
                    'Title': self.videoTab_html.select('#video-title')[i].text,
                    'ViewCount': viewNum,
                    'ElapsedTime': self.videoTab_html.select('#metadata-line > span:nth-of-type(2)')[i].text
                   }
            i += 1

    def moveToVideo(self, url):
        print('moveToVideo()')
        self.chromeBrowser.get(url)
        print(wait(self.chromeBrowser, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#container > h1 > yt-formatted-string'))).text)
        print(self.chromeBrowser.find_element_by_css_selector('#count > yt-view-count-renderer > span.view-count.style-scope.yt-view-count-renderer').text)

    def getPlaylistsNum(self):
        print('getPlaylists()')
        self.chromeBrowser.get(self.playlistsTab)
        self.scrollDown()
        return len(self.chromeBrowser.find_elements_by_css_selector('#items > ytd-grid-playlist-renderer'))

    def getDiscussionReviewNum(self):
        print('getDiscussionReviewNum()')
        self.chromeBrowser.get(self.discussionTab)
        if self.chromeBrowser.find_elements_by_css_selector('#image-container'):
            return 0
        self.scrollDown()
        return int(self.chromeBrowser.find_element_by_css_selector('#count > yt-formatted-string').text[3:-1])

    def getCommunityPostNum(self):
        print('getCommunityPostNum()')
        self.chromeBrowser.get(self.communityTab)
        if self.chromeBrowser.find_elements_by_css_selector('#image-container'):
            return 0
        self.scrollDown()
        return len(self.chromeBrowser.find_elements_by_css_selector('#contents > ytd-backstage-post-thread-renderer'))


if __name__ == '__main__':
    print('execute the \"mainProcess.py\"!')
    exit()
