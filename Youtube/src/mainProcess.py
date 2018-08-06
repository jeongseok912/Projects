# created by jeongseok
# jeongseok912@gmail.com
# 2018.07.29
import time
import pymongo
import socialerus as sr
import channel

def getSpendTime(start, end):
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
sr.enableGetSocialerusData(False)

'''
print('Distinct : ' + str(len(collection.distinct('CID'))))

# 중복 검사
point1 = time.clock()
for compare in collection.find({}, {'CID':1}, no_cursor_timeout=True):
    if collection.find({'CID': compare['CID']}).count() > 1:
        for dup in collection.find({'CID': compare['CID']}):
            print(dup)
point2 = time.clock()
getSpendTime(point1, point2)
'''

# CID로 채널 데이터 가져와서 저장하기
print('\n### 채널 데이터 저장하기 ###')
selectAll = collection.find({'CID': 'UCT-_4GqC-yLY1xtTHhwY0hA'}, {'CID':1}, no_cursor_timeout=True) # return type: cursor
# selectAll = collection.find({}, {'CID':1}, no_cursor_timeout=True) # return type: cursor

ch = channel.Channel()
start = time.clock()
#sum = 0
for selectOne in selectAll:
    print('-----------------------')
    # 채널 설정
    ch.setChannelHomeURL(selectOne['CID'])
    # 채널 띄우기
    ch.popupChannelHome()
    print('###' + ch.getChannelTitle() + '###')
    # 홈 섹션 개수
    if ch.hasHomeVideoPlayer() == True:
        totalSectionNum = ch.getHomeSectionNum() + 1
    else:
        totalSectionNum = ch.getHomeSectionNum()
    # 동영상탭에서 데이터 가져오기
    point3 = time.clock()
    ch.getVideoTabHTML()
    videoListData = [data for data in ch.getVideoListData()]
    '''
    for i in range(len(videoListData)):
        ch.moveToVideo(videoListData[i]['URL'])
    '''
    point4 = time.clock()
    getSpendTime(point3, point4)

    # 가져온 데이터 저장
    collection.update({'_id': selectOne['_id']}, {'$set':
        {
            'ChannelTitle': ch.getChannelTitle(),
            'Subscriber': ch.getSubscriberNum(),
            'HomeTab':
                {
                    'VideoPlayer': ch.hasHomeVideoPlayer(),
                    'SectionNum': ch.getHomeSectionNum(),
                    'TotalSectionNum': totalSectionNum,
                    'recommendChannel': [href for href in ch.getRecommendChannel()]
                },
            'VideoTab':
                {
                    'VideoNum': ch.getVideoNum(),
                    'VideoData': videoListData
                }
        }
    })
    '''
    print(ch.getChannelTitle() + ': ' + str(ch.getVideoNum()))
    sum += ch.getVideoNum()
    print('Total : ' + str(sum))
    '''
'''
print(sum)
print(sum/len(selectAll))
'''

del ch
selectAll.close()
end = time.clock()
getSpendTime(start, end)







