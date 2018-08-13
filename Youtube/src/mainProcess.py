# created by jeongseok
# jeongseok912@gmail.com
# 2018.07.29

import pymongo
from multiprocessing import Pool
import os

# 정의 모듈
import socialerus as sr
import channel
from myutil import pcolors, times

# 몽고DB connection
conn = pymongo.MongoClient('localhost', 27017)
db = conn.get_database('youtube')
collection = db.get_collection('channel')

def enableGetSocialerusData(triger):
    if triger == True:
        # 소셜러스 구독자 랭킹에서 데이터 가져오기
        times.START
        print('### 소셜러스 구독자 랭킹에서 데이터 가져오기 ###')
        rankingList = sr.getSocialerusRanking()
        print('수집 유튜버 수 : ' + str(len(rankingList)) + '명')

        # MongoDB에 랭킹 데이터 저장
        for i in range(len(rankingList)):
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.CRUD + ' (insert) ' + pcolors.END + str(collection.insert_one(
                {
                    "CID": rankingList[i][0],
                    "Category": rankingList[i][1]
                }
            )))
        times.getSpendTime()

def saveData(cursor):
    # 데이터 가져와서 mongodb에 저장
    try:
        ch = channel.Channel()
        for doc in cursor:
            times.START
            # 데이터 가져오기
            ch.setChannelHomeURL(doc['CID'])
            # 정보탭 정보 가져오기
            ch.getAboutTabSource()
            # 홈 정보 가져오기
            ch.getHomeSource()
            # 비디오탭 정보 가져오기
            # ch.getVideoTabSource()
            # 유튜브 검색 엔진에서 비디오 수 가져오기
            ch.getVideoCount()
            # 재생목록탭 정보 가져오기
            ch.getPlaylistsTabSource()
            # 토론탭 정보 가져오기
            ch.getDiscussionTabSource()
            # 커뮤니티탭 정보 가져오기
            ch.getCommunityTabSource()

            # mongodb에 저장
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.CRUD + ' (update) ' + pcolors.END + str(
                doc.get('_id')) + ' - ' + ch.channel_title + ', ' + ch.channel_id + ', ' + str(
                collection.update({'_id': doc['_id']}, {'$set':
                    {
                        'ChannelTitle': ch.channel_title,
                        'SubscriberNum': ch.subscriber_num,
                        'AboutTab':
                            {
                                'DescSize': ch.desc_size,
                                'Description': ch.desc,
                                'Loc': ch.location,
                                'LinkCount': ch.link_cnt,
                                'Link':
                                    {
                                        'Instagram': ch.instagram,
                                        'Facebook': ch.facebook,
                                        'Google+': ch.googleplus,
                                        'NaverCafe': ch.naver_cafe,
                                        'NaverBlog': ch.naver_blog,
                                        'Tistory': ch.tistory,
                                        'Afreeca': ch.afreeca,
                                        'Youtube': ch.youtube,
                                        'Tumblur': ch.tumblur,
                                        'Others': ch.others
                                    },
                                'JoinDate': ch.join_date,
                                'TotalViewCount': ch.total_view_cnt
                            },
                        'HomeTab':
                            {
                                'MainVideo': ch.main_video_enable,
                                'Section': ch.section_cnt,
                                'RecommendChannel': [reco for reco in ch.getRecommendChannel()]
                            },
                        'VideoCount': ch.video_cnt,
                        'PlaylistCount': ch.playlists_cnt,
                        'DiscussionVitalization': ch.discussionTab_enable,
                        'DiscussionCount': ch.discussion_cnt,
                        'CommunityVitalization': ch.communityTab_enable,
                        'CommunityTabPostCount': ch.playlists_cnt
                    }
                })))
            times.getSpendTime()

            # 리스트 전처리 - 국내 채널 선정(location = 한국 or '')
            # 리스트 전처리 - 구독자수 내림차순 정렬
        del ch
    except Exception as e:
        print(e)
    finally:
        cursor.close()

def getData(num):
    try:
        # 프로세스마다 실행할 리스트 범위 지정
        div = 6
        divList = round(collection.find({}, {'CID': 1}).count() / div)
        if num == 0:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + ': 0 - ' + str(divList))
            cursor1 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).limit(100)
            cursor2 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(100).limit(100)
            cursor3 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(200).limit(100)
            cursor4 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(300).limit(100)
            cursor5 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(400).limit(divList - 400)
        elif num == 1:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + ': ' + str(divList+1) + ' - ' + str(divList*2))
            cursor1 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList).limit(100)
            cursor2 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList + 100).limit(100)
            cursor3 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList + 200).limit(100)
            cursor4 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList + 300).limit(100)
            cursor5 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList + 400).limit(divList - 400)
        elif num == 2:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + ': ' + str(divList*2+1) + ' - ' + str(divList*3))
            cursor1 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 2).limit(100)
            cursor2 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 2 + 100).limit(100)
            cursor3 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 2 + 200).limit(100)
            cursor4 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 2 + 300).limit(100)
            cursor5 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 2 + 400).limit(divList - 400)
        elif num == 3:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + ': ' + str(divList*3+1) + ' - ' + str(divList*4))
            cursor1 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 3).limit(100)
            cursor2 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 3 + 100).limit(100)
            cursor3 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 3 + 200).limit(100)
            cursor4 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 3 + 300).limit(100)
            cursor5 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 3 + 400).limit(divList - 400)
        elif num == 4:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + ': ' + str(divList*4+1) + ' - ' + str(divList*5))
            cursor1 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 4).limit(100)
            cursor2 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 4 + 100).limit(100)
            cursor3 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 4 + 200).limit(100)
            cursor4 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 4 + 300).limit(100)
            cursor5 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 4 + 400).limit(divList - 400)
        elif num == 5:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + ': ' + str(divList*5+1) + ' - ' + str(divList*6))
            cursor1 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 5).limit(100)
            cursor2 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 5 + 100).limit(100)
            cursor3 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 5 + 200).limit(100)
            cursor4 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 5 + 300).limit(100)
            cursor5 = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList * 5 + 400).limit(divList - 400)

        saveData(cursor1)
        saveData(cursor2)
        saveData(cursor3)
        saveData(cursor4)
        saveData(cursor5)
    except Exception as e:
        print(e)

def excuteMultiProcessing():
    # 프로세스 할당
    proc_num = 6
    p = Pool(processes=proc_num)
    p.map(getData, range(proc_num))

if __name__ == '__main__':
    times.START
    # TODO: 배열 리턴 -> 제너레이터로 변경
    # 소셜러스 데이터 트리
    enableGetSocialerusData(False)
    # 멀티프로세싱으로 youtube에서 데이터 가져오기
    excuteMultiProcessing()
    times.getSpendTime()







