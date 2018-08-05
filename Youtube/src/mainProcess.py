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
i = 1
ch = channel.Channel()
start = time.clock()
for selectOne in selectAll:
    print('-----------------------')
    ch.setChannelHomeURL(selectOne['CID'])
    ch.popupChannelHome()
    print('###' + ch.getChannelTitle() + '###')
    # totalSectionNum
    if ch.hasHomeVideoPlayer() == True:
        totalSectionNum = ch.getHomeSectionNum() + 1
    else:
        totalSectionNum = ch.getHomeSectionNum()

    if ch.getChannelTitle() == 'PONY Syndrome':
        print(ch.getVideoData())

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
                }

        }
    })
    '''
                   'VideoTab':
                       {
                           'videoNum': ch.getVideoNum()
                           'video': [href for href in ch.getVideoData()]
                       }
                   '''

    #collectionName = 'ch' + str(i)
    #chCollection = db.get_collection(collectionName)
    #chCollection.insert_one({'a':1})
    i += 1
#del ch
selectAll.close()
end = time.clock()
getSpendTime(start, end)







