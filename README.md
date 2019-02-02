# 1. Youtube  
유튜브 채널 분석 프로젝트  
* `/src/` : python 크롤링 소스 경로    
  * `channel.py` : 유튜브 채널들의 정보를 가져오는 클래스가 담긴 모듈  
  * `mainProcess.py` : 국내 유튜브 채널 랭킹 사이트 소셜러스 https://kr.socialerus.com/ranking 에서 채널리스트를 가져오고 리스트에 있는 유튜브 채널들의 데이터를 가져와 MongoDB에 저장하는 메인 모듈   
  * `myutil.py` : 경고문 색 정의, 경과 시간 출력, 직접 정의한 에러 출력을 위해 정의한 모듈  
  * `socialerus.py` : 소셜러스에서 채널리스트를 가져오는 모듈  
  * `test.py` : 채널 데이터를 잘 가져오는지 확인하기 위해 한 채널의 정보만 가져올 수 있는 모듈   
* `/analysis/` : 수집한 정보로 분석한 결과를 담은 경로  
  * `ch.json` : MongoDB에 저장된 데이터를 전부 Export한 결과물  
  * `국내 유튜브 채널 데이터 분석을 통한 신규 채널 운영 전략.pptx` : 데이터 수집, 가공, 분석 등의 과정을 정리하고, 분석에 대한 고찰을 담은 PPT

# 2. Kaggle
## 2.1. `/House Prices/`
House Prices: Advanced Regression Techniques 컴피티션 관련 소스 및 자료 경로
* `Strong Regression_submission_rev1.ipynb`
  * 사이킷런의 기본적인 회귀 모델 `LinearRegression`과 정규화 회귀 모델 `Ridge`, `Lasso`, `ElasticNet`만 사용한 단순한 회귀 진행
    * SVR 모델, Tree 모델, ensemble 모델 등을 이용한 회귀 추가 예정
    * grid search와 같은 탐색 모델을 통해 세부 튜닝 예정
  * missing values를 처리하는 변환기와 feature engineering하는 변환기 제작
    * 변환기를 통합하고 파이프라인 처리를 할 수 있도록 refactoring 필요
## 2.2. `/Titanic/`
Titanic: Machine Learning from Disaster 컴피티션 관련 소스 및 자료 경로
* `Titanic_submission_rev1.ipynb`
  * ensemble model과 2layer stacking model을 이용한 분류 진행
    * 더 다양한 모델 시도 및 세부 튜닝 예정
  * missing values 처리 변환기와 feature engineering 변환기 pipeline 제작
    * 모델링도 포함하는 pipeline 구축 예정
