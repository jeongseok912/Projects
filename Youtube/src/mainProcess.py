# created by jeongseok
# jeongseok912@gmail.com
# 2018.07.29
import time
import pymongo
import socialerus as sr
import channel

def getSpendTime(start):
    end = time.clock()
    spendTime_sec = int(end - start)
    if spendTime_sec < 60:
        print('경과 시간 : ' + str(spendTime_sec) + '초')
    elif spendTime_sec >= 60:
        print('경과 시간 : ' + str(int(spendTime_sec/60)) + '분 ' + str(int(spendTime_sec%60)) + '초')
    elif spendTime_sec >= 3600:
        print('경과 시간 : ' + str(int(spendTime_sec/3600)) + '시간 ' + str(int((spendTime_sec%3600)/60)) + '분 ' + str(int((spendTime_sec%3600)%60)) + '초')

# 몽고DB connection
conn = pymongo.MongoClient('localhost', 27017)
db = conn.get_database('youtube')
collection = db.get_collection('channel')

# 소셜러스 데이터 트리거
# TODO: 배열 리턴 -> 제너레이터로 변경
sr.enableGetSocialerusData(True)

'''
print('Distinct : ' + str(len(collection.distinct('CID'))))

# 중복 검사
point1 = time.clock()
for compare in collection.find({}, {'CID':1}, no_cursor_timeout=True):
    if collection.find({'CID': compare['CID']}).count() > 1:
        for dup in collection.find({'CID': compare['CID']}):
            print(dup)
getSpendTime(point1)
'''

# 리스트 전처리
## 국내 유튜버 선별
loc = channel.Channel()
for doc in collection.find({}, {'CID':1}, no_cursor_timeout=True):
    loc.setChannelHomeURL(doc['CID'])
    collection.update({'_id': doc['_id']}, {'$set':
        {
            'Loc': loc.getLocation()
        }
    })
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






