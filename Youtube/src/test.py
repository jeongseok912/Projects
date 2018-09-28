import channel
import pymongo
from myutil import myError

# 몽고DB connection
conn = pymongo.MongoClient('localhost', 27017)
db = conn.get_database('youtube')
collection = db.get_collection('channel')


cursor = collection.find({'CID': 'UCAAyQrLDrcK0h1Ll3g8lURw'})
#cursor = collection.find({'CID': 'UCpTBYRfxcC5bNYRMEA3oiKQ'}) # DailyDose




ch = channel.Channel()

for doc in cursor:
    # 데이터 가져오기
    # ch.setChannelHomeURL('UC2ShoBD_1svSHQhDsJUHnfw')
    ch.setChannelHomeURL(doc['CID'])
    print('channel_id: ' + ch.channel_id)

    try:
        ch.getAboutTabSource()
    except myError as m:
        print("111")
        print(m)
    channel_title = ch.channel_title
    subs_num = ch.subscriber_num
    location = ch.location
    print('channel_title: ' + channel_title)
    print('subs_num: ' + str(subs_num))
    print('desc_size: ' + str(ch.desc_size,))
    print('desc: ' + ch.desc)
    print('location: ' + location)
    print('link_cnt: ' + str(ch.link_cnt))
    print('Instagram: ' + str(ch.instagram))
    print('Facebook: ' + str(ch.facebook))
    print('Google+: ' + str(ch.googleplus))
    print('NaverCafe: ' + str(ch.naver_cafe))
    print('NaverBlog: ' + str(ch.naver_blog))
    print('Tistory: ' + str(ch.tistory))
    print('Afreeca: ' + str(ch.afreeca))
    print('Youtube: ' + str(ch.youtube))
    print('Tumblur: ' + str(ch.tumblur))
    print('Others: ' + str(ch.others))
    print('JoinDate: ' +  ch.join_date)
    print('TotalViewCount: ' + str(ch.total_view_cnt))

    ch.getHomeSource()
    print('main_video_enable: ' + str(ch.main_video_enable))
    print('section_cnt: ' + str(ch.section_cnt))
    recommend_ch = [reco for reco in ch.getRecommendChannel()]
    print(str(recommend_ch))
    '''
    ch.getVideoTabSource()
    print('video_cnt: ' + str(ch.video_cnt))
    print({'VideoData': [a for a in ch.getVideoData()]})
    '''
    ch.getVideoCount()
    print('Search browser video cnt:' + str(ch.video_cnt))

    ch.getPlaylistsTabSource()
    print('playlist_cnt: ' + str(ch.playlists_cnt))

    ch.getDiscussionTabSource()
    print('discussion_enable: ' + str(ch.discussionTab_enable))
    print('discussion_cnt: ' + str(ch.discussion_cnt))

    ch.getCommunityTabSource()
    print('community_enable: ' + str(ch.communityTab_enable))
    print('post_cnt: ' + str(ch.post_cnt))
