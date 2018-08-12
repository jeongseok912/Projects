import channel
import pymongo

# 몽고DB connection
conn = pymongo.MongoClient('localhost', 27017)
db = conn.get_database('youtube2')
collection = db.get_collection('channel')

cursor = collection.find({'CID': 'UCSLbd-2R06iv0VtChxERhDA'}) # IT's okay 잇츠 오케이
# cursor = collection.find({'CID': 'UCbIjPWkBCUNn-wC_jui2tfA'})  # 02 fa
# cursor = collection.find({'CID': 'UCKqx9r4mrFglauNBJc1L_eg'})  # [토이푸딩] ToyPudding TV
# cursor = collection.find({'CID': 'UCEGJpYOKAD4PQuNIoImyReQ'}) # KwonHee

ch = channel.Channel()
for doc in cursor:
    # 데이터 가져오기
    ch.setChannelHomeURL(doc['CID'])

    ch.getAboutTabSource()  # set channel_title, subscriber_num, location
    channel_title = ch.channel_title
    subs_num = ch.subscriber_num
    location = ch.location
    #print('channel_title: ' + channel_title)
    #print('subs_num: ' + str(subs_num))
    #print('location: ' + location)
    '''
    ch.getHomeSource()
    #print('main_video_enable: ' + str(ch.main_video_enable))
    #print('section_cnt: ' + str(ch.section_cnt))
    recommend_ch = [reco for reco in ch.getRecommendChannel()]
    print(str(recommend_ch))
    
    ch.getVideoTabSource()
    print('video_cnt: ' + str(ch.video_cnt))
    print({'VideoData': [a for a in ch.getVideoData()]})

    ch.getVideoCount()
    print('Search browser video cnt:' + str(ch.video_cnt))
    '''
    ch.getPlaylistsTabSource()
    print('playlist_cnt: ' + str(ch.playlists_cnt))

    ch.getDiscussionTabSource()
    print('discussion_enable: ' + str(ch.discussionTab_enable))
    print('discussion_cnt: ' + str(ch.discussion_cnt))

    ch.getCommunityTabSource()
    print('community_enable: ' + str(ch.communityTab_enable))
    print('post_cnt: ' + str(ch.post_cnt))

