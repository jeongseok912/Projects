from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from bs4 import BeautifulSoup
import re
import time

# 정의 모듈
from myutil import pcolors

class SquenceError(Exception):
    def __init__(self, msg):
        self.msg = msg
    def __str__(self):
        return self.msg

class Channel:
    def __init__(self):
        self.driver = webdriver.Chrome('../chromedriver.exe')
        self.channel_id = ''
        self.video_cnt = 0

        # 홈탭 변수
        self.home = ''
        self.home_src = ''
        self.home_parser = ''
        self.main_video_enable = False
        self.section_cnt = 0
        self.reco_section_title = ''
        # 동영상탭 변수
        self.videoTab = ''
        self.videoTab_src = ''
        self.videoTab_parser = ''
        # 재생목록탭 변수
        self.playlistsTab = ''
        self.playlistsTab_src = ''
        self.playlistsTab_parser = ''
        self.playlists_cnt = 0
        # 토론탭 변수
        self.discussionTab = ''
        self.discussionTab_src = ''
        self.discussionTab_parser = ''
        self.discussionTab_enable = True
        self.discussion_cnt = 0
        # 커뮤니티탭 변수
        self.communityTab = ''
        self.communityTab_src = ''
        self.communityTab_parser = ''
        self.communityTab_enable = True
        self.post_cnt = 0
        # 정보탭 변수
        self.aboutTab = ''
        self.aboutTab_src = ''
        self.aboutTab_parser = ''
        self.channel_title = ''
        self.subscriber_num = 0
        self.desc_size = 0
        self.desc = ''
        self.location = ''
        self.link_cnt = 0
        self.instagram = False
        self.facebook = False
        self.twitter = False
        self.googleplus = False
        self.naver_cafe = False
        self.naver_blog = False
        self.tistory = False
        self.afreeca = False
        self.youtube = False
        self.tumblur = False
        self.others = False
        self.join_date = ''
        self.total_view_cnt = 0

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
            # 채널 제목 가져오기
            self.channel_title = self.aboutTab_parser.select_one('#channel-title').text
            # 구독자 수 가져오기
            subs_cnt_parser = self.aboutTab_parser.select_one('#subscriber-count').text[4:-1]
            if subs_cnt_parser.find(',') != -1:
                subs_cnt_parser = int(subs_cnt_parser.replace(',', ''))
            if subs_cnt_parser == '':
                self.subscriber_num = 0
            else:
                self.subscriber_num = int(subs_cnt_parser)
            # 정보탭 섹션 정보 가져오기
            elements_left = self.aboutTab_parser.select('#left-column > div')
            for element_left in elements_left:
                about_section_name = element_left.select_one('.subheadline').text
                # 설명 정보 가져오기
                if about_section_name == '설명':
                    self.desc_size = len(element_left.select_one('#description').text)
                    self.desc = element_left.select_one('#description').text
                # 장소 정보 가져오기
                elif about_section_name == '세부정보':
                    locVlaue_selector = 'table > tbody > tr:nth-of-type(2) > td:nth-of-type(2) > yt-formatted-string'
                    if element_left.select_one(locVlaue_selector).text != '':
                        self.location = element_left.select_one(locVlaue_selector).text
                    else:
                        self.location = 'NA'
                # 링크 정보 가져오기
                elif about_section_name == '링크':
                    links = element_left.select('#link-list-container > a')
                    self.link_cnt = len(links)
                    cnt = 0
                    for link in links:
                        if re.compile('instagram', re.I).search(link['href']):
                            self.instagram = True
                            cnt += 1
                        elif re.compile('facebook', re.I).search(link['href']):
                            self.facebook = True
                            cnt += 1
                        elif re.compile('twitter', re.I).search(link['href']):
                            self.twitter = True
                            cnt += 1
                        elif re.compile('plus.google', re.I).search(link['href']):
                            self.googleplus = True
                            cnt += 1
                        elif re.compile('cafe.naver', re.I).search(link['href']):
                            self.naver_cafe = True
                            cnt += 1
                        elif re.compile('blog.naver', re.I).search(link['href']):
                            self.naver_blog = True
                            cnt += 1
                        elif re.compile('tistory', re.I).search(link['href']):
                            self.tistory = True
                            cnt += 1
                        elif re.compile('afreeca', re.I).search(link['href']):
                            self.afreeca = True
                            cnt += 1
                        elif re.compile('youtube', re.I).search(link['href']):
                            self.youtube = True
                            cnt += 1
                        elif re.compile('tumblur', re.I).search(link['href']):
                            self.tumblur = True
                            cnt += 1
                    if self.link_cnt - cnt != 0:
                        self.others = True
            # 정보탭 통계 섹션 정보 가져오기
            self.join_date = self.aboutTab_parser.select_one('#right-column > yt-formatted-string:nth-of-type(2)').text.split(': ')[1]
            if self.aboutTab_parser.select_one('#right-column > yt-formatted-string:nth-of-type(3)').text != '':
                self.total_view_cnt = self.aboutTab_parser.select_one('#right-column > yt-formatted-string:nth-of-type(3)').text.split(' ')[1][:-1]
                if self.total_view_cnt.find(',') != -1:
                    self.total_view_cnt = int(self.total_view_cnt.replace(',', ''))
        except Exception as e:
            print(pcolors.EXPT + self.channel_title + ', getAboutTabSource(), ' + str(e) + pcolors.END)


    def getHomeSource(self):
        try:
            # 홈 소스 가져오기
            self.driver.get(self.home)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.scrollDown()
            self.home_src = self.driver.page_source
            self.home_parser = BeautifulSoup(self.home_src, 'html.parser')
            # 섹션 개수, 메인비디오 사용여부 가져오기
            if self.home_parser.select_one('ytd-channel-video-player-renderer') is None:
                self.section_cnt = len(self.home_parser.select('#image-container'))
            else:
                self.main_video_enable = True
                self.section_cnt = len(self.home_parser.select('#image-container')) + 1
        except Exception as e:
            print(pcolors.EXPT + self.channel_title + ', getHomeSource(), ' + str(e) + pcolors.END)

    def getRecommendChannel(self):
        try:
            elements = self.home_parser.select('ytd-vertical-channel-section-renderer')
            for element in elements:
                if element.select_one('#title').text != '관련 채널':
                    yield element.select_one('#title').text
                    reco_Infos = element.select('#channel-info')
                    for reco_Info in reco_Infos:
                        yield reco_Info.select_one('span').text
                        yield 'https://www.youtube.com' + reco_Info['href']
        except Exception as e:
            print(pcolors.EXPT + self.channel_title + ', getRecommendChannel(), '    + str(e) + pcolors.END)

    # 시간 오래걸리니까 보류
    def getVideoTabSource(self):
        try:
            # 비디오탭 소스 가져오기
            self.driver.get(self.videoTab)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.scrollDown()
            self.videoTab_src = self.driver.page_source
            self.videoTab_parser = BeautifulSoup(self.videoTab_src, 'html.parser')
            self.video_cnt = len(self.videoTab_parser.select('#items > ytd-grid-video-renderer'))
        except Exception as e:
            print(pcolors.EXPT + self.channel_title + ', getVideoTabSource(), ' + str(e) + pcolors.END)

    def getVideoData(self):
        try:
            # 영상별 링크, 제목, 조회수, 경과시간 가져오기
            i = 0
            for href in self.videoTab_parser.select('#thumbnail'):
                span = self.videoTab_parser.select('#metadata-line > span:nth-of-type(1)')[i].text
                view_cnt = 0
                cnt10000 = re.compile('조회수 \d+만회')
                cnt10000_dot = re.compile('조회수 \d+[.]\d+만회')
                cnt1000 = re.compile('조회수 \d+천회')
                cnt1000_dot = re.compile('조회수 \d+[.]\d+천회')
                cnt = re.compile('조회수 \d+회')

                if cnt10000.search(span):
                    rep = cnt10000.sub(span[4:-2] + '0000', span)
                    view_cnt = int(rep)
                if cnt10000_dot.search(span):
                    rep = cnt10000_dot.sub(span[4:-4] + span[-3:-2] + '000', span)
                    view_cnt = int(rep)
                if cnt1000.search(span):
                    rep = cnt1000.sub(span[4:-2] + '000', span)
                    view_cnt = int(rep)
                if cnt1000_dot.search(span):
                    rep = cnt1000_dot.sub(span[4:-4] + span[-3:-2] + '00', span)
                    view_cnt = int(rep)
                if cnt.search(span):
                    e = span[4:-1]
                    view_cnt = int(e)
                yield {
                    'URL': 'https://www.youtube.com' + href.get('href'),
                    'Title': self.videoTab_parser.select('#video-title')[i].text,
                    'ViewCount': view_cnt,
                    'ElapsedTime': self.videoTab_parser.select('#metadata-line > span:nth-of-type(2)')[i].text
                }
                i += 1
        except Exception as e:
            print(pcolors.EXPT + self.channel_title + ', getVideoData(), ' + str(e) + pcolors.END)

    def getVideoCount(self):
        try:
            video_cnt_element = ''
            try:
                try:
                    search = self.driver.find_element_by_css_selector('#form').get_attribute('action').split('/')[-2]
                    search_query = 'https://www.youtube.com/results?search_query=' + search
                    self.driver.get(search_query)
                    video_cnt_element = self.driver.find_element_by_css_selector('#video-count').text[4:-1]
                except NoSuchElementException:
                    print(pcolors.WARNING + self.channel_title + ', getVideoCount(), Can\'t find the video count with action, So scraper will find it with channel_title' + pcolors.END)
                    search_query = 'https://www.youtube.com/results?search_query=' + self.channel_title
                    self.driver.get(search_query)
                    video_cnt_element = self.driver.find_element_by_css_selector('#video-count').text[4:-1]
            except NoSuchElementException:
                print(pcolors.WARNING + self.channel_title + ', getVideoCount(), Can\'t find the video count with channel_title, So scraper will change a query' + pcolors.END)
                search_query = 'https://www.youtube.com/results?search_query=' + self.channel_title + ' 채널'
                self.driver.get(search_query)
                video_cnt_element = self.driver.find_element_by_css_selector('#video-count').text[4:-1]
        except Exception as e:
            print(pcolors.EXPT + self.channel_title + ', getVideoCount(), ' + str(e) + pcolors.END)
        finally:
            if video_cnt_element.find(',') != -1:
                video_cnt_element = video_cnt_element.replace(',', '')
            if video_cnt_element != '':
                self.video_cnt = int(video_cnt_element)
            else:
                self.video_cnt = 0

    def getPlaylistsTabSource(self):
        try:
            # 재생목록탭 소스 가져오기
            self.driver.get(self.playlistsTab)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            self.scrollDown()
            self.playlistsTab_src = self.driver.page_source
            self.playlistsTab_parser = BeautifulSoup(self.playlistsTab_src, 'html.parser')
            self.playlists_cnt = len(self.playlistsTab_parser.select('#items > ytd-grid-playlist-renderer'))
        except Exception as e:
            print(pcolors.EXPT + self.channel_title + ', getPlaylistsTabSource(), ' + str(e) + pcolors.END)

    def getDiscussionTabSource(self):
        try:
            # 토론탭 소스 가져오기
            self.driver.get(self.discussionTab)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            # 홈으로 넘어가는 경우 고려
            tab_selector = '#tabsContent > paper-tab.style-scope.ytd-c4-tabbed-header-renderer.iron-selected'
            if self.driver.find_element_by_css_selector(tab_selector + ' > div').text == '토론' and self.driver.find_element_by_css_selector(tab_selector).get_attribute('aria-selected'):
                self.scrollDown()
                self.discussionTab_src = self.driver.page_source
                self.discussionTab_parser = BeautifulSoup(self.discussionTab_src, 'html.parser')
                self.discussion_cnt = int(
                self.discussionTab_parser.select_one('#count > yt-formatted-string').text[3:-1])
            elif self.driver.find_element_by_css_selector(tab_selector + ' > div').text == '홈' and self.driver.find_element_by_css_selector(tab_selector).get_attribute('aria-selected'):
                self.discussionTab_enable = False
                self.discussion_cnt = 0
        except NoSuchElementException as n:
            self.discussionTab_enable = False
            self.discussion_cnt = 0
            print(pcolors.EXPT + self.channel_title + ', getDiscussionTabSource(), ' + str(n) + pcolors.END)
        except Exception as e:
            print(pcolors.EXPT + self.channel_title + ', getDiscussionTabSource(), ' + str(e) + pcolors.END)

    def getCommunityTabSource(self):
        try:
            # 커뮤니티탭 소스 가져오기
            self.driver.get(self.communityTab)
            wait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
            tab_selector = '#tabsContent > paper-tab.style-scope.ytd-c4-tabbed-header-renderer.iron-selected'
            if self.driver.find_element_by_css_selector(tab_selector + ' > div').text == '커뮤니티' and self.driver.find_element_by_css_selector(tab_selector).get_attribute('aria-selected'):
                self.scrollDown()
                self.communityTab_src = self.driver.page_source
                self.communityTab_parser = BeautifulSoup(self.communityTab_src, 'html.parser')
                self.post_cnt = len(self.communityTab_parser.select('#contents > ytd-backstage-post-thread-renderer'))
            elif self.driver.find_element_by_css_selector(tab_selector + ' > div').text == '홈' and self.driver.find_element_by_css_selector(tab_selector).get_attribute('aria-selected'):
                self.communityTab_enable = False
                self.post_cnt = 0
        except Exception as e:
            print(pcolors.EXPT + self.channel_title + ', getCommunityTabSource(), ' + str(e) + pcolors.END)


    # 시간 오래걸리니까 보류
    def moveToVideo(self, url):
        self.driver.get(url)
        print(wait(self.driver, 3).until(EC.presence_of_element_located((By.CSS_SELECTOR, '#container > h1 > yt-formatted-string'))).text)
        print(self.driver.find_element_by_css_selector('#count > yt-view-count-renderer > span.view-count.style-scope.yt-view-count-renderer').text)

if __name__ == '__main__':
    print('execute the \"mainProcess.py\"!')
    exit()
