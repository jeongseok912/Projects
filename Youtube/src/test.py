import channel
import pymongo
from myutil import myError

# 몽고DB connection
conn = pymongo.MongoClient('localhost', 27017)
db = conn.get_database('youtube')
collection = db.get_collection('channel')

# cursor = collection.find({'CID': 'UCSLbd-2R06iv0VtChxERhDA'}) # IT's okay 잇츠 오케이
# cursor = collection.find({'CID': 'UCbIjPWkBCUNn-wC_jui2tfA'})  # 02 fa
# cursor = collection.find({'CID': 'UCKqx9r4mrFglauNBJc1L_eg'})  # [토이푸딩] ToyPudding TV
# cursor = collection.find({'CID': 'UCEGJpYOKAD4PQuNIoImyReQ'}) # KwonHee
# cursor = collection.find({'CID': 'UCNth1SaCfdjPg9WFQYtqAfw'}) # 팀유통기한 커뮤니티(o), post(~), 토론(x)
# cursor = collection.find({'CID': 'UCzjEp3u8RMkOJwpc3RzxmWg'}) # 양띵TV콩콩 커뮤니티(o), post(0), 토론(x)
# cursor = collection.find({'CID': 'UCixfddJJ4VkzIa8tMnSWPFQ'}) # Kanna칸나 커뮤니티(x), 토론(o), 댓글(0)
# cursor = collection.find({'CID': 'UCw8ZhLPdQ0u_Y-TLKd61hGA'}) # 1MILLION Dance Studio

# cursor = collection.find({'CID': 'UCPJmHR4CG_lRuVwKCo0kjjg'}) # KPOP COVER STREET KARAOKE 창현거리노래방 쏭카페
# cursor = collection.find({'CID': ''}) # CJ7
# cursor = collection.find({'CID': 'UCKG1FQU_Iz5vYvO7_w10_gg'}) # 음악 연속듣기
# cursor = collection.find({'CID': 'UCvohsyXlehjoLHWuffue5IA'}) # BHC치킨
# cursor = collection.find({'CID': 'UCmcOMiiFPkBTx3UK2yfUekQ'}) # #nebyvlogs
# cursor = collection.find({'CID': 'UCwVw_Ha7k-kxf1I1zSshc-w'}) # 서지혜

# cursor = collection.find({'CID': 'UCfTswP_uNy_h86pUjCU410A'}) # HANA 김하나
# cursor = collection.find({'CID': 'UCmcOMiiFPkBTx3UK2yfUekQ'}) # #nebyvlogs
# cursor = collection.find({'CID': 'UCfDWSYJhJfvZm-abHS1lH6Q'}) # Jon Park Vlogs
# cursor = collection.find({'CID': 'UClqMRYeJyY4_qhcY15okzmQ?'}) # 감자펀치
# cursor = collection.find({'CID': 'UCR43XXEm8WgV31MIf6CcDVg'})
cursor = collection.find({'CID': 'UCiiWTch5kweyoXsvTv16bGQ'}) # 삭제된 채널
cursor = collection.find({'CID': 'UCqWEkbikkSFnrgGVSEHX_Nw'})


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

