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
db = conn.get_database('youtube2')
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
            print('[insert] CID, Category : ' + str(collection.insert_one(
                {
                    "CID": rankingList[i][0],
                    "Category": rankingList[i][1]
                }
            )))
        times.getSpendTime()

def getData(num):
    try:
        # 프로세스마다 실행할 리스트 범위 지정
        div = 6
        divList = round(collection.find({}, {'CID': 1}).count() / div)
        if num == 0:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + 'range: 0 - ' + str(divList))
            cursor = collection.find({}, {'CID': 1}, no_cursor_timeout=True).limit(divList)
        elif num == 1:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + 'range: ' + str(divList+1) + ' - ' + str(divList*2))
            cursor = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList).limit(divList)
        elif num == 2:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + 'range : ' + str(divList*2+1) + ' - ' + str(divList*3))
            cursor = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList*2).limit(divList)
        elif num == 3:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + 'range: ' + str(divList*3+1) + ' - ' + str(divList*4))
            cursor = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList*3).limit(divList)
        elif num == 4:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + 'range: ' + str(divList*4+1) + ' - ' + str(divList*5))
            cursor = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList*4).limit(divList)
        elif num == 5:
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.END + 'range: ' + str(divList*5+1) + ' - ' + str(divList*6))
            cursor = collection.find({}, {'CID': 1}, no_cursor_timeout=True).skip(divList*5)

        # 데이터 가져와서 mongodb에 저장
        ch = channel.Channel()
        for doc in cursor:
            # 데이터 가져오기
            ch.setChannelHomeURL(doc['CID'])
            # 정보탭 정보 가져오기
            ch.getAboutTabSource()
            # 홈 정보 가져오기
            ch.getHomeSource()
            # 비디오탭 정보 가져오기
            ch.getVideoTabSource()
            # 유튜브 검색 엔진에서 비디오 수 가져오기
            # ch.getVideoCount()
            # print('Search browser video cnt:' + str(ch.video_cnt))

            # mongodb에 저장
            print(pcolors.PID + 'PID ' + str(os.getpid()) + pcolors.CRUD + '(update)' + pcolors.END + str(doc.get('_id')) + ' - ' + ch.channel_title + ', ' + str(collection.update({'_id': doc['_id']}, {'$set':
                {
                    'ChannelTitle': ch.channel_title,
                    'SubscriberNum': ch.subscriber_num,
                    'Loc': ch.location,
                    'HomeTab':
                        {
                            'MainVideo': ch.main_video_enable,
                            'Section' : ch.section_cnt,
                            'RecommendChannel': [reco for reco in ch.getRecommendChannel()]
                        },
                    'VideoTab':
                        {
                            'VideoCount': ch.video_cnt,
                            'VideoData': [a for a in ch.getVideoData()]
                        }
                }
            })))

            # 리스트 전처리 - 국내 채널 선정(location = 한국 or '')
            # 리스트 전처리 - 구독자수 내림차순 정렬
        del ch
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


"""
# CID로 채널 데이터 가져와서 저장하기
print('\n### 채널 데이터 저장하기 ###')
#selectAll = collection.find({'CID': 'UCT-_4GqC-yLY1xtTHhwY0hA'}, {'CID':1}, no_cursor_timeout=True) # return type: cursor
selectAll = collection.find({}, {'CID':1}, no_cursor_timeout=True).limit(5) # return type: cursor

ch = channel.Channel()
start = time.clock()
for selectOne in selectAll:
    print('----------------------------------------------')
    # 채널 설정
    ch.setChannelHomeURL(selectOne['CID'])
    # 채널 소스 가져오기
    ch.getPageSource()
    '''
    # 채널홈 이동
    ch.moveToChannelHome()
    # 채널 제목
    channelTitle = ch.getChannelTitle()
    # 구독자 수
    channelSubscriberNum = ch.getSubscriberNum()
    # 홈 섹션 메인비디오플레이어 사용여부
    homeVideoPlayer = ch.hasHomeVideoPlayer()
    # 메인비디오플레이어 섹션을 제외한 사용 섹션 개수
    homeSectionNum = ch.getHomeSectionNum()
    # 총 홈 섹션 개수
    if ch.hasHomeVideoPlayer() == True:
        totalSectionNum = ch.getHomeSectionNum() + 1
    else:
        totalSectionNum = ch.getHomeSectionNum()
    recommendChannel = [href for href in ch.getRecommendChannel()]
    # 동영상 개수
    #videoNum = ch.getVideoNum()
    # 재생목록 개수
    playlistNum = ch.getPlaylistsNum()
    # 토론탭 댓글 개수
    discussionReviewNum = ch.getDiscussionReviewNum()
    # 커뮤니티 포스팅 수
    communityPostNum = ch.getCommunityPostNum()
    # TODO: 데이터 일부만 불러오는 문제 해결필요. 보류

    # 동영상 탭 HTML 소스 가져오기
    videoNum = ch.getVideoTabHTML()
    '''
    # 동영상 탭 동영상 메타데이터 가져오기
    # videoListData = [data for data in ch.getVideoTabData()] #
    '''
    # TODO: 각 동영상 url 접속해서 데이터를 가져오기에는 시간이 너무 오래걸림. 추후 고찰
    for i in range(len(videoListData)):
        ch.moveToVideo(videoListData[i]['URL'])

    # 가져온 데이터 저장
    collection.update({'_id': selectOne['_id']}, {'$set':
        {
            'ChannelTitle': channelTitle,
            'Subscriber': channelSubscriberNum,
            'HomeTab':
                {
                    'VideoPlayer': homeVideoPlayer,
                    'SectionNum': homeSectionNum,
                    'TotalSectionNum': totalSectionNum,
                    'RecommendChannel': recommendChannel
                },
            'VideoTab':
                {
                    'VideoNum': videoNum
                    # TODO: 데이터 일부만 불러오는 문제해결 필요. 보류
                    # 'VideoData': videoListData
                },
            'PlaylistTab':
                {
                    'PlaylistNum': playlistNum
                },
            'DiscussionTab':
                {
                    'ReviewNum': discussionReviewNum
                },
            'CommunityTab':
                {
                    'PostNum': communityPostNum
                }
        }
    })
    '''
del ch
selectAll.close()
getSpendTime(start)
"""






