### FRONTEND 개발환경 세팅 하기    
---
   
node.js와 vue cli가 설치되어 있어야 합니다.   
node.js는 최대한 최신 버전 (nodeJs 16.13 LTS 추천) 만약 16버전 미만일 경우 환경 설정 중 오류가 없도록 재설치를 권장합니다.   

<br />   

[ >> nodeJs 설치 링크 << ](https://nodejs.org/ko/download/releases/)   


<br />   

<br />   


<b>[vue가 설치되어 있지 않은 경우]</b>   

``` ruby 
#open terminal or powershell   
npm install -g @vue/cli
npm install -g @vue/cli-service
```

<br />   


<br />   


#### 환경 세팅 (with npm)


<br />   


```ruby   
# cd COUDeploy/frontend

# !주의!
# Windows에서는 export 대신 set 명령어를 사용할 것

# Warnning은 일단 무시한다. 
# 모듈 업그레이드(업데이트) 잘못하면 build 과정에서 Error 남
> npm install

# package upgrade를 하지 않는이상 초기 딱 한 번만 실행해도 됨.
> export NODE_ENV=development 

> npm run build:dll 

# Your-backend의 경우 로컬호스트 웹에서 테스트를 할려면 localhost로
# ex) export TARGET=http://localhost
> export TARGET=http://Your-backend
```   

<br />   


#### 실시간 반영 개발하기
```ruby   
# cd COUDeploy/frontend
> npm run dev 

```   

위 명령어를 치면 webpack의 middleware(webpack-dev-middleware)가 실행되고, hot-reload로 실시간 반영이 됩니다 별도의 웹서버 구축 없이 프로세스가 실행됩니다. 해당 포트는 8080포트(http://localhost:8080)이며, 80포트와는 다른 경로입니다.

만약 실행중인 8080포트로 연결 된 프로세스를 종료하고싶다면, 실행중인 터미널에서 ctrl + C 키를 눌러주시면 됩니다.
   
<br />   


#### 빌드하기
```ruby   
# cd COUDeploy/frontend
> npm run build 

```   

위에서 개발이 완료되면 실제 배포를 하기 위해서는 build를 해야합니다. build를 하면 frontend 디렉토리 안에 dist라는 폴더가 생성 될 것입니다.

   
<br />   


#### frontend 볼륨 마운트(빌드한 파일을 적용시키고 싶을 때)   

<br />   

위 과정만으로는 아직 빌드한 dist폴더가 docker에 반영된 것은 아닙니다.
docker 컨테이너가 아닌 로컬 시스템의 frontend 의 빌드 폴더(dist)를 바인드하기 위해서는 <b>docker-compose.yml</b> 파일을 부분적으로 수정해야합니다.

```
  ...

  oj-backend:
    image: kdonggyun97/cou-coding-platform-dev
    container_name: cou-coding-platform-dev
    restart: always
    depends_on:
      - oj-redis
      - oj-postgres
      - judge-server
    volumes:
      - ./data/backend:/data
      # - ./frontend/dist:/app/dist
    environment:
      - POSTGRES_DB=onlinejudge
      - POSTGRES_USER=onlinejudge
      - POSTGRES_PASSWORD=onlinejudge
      - JUDGE_SERVER_TOKEN=CHANGE_THIS
      # - FORCE_HTTPS=1
      - STATIC_CDN_HOST=/
    ports:
      - "0.0.0.0:80:8000"
      - "0.0.0.0:443:1443"

```

여기서 <b> - ./frontend/dist:/app/dist </b> 주석을 해제해줍니다.

그 다음 다음과 같이 명령어를 입력합니다.


```ruby
# cd COUDeploy
> docker-compose up -d
```

<br />   


위 과정이 끝나고 http://localhost:80 에 접속하여 페이지를 새로고침 할 경우 빌드 된 dist폴더가 반영이 되는 것을 확인 하실 수 있습니다.


<br />
<br />
<br />

----





## Frontend Hierarchy   
프론트엔드 계층    

```shell
 #front/src/pages/admin/views
 └── contest 
     │── Contet.vue
     └── ContestList.vue
 └── general
     │── Announcement.vue
     │── Conf.vue
     │── Dashboard.vue
     │── JudgeServer.vue
     │── Login.vue
     │── PruneTestCase.vue
     └── User.vue
 │── problem
     │── AddPublicProblem.vue
     │── ImportAndExport.vue
     │── Problem.vue 
     └── ProblemList.vue
 
 
 #frontend/src/pages/oj/views
 │── article 
     │── ArticleDetails.vue    # (/article/:articleID/) : 게시글 고유 ID에 대한 상세 글 페이지뷰 
     │── ArticleList.vue      # (/article-list?query) : 게시글 리스트
     │── CreateArticle.vue      # (/create-article) : 게시글 작성 페이지
     └── Notification.vue      # (notification-list) : 알림 리스트 페이지
 │── contest 
     │── ContestDetail.vue    #(/contest/:contestID/) : 해당 ID 대회 문제 
     │── ContestList.vue      #(/contest) : 대회 문제 리스트
     └── children
         │── ACMContestRank.vue 
         │── ACMHelper.vue
         │── ContestProblemList.vue
         │── ContestRank.vue
         └── OIContestRank.vue
 │── general
     │── 404.vue        # 잘못된 경로로 접근시 404 페이지
     │── Anncouncement.vue  # 공지사항 페이지
     │── AnncouncementList.vue  # 공지사항 리스트 페이지
     └── Home.vue       # 홈
 │── help
     │── About.vue      # (/about) : 자주 묻는 질문 페이지 (현재 안씀; FAQ로 통합)
     │── Languages.vue      # (/languages) : 언어별 도움말 페이지
     └── FAQ.vue        # (/faq) : Frequently Asked Questions
 │── preHome
     └── Start_Login.vue        # 로그인 전 pre 페이지
 │── problem
     │── Problem.vue       # (/problem/:problemID) : 문제 상세 페이지
     │── ProblemCategory.vue       # (/problem?query) : 카테고리에 묶인 문제 리스트
     └── ProblemList.vue   # (/problem) : 문제 리스트
 │── rank
     │── ACMRank.vue       #(/acm-rank) : ACM Ranklist 페이지
     └── OIRank.vue        #(/oi-rank) : OI Ranklist 페이지
 └── setting
     └── children # setting 사이드바 components (default-setting, profile-setting, account-setting, security-setting)
         │── AccountSetting.vue
         │── ProfileSetting.vue
         └── SecuritySetting.vue 
     └── Settings.vue      #(/setting) : 설정 페이지
 │── submission
     │── SubmissionDetails.vue      #(status/:id/) : 해당id문제 제출 상태 페이지
     └── SubmissionList.vue         #(/status) : 모든 문제의 제출 상태 페이지
 └── user
     │── ApplyResetPassword.vue     #(/apply-reset-password) : 비밀번호 찾기 페이지
     │── ApplyVerifyEmail.vue       # 이메일 인증 페이지
     │── Login.vue                  # 로그인 함수 (페이지 뷰는 없음)
     │── Logout.vue                 # 로그아웃 함수 (페이지 뷰는 없음)
     │── Register.vue               # 회원가입
     │── ResetPassword.vue          #(/reset-password/:token) : 비밀번호 재설정
     └── UserHome.vue               #(/user-home) : 사용자 계정 정보
 ```  
 
<br />   
