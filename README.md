# 1. Youtube  
유튜브 채널 분석 프로젝트  
* `/src/` : python 크롤링 소스 경로    
  * `channel.py` : 유튜브 채널들의 정보를 가져오는 클래스가 담긴 모듈  
  * `mainProcess.py` : 국내 유튜브 채널 랭킹 사이트 소셜러스 https://kr.socialerus.com/ranking 에서 채널리스트를 가져오고 리스트에 있는 유튜브 채널들의 데이터를 가져와 MongoDB에 저장하는 메인 모듈   
  * `myutil.py` : 경고문 색, 경과 시간 확인, 직접 정의한 에러 출력을 위해 정의한 모듈  
  * `socialerus.py` : 국내 유튜브 채널 랭킹 사이트 소셜러스 https://kr.socialerus.com/ranking/ 에서 채널리스트를 가져오는 모듈  
  * `test.py` : 채널 데이터를 잘 가져오는지 확인하기 위해 한 채널의 정보만 가져올 수 있는 모듈   
* `/analysis/` : 수집한 정보로 분석한 결과를 담은 경로  
  * `ch.json` : MongoDB에 저장된 데이터를 전부 Export한 결과물  
  * `국내 유튜브 채널 데이터 분석을 통한 신규 채널 운영 전략.pptx` : 데이터 수집, 가공, 분석 등의 과정을 정리하고, 분석에 대한 고찰을 담은 PPT
