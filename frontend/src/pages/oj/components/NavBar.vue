<template>
  <div id="header" >
    <!-- <transition name="fadenav"> -->
    <Menu v-if="screenWidth > 900" :style="{visibility: screenWidth > 900 ? 'visible' : 'hidden'}" theme="light" :mode="hMode" @on-select="handleRoute" :active-name="activeMenu" class="oj-menu">
      <Menu-item class="home_bar" name="/" ><router-link to="/">춘천재래시장</router-link></Menu-item>
      <!-- <Menu-item class="bar_list" name="/problem">
        <router-link to="/problem">문제</router-link>
      </Menu-item> -->
      <Menu-item class="bar_list" name="/market">
        <router-link to="/contest">재래시장</router-link>
      </Menu-item>
      <Menu-item class="bar_list" name="/announcement-list">
        <router-link to="/contest">공지사항</router-link>
      </Menu-item>
      <Menu-item class="bar_list" name="/article-list">
        <router-link to="/article-list?boardtype=1">자유게시판</router-link>
      </Menu-item>
      <!-- <Submenu class="bar_list" name="/community" trigger="click">
        <template slot="title">
          커뮤니티
        </template> -->
          <!-- <MenuItem name="/article-list?boardtype=0"><router-link to="/article-list?boardtype=0">전체 게시판</router-link></MenuItem>
          <MenuItem name="/article-list?boardtype=1"><router-link to="/article-list?boardtype=1">자유 게시판</router-link></MenuItem> -->
          <!-- <MenuItem name="/article-list?boardtype=2"><router-link to="/article-list?boardtype=2">질문 게시판</router-link></MenuItem> -->
          <!-- <MenuItem name="/article-list?boardtype=3"><router-link to="/article-list?boardtype=3">요청 게시판</router-link></MenuItem>
      </Submenu>
      <Menu-item class="bar_list" :class="{'open': navOpen === true}" name="/status">
      <Icon type="ios-pulse-strong">
       <router-link to="/status">{{$t('m.NavStatus')}}</router-link>
      </Menu-item> -->
      <template v-if="!isAuthenticated">
        <div class="login_menu">
          <Button type="text"
                  ref="loginBtn"
                  shape="circle"
                  @click="goLogin"
                  style="line-height:50%;">
                  <p>{{$t('m.Login')}}</p>
          </Button>
        </div>
      </template>
      <template v-else>
        <div class="right_menu">
          <!-- 알림 출력 버튼 -->
          <div class="alarm">
            <Badge dot v-if="init_notification_count > 0" class="alarm-box">
              <Button type="text" class="bell bells" size="large" @click="changeNoti" @mouseover.native="alarmHoverForActive" @mouseleave.native="alarmHoverForNoActive">
                <i v-bind:class="AlarmHoverActive" style="padding-bottom:5px; color:#fff"></i>
              </Button>
            </Badge>
            
            <Badge v-else>
              <Button type="text" class="bell bells" size="large" @click="changeNoti" @mouseover.native="alarmHoverForActive" @mouseleave.native="alarmHoverForNoActive">
                <i v-bind:class="AlarmHoverActive" style="padding-bottom:5px"></i>
              </Button>
            </Badge>
            <div style="clear:both"></div>
            <div v-if="visibleDraw" class="notifications-tab" v-click-outside="closeNoti">
              <ul class="notifications-table" v-bind:style="[vNotifications.length == 0 ?{'overflow-y' : 'visible'}:{'overflow-y' : 'scroll'}]">
                <p class="no-notifications" v-if="vNotifications.length == 0">알람이 없습니다.</p>
                <li v-else v-for="(item, index) in vNotifications" :key="index">
                  <ul v-bind:style="[!item.is_read ?{'background-color' : '#e0dafc4d'}:{}]" class="notifications-entry"  @click="redirectToArticle(item)">
                    <div>
                      <div>
                        <div>
                          <div id="icon-container">
                            <Icon v-if="item.notificationtype === 'COMMENT'" class="icon" size=12 type="ios-chatboxes" />
                            <Icon v-if="item.notificationtype === 'LIKE'" class="icon" size=12 type="md-heart" />
                          </div>
                          <div id="notification-type">
                              <li>{{ item.notificationtype }}</li>
                          </div>
                        </div>
                        <div id="notification-date">
                          <li> {{ convertDate(item.create_time) }}</li>
                        </div>
                      </div>
                      <div>
                        <div id="notification-content">
                          <li> {{item.content}} </li>
                        </div>
                      </div>
                    </div>
                  </ul>
                  <hr v-if="index < vNotifications.length - 1">
                </li>
              </ul>
              <div id="all-notifications">
                <hr>
                <a @click="goAllNotificationList">알림 전체 보기</a>
              </div>
            </div>
          </div>
            <!--사용자 아이디 출력-->
          <div @click="viewModal" @blur="visibleAccount = false" class="account_tab"> <!--/setting/mypage-->
              <i v-if="getAvatar" class="small-avatar-container">
                <img :src="profile.avatar"/>
              </i>
              <Icon v-else type="md-contact" size="30" color="#fff"/>
            <span class="username">{{ user.username }}</span>
          </div>
          <div style="clear:both"></div>
          <transition name="fade">
            <div v-if="visibleAccount" class="account_modal" v-click-outside="closeModal">
              <div class="profile">
                <div class="photo">
                  <div v-if="getAvatar" class="avatar-container">
                    <img :src="profile.avatar"/>
                  </div>
                  <Icon v-else type="md-contact" size="100" color="#5030E5"/>
                </div>
                <div class="name">{{ user.username }}</div>
                <div class="email">{{ user.email || 'Unlocked Account' }}</div>
              </div>
              <!-- <div class="mypage_btn" @click="goMySettingPage">계정관리</div> -->
              <div class="line"></div>
              <div class="logout_btn" @click="goLogOut">로그아웃</div>
            </div>
          </transition>
        </div>
      </template>
    </Menu>


    <!-- vertical navigation-bar -->
    <Menu :style="{visibility: screenWidth <= 900 ? 'visible' : 'hidden'}" theme="light" width="100%" :mode="vMode" @on-select="handleRoute" :active-name="activeMenu" class="oj-menu">
      <Menu-item class="home_bar" name="/ff" >
        <div class="logo-name" @click="handleRoute('/')">춘천재래시장</div>
      </Menu-item>
      <!-- <Menu-item class="bar_list" :class="{'open': navOpen === true}" name="/problem">
        문제
      </Menu-item> -->
      <Menu-item class="bar_list" :class="{'open': navOpen === true}" name="/market">
        대회
      </Menu-item>
      <Submenu class="bar_list" :class="{'open': navOpen === true}" name="/info">
        <template slot="title">
          정보
        </template>
          <MenuItem name="/announcement-list">공지사항</MenuItem>
          <MenuItem name="/help">오시는 길</MenuItem>
          <!-- <MenuItem name="/languages">언어별 도움말</MenuItem>
          <MenuItem name="/acm-rank">사용자 순위</MenuItem> -->
      </Submenu>
      <Submenu class="bar_list" :class="{'open': navOpen === true}" name="/community">
        <template slot="title">
          커뮤니티
        </template>
          <!-- <MenuItem name="/article-list?boardtype=0">전체 게시판</MenuItem> -->
          <MenuItem name="/article-list?boardtype=1">자유 게시판</MenuItem>
          <MenuItem name="/article-list?boardtype=2">질문 게시판</MenuItem>
          <!-- <MenuItem name="/article-list?boardtype=3">요청 게시판</MenuItem> -->
      </Submenu>
      <Menu-item class="bar_list" :class="{'open': navOpen === true}" name="/status">
        <!-- <Icon type="ios-pulse-strong"></Icon> -->
        {{$t('m.NavStatus')}}
      </Menu-item>
      <Menu-item v-if="navOpen && !isAuthenticated" class="bar_list" :class="{'open': navOpen === true}" name="/login">
        로그인
      </Menu-item>
      <!-- <Menu-item v-if="navOpen && isAuthenticated" class="bar_list" :class="{'open': navOpen === true}" name="/setting/mypage">
        마이페이지
      </Menu-item> -->
      <Menu-item v-if="navOpen && isAuthenticated" class="bar_list" :class="{'open': navOpen === true}" name="/logout">
        로그아웃
      </Menu-item>
    </Menu>
    <!-- </transition> -->
    <button  v-show="screenWidth <= 900" class="navbar_toggle-btn" @click="navToggle">
      <Icon type="md-menu" />
    </button>
    
    <Modal v-model="modalVisible" :width="430">
      <div slot="header" class="modal-title">인증이 필요해요!</div>
      <component :is="modalStatus.mode" v-if="modalVisible"></component>
      <div slot="footer" style="display: none"></div>
    </Modal>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import GuardMessage from '@oj/views/user/GuardMessage.vue'
  import api from '@oj/api'
  import time from '@/utils/time'
  import vClickOutside from 'v-click-outside'
  export default {
    directives: {
      clickOutside: vClickOutside.directive
    },
    components: {
      GuardMessage
    },
    data () {
      return {
        screenWidth: 0,
        navOpen: false,
        hMode: 'horizontal',
        vMode: 'vertical',
        alarmHoverActive: false,
        init_notification_count: 0,
        emptyChar: '알람이 존재하지 않습니다.',
        showHeaderandborder: false,
        dishovering: true,
        visibleDraw: false,
        visibleAccount: false,
        vNotifications: [],
        colums: [
          {
            title: 'noti',
            render: (h, params) => {
              return h('div', {
                style: {
                }
              }, [
                h('div', {
                  style: {
                    'float': 'left',
                    'padding-top': '5px'
                  }
                }, [
                  h('a', {
                    style: {
                      'font-size': '1.2em',
                      'font-weight': 'bold',
                      'line-height': '1.3em'
                    },
                    on: { // 확인 클릭 시 알림이 발생한 곳으로 이동
                      click: () => {
                        api.checkNotification(params.row.id).then(res => {
                          window.open(params.row.url)
                        })
                      }
                    }
                  }, params.row.notificationtype),
                  h('p', {
                    style: {
                      'padding-bottom': '5px'
                    }
                  }, params.row.content)
                ]),
                h('div', {
                  style: {
                    'margin-top': '10px',
                    'float': 'right',
                    'max-width': '55px'
                  }
                }, [
                  h('Button', {
                    props: {
                      'type': 'error',
                      'size': 'small',
                      'icon': 'ios-trash-outline'
                    },
                    on: {
                      click: () => {
                        this.delete = true
                        this.close(params.row.id)
                        this.vGetNotifications()
                      }
                    }
                  })
                ])
              ]
              )
            }
          }
        ],
        notification_checked: false, // true - 현재 알림창 열림 / false - 현재 알림창 닫힘
        notifications: [], // 알림 목록
        delete: false // true - 알림창 close 시 알림 삭제 / false - 알림창 close 시 알림 삭제 X
      }
    },
    mounted () {
      this.init()
    },
    created () {
      window.addEventListener('resize', this.handleResize)
      this.handleResize()
      this.getOnlyNotificationsListLength()
      setInterval(() => {
        this.getOnlyNotificationsListLength()
      }, 5000)
    },
    methods: {
      ...mapActions(['getProfile', 'changeModalStatus']),
      init () {
        this.getProfile()
      },
      handleRoute (route) {
        if (route === '/ff') {  // vertical-nav-bar 상단전체 클릭 방지용
          return
        }
        this.navOpen = false
        if (this.notification_checked) { // 변경될 때 마다 알림창을 닫음
          this.delete = false
          this.$Notice.destroy()
          this.notification_checked = false
        }
        if (route && route.indexOf('admin') < 0) {
          this.$router.push(route).catch(() => {}) // exception catch
        } else {
          window.open('/admin/')
        }
      },
      handleBtnClick () {
        this.changeModalStatus({
          visible: true,
          mode: 'GuardMessage'
        })
        this.handleRoute('GuardMessage')
      },
      goLogOut () {
        this.$router.push({path: '/logout'}).catch(() => {})
      },
      goMySettingPage () {
        this.$router.push({name: 'my-page'}).catch(() => {})
      },
      goLogin () {
        this.$router.push({path: '/login'}).catch(() => {})
      },
      getOnlyNotificationsListLength () {
        let li = []
        api.getReadNotification().then(res => { // 현재 접속한 유저의 알림을 전송 받음
          li = res.data.data
          if (li === undefined || li === null || li.length <= 0) {
            this.init_notification_count = 0
          } else {
            this.init_notification_count = li.length
          }
        }, () => {
          this.init_notification_count = 0
        })
      },
      changeNoti () {
        this.vGetNotifications()
        this.visibleDraw = !this.visibleDraw
      },
      viewModal () {
        this.visibleAccount = !this.visibleAccount
      },
      closeModal () {
        if (this.visibleAccount === true) {
          this.visibleAccount = false
        }
      },
      closeNoti () {
        if (this.visibleDraw === true) {
          this.visibleDraw = false
        }
      },
      convertDate (date) {
        return time.utcToLocal(date, 'YYYY-MM-DD HH:mm')
      },
      vGetNotifications () {
        api.getNotificationList().then(res => {
          this.vNotifications = res.data.data
          console.log(res.data.data)
          this.getOnlyNotificationsListLength()
        })
      },
      close (notificationid) {
        if (this.delete) {
          api.deleteNotification(notificationid).then(res => { // 알림 고유 ID를 전송해 알림 삭제
            this.getOnlyNotificationsListLength()
          })
        }
      },
      goAllNotificationList () {
        this.visibleDraw = false
        this.$router.push({
          path: '/notification-list'
        }).catch(() => {})
      },
      alarmHoverForActive () {
        this.alarmHoverActive = true
      },
      alarmHoverForNoActive () {
        this.alarmHoverActive = false
      },
      redirectToArticle (notification) {
        let noti = notification.url.split('/')
        let articleId = noti[noti.length - 1]
        if (!notification.is_read) this.init_notification_count -= 1
        api.checkNotification(notification.id).then(res => {
          if (notification.notificationtype === 'COMMENT') {
            this.$router.push({name: 'article-details', params: {articleID: articleId}, hash: this.getHashtag(notification)}).catch(() => {})
          } else {
            this.$router.push({name: 'article-details', params: {articleID: articleId}}).catch(() => {})
          }
        })
        this.visibleDraw = false
      },
      getHashtag (notification) {
        return '#comment' + notification.id
      },
      navToggle () {
        this.navOpen = !this.navOpen
      },
      closeNav () {
        if (this.navOpen === true) {
          this.navOpen = false
        }
      },
      handleResize (e) {
        this.screenWidth = window.innerWidth
      }
    },

    computed: {
      ...mapGetters(['website', 'modalStatus', 'user', 'isAuthenticated', 'isAdminRole', 'isVerifiedEmail', 'profile']),
      AlarmHoverActive () {
        if (this.alarmHoverActive) {
          return 'ivu-icon ivu-icon-ios-notifications'
        } else {
          return 'ivu-icon ivu-icon-ios-notifications-outline'
        }
      },
      activeMenu () {
        return '/' + this.$route.path.split('/')[1]
      },
      modalVisible: {
        get () {
          return this.modalStatus.visible
        },
        set (value) {
          this.changeModalStatus({visible: value})
        }
      },
      getAvatar () {
        return this.profile.avatar !== '/public/avatar/default.png'
      }
    },
    destroyed () {
      window.removeEventListener('resize', this.handleResize)
    },
    watch: {
      init_notification_count: function (newVal, oldVal) {
        this.init_notification_count = newVal
      },
      '$route' (to, from) {
        if (this.visibleAccount !== false) {
          this.visibleAccount = false
        }
        if (this.visibleDraw !== false) {
          this.visibleDraw = false
        }
      },
      'screenWidth' (newVal, oldVal) {
        this.screenWidth = newVal
        if (newVal > 900 && this.navOpen === true) {
          this.closeNav()
        }
      }
    }
  }
</script>
<style lang="less">
  .alarm-box {
    .ivu-badge-dot {
      top: 5px !important;
      right: 5px !important;
    }
  }
  .bells {
    &.ivu-btn:hover {
      border-color: #263A8C;
    }
    &.ivu-btn:focus {
      border-color: transparent;
      box-shadow: none;
    }
  }
</style>
<style lang="less" scoped>
@import '../../../styles/common.less';
@avatar-radius: 50%;
  #header {
    min-width: 300px;
    position: fixed;
    top: 0;
    left: 0;
    height: 60px;
    width: 100%;
    z-index: 985;
    background-color: #263A8C;
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);
    .oj-menu {
      //background: #404040;
      position: relative;
      background: #263A8C;
      z-index: 986;
    }
    .navbar_toggle-btn {
      position: absolute;
      background: transparent;
      border: none;
      right: 32px;
      top: 0;
      font-size: 24px;
      color: #F4815A;
      display: none;
      z-index: 988;
    }
    .logo {
      margin-left: 2%;
      margin-right: 2%;
      font-size: 20px;
      float: left;
      line-height: 60px;
    }
    .logo > span > a, .bar_list, a, .bar_list a {
      color: @white;
      font-weight: @weight-regular;
      transition: all 0.2s ease-in-out;
      &:hover {
        color: #F4815A;
        & a {
          color:#F4815A;
        }
      }
    }
    .home_bar, .home_bar a {
        color: #F4815A;
        font-size: @font-medium;
        font-weight: @weight-bold;
        //-webkit-text-stroke: 1.5px;
        .logo-name {
          width: fit-content;
          height: 32px;
          line-height: 32px;
          &:hover {
            cursor: pointer;
          }
        }
    }

    .bar_list {
      text-align: center;
    }
    .drop-menu {
      float: right;
      padding: 0 30px 0 30px;
      //margin-right: 50px;
      //position: fixed;
      right: 10px;
      //color: white;
      color: #404040;
      font-size: 18px;
      &-title {
        font-size: 20px;
      }
    }
    .btn-menu {
      display: block;
      position: fixed;
      font-size: 16px;
      float: right;
      margin-right: 10px;
    }
  }
  .modal {
    &-title {
      font-size: 18px;
      font-weight: 600;
    }
  }
  .alarm {
    line-height: 50%;
    float: right;
    margin-right: 10px;
    .bell {
      color: #F4815A;
      font-size: 1.5em;
    }
  }
  .login_menu {
    overflow:hidden;
    float: right;
    padding: 0 30px;
    // position: fixed;
    height: 60px;
    padding: 0 60px;
    button {
      border: 2px solid @light-gray;
      border-radius: 5px;
      height: 40px;
      padding: 20px;
      font-weight: @weight-bold;
      &:hover {
        box-shadow: 0 1px 5px 0 rgba(90, 82, 128, 0.31);
        color: #F4815A;
      }
    }
  }
  .right_menu {
    display: flex;
    align-items: center;
    justify-content: center;
    line-height: 50%;
    overflow:hidden;
    float: right;
    padding: 0px 30px;
    // position: fixed;
    height: 60px;
    margin-right: 5px;
    .account_tab {
      &:hover {
        cursor: pointer;
        border: 1.5px solid #F4815A;
      }
      float: right;
      line-height: 50%;
      height: 45px;

      color: @white;
      font-weight: 500;
      padding: 5px 7px 5px 5px;
      border-radius: @size-border-radius;
      -webkit-transition: all .2s ease-in;
      -moz-transition: all .2s ease-in;
      -ms-transition: all .2s ease-in;
      -o-transition: all .2s ease-in;
      transition: all .2s ease-in;
      span {
        -webkit-text-stroke: 0.5px;
      }
    }
    .account_modal {
      position: absolute;
      display:flex;
      flex-direction: column;
      justify-content: space-between;
      align-items: center;
      border-radius: @size-border-radius;
      padding: 24px;
      top: 60px;
      right: 20px;
      width: 300px;
      min-width: 250px;
      height: 340px;
      min-height: 300px;
      background-color: @white;
      color: @white;
      box-shadow: 2px 5px 20px 2px rgba(90, 82, 128, 0.31);

      .profile {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        align-items: center;
        height: 150px;
        .name {
          color: #F4815A;
          font-size: @font-medium;
          font-weight: @weight-semi-bold;
        }
        .email {
          color: @gray;
          font-size: @font-small;
          margin-top: 10px;
        }
      }
      .mypage_btn {
        border: 2px solid @gray;
        border-radius: 20px;
        width: 40%;
        padding: 12px;
        margin: 10px 0;
        color: @gray;
        font-size: @font-micro;
        font-weight: @weight-bold;
        text-align: center;
        -webkit-transition: all .2s ease-in;
        -moz-transition: all .2s ease-in;
        -ms-transition: all .2s ease-in;
        -o-transition: all .2s ease-in;
        transition: all .2s ease-in;
        &:hover {
          cursor: pointer;
          border: 2px solid #F4815A;
          background-color: #F4815A;
          color: @white;
        }
      }

      .line {
        width: 100%;
        height: 2px;
        background-color: @light-gray;
      }
      .logout_btn {
        border: 2px solid @gray;
        border-radius: @size-border-radius;
        width: 80%;
        margin-top: 20px;
        padding: 15px;
        color: @gray;
        font-size: @font-small;
        font-weight: @weight-bold;
        text-align: center;
        // transition area
        -webkit-transition: all .2s ease-in;
        -moz-transition: all .2s ease-in;
        -ms-transition: all .2s ease-in;
        -o-transition: all .2s ease-in;
        transition: all .2s ease-in;
        &:hover {
          cursor: pointer;
          border: 2px solid #F4815A;
          background-color: #F4815A;
          color: @white;
        }
      }
    }
  }
  .username {
    height: 100%;
    line-height:30px;
  }

  .avatar-container {
    position: relative;
    width: 100px;
    height: 100px;
  }

  .small-avatar-container {
    display: inline-block;
    vertical-align: middle;
    position: relative;
    width: 30px;
    height: 30px;
    font-size: 30px;
    margin-right: 3px;
    img {
      width: 30px;
      max-width: 30px;
    }
  }

  img {
    display: inline-block;
    width: 100% !important;
    height: auto !important;
    max-width: 100% !important;
    display: block;
    border-radius: @avatar-radius;
    box-shadow: 0px 0px 1px 0px;
  }

  ul {
    list-style: none;
  }

  .notifications-tab {
    transition: background-color .3s;
    font-size: 70%;
    position: absolute;
    display:flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    border-radius: @size-border-radius;
    top: 60px;
    right: 60px;
    min-height: 100px;
    max-height: 400px;
    width: 400px;
    background-color: @white;
    color: @white;
    box-shadow: 2px 5px 20px 2px rgba(90, 82, 128, 0.31);
    .notifications-table {
      width: inherit;
      overflow-x: hidden;
      // scrollbar
      &::-webkit-scrollbar {
        background-color: transparent;
        width: 15px;
      }
      &:hover {

        &::-webkit-scrollbar {
          width: 15px;
          height: 20px;
        }

        &::-webkit-scrollbar-track {
          background-color: transparent;
        }

        &::-webkit-scrollbar-thumb {
          background-color: #d6dee1;
          border-radius: 20px;
          border: 6px solid transparent;
          background-clip: content-box;
        }
      }
    }
    .notifications-entry {
      padding: 10px 10px 10px 20px;
      cursor: pointer;
      &:hover {
        background: rgb(0,0,0);
        background: linear-gradient(0deg, rgba(240, 240, 240, 0.3) 0%, rgba(255,255,255,0.6) 100%);
      }
      div:first-child {
        display: flex;
        flex-direction: column;
        div:first-child {
          color: @dark-white;
          line-height: 20px;
          display: flex;
          justify-content: space-between;
          flex-direction: row;
          div:first-child {
            display: flex;  
          }
          #icon-container {
            margin-right: 10px;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: @white;

            .icon {
              margin: auto;
              color: @white;
            }
          }
        }
      }
      #notification-content {
        color: @white;
      }
      #notification-type {
        -webkit-text-stroke: .3px;
      }
    }

    hr {
      border: 0;
      border-top: 1px solid #dfdfdf;
      margin-left: 20px;
    }

    #all-notifications {
      width: inherit;
      hr {
        border: 0;
        border-top: 1px solid #dfdfdf;
        margin: 0;
      }
      a {
        color: @light-purple;
        padding-right: 15px;
        -webkit-text-stroke: .3px;
        &:hover {
          color: #F4815A;
          transition: color .3s ease-in;
        }
      }
      height: 50px;
      line-height: 50px;
      text-align: right;
      //color: #e0dafc4d;
    }
  }

  .no-notifications {
    line-height: 50px;
    text-align: center;
    font-size: 120%;
    -webkit-text-stroke: .2px;
    color: @white;
  }

  @media screen and (min-width: 901px) {
    .bar_list {
      padding-right: 30px;
      padding-left: 30px;
    }
  }

  @media screen and (max-width : 900px) {
    .bar_list .ivu-menu-submenu {
      &:hover {
        pointer-events: none;
      }
    }
    .home_bar {
      width: 100vw;
      height: 60px;
      background-color: #263A8C;
      //  vertical nav일시 상단 전체가 커서가 되는 것을 방지
      &:hover {
        cursor: default;
      }
    }
    .bar_list {
      padding-left: 0;
      padding-right: 0;
      display: none;
      background-color: @white;
      border: solid 1px @white;
      transition: all 2s ease-in;
      &:hover {
        color: #F4815A;
        border-bottom-color: #F4815A;
      }
      &:last-child {
        border-bottom: solid 2px;
        border-bottom-color: #F4815A;
      }
    }
    .bar_list.open {
      display: block;
      // transition: all 2s ease-in;
    }
    .navbar_toggle-btn {
      height: 60px;
      line-height: 60px;
      display: block !important;
      &:hover {
        cursor: pointer;
      }
    }
    .oj-menu {
      display: flex;
      flex-direction: column;
    }
    .account_tab {
      display: none;
    }
  }
  
  /** transition group */
  .fade-enter-active, .fade-leave-active {
      transition: opacity .2s ease-in-out
  }
  .fade-enter,.fade-leave-to {
      opacity: 0
  }

</style>

<style lang="less">
@import '../../../styles/common.less';
  @media screen and (max-width : 900px) {
    #header {
      max-width: 100vw;
      .home_bar.ivu-menu-item {
        min-width: 100vw;
      }
    }
    
    .ivu-menu-light .ivu-menu-vertical .ivu-menu-item-active:not(.ivu-menu-submenu) {
        background:@light-purple;
    }
    .bar_list {
      padding-left: 0;
      padding-right: 0;
    }
  }
  .bar_list .ivu-menu-vertical .ivu-menu-item:hover, .ivu-menu-vertical .ivu-menu-submenu-title:hover {
    color: #F4815A;
  }
  .ivu-menu-vertical .ivu-menu-item:hover, .ivu-menu-vertical .ivu-menu-submenu-title:hover {
    color: #F4815A;
  }
  .ivu-menu-horizontal .ivu-menu-submenu .ivu-select-dropdown .ivu-menu-item a {
    color: @default-font-color !important;
  }
  .ivu-menu-item .ivu-menu-item-active .ivu-menu-item-selected {
    color: #F4815A !important;
  }
  .ivu-menu-horizontal .ivu-menu-submenu .ivu-select-dropdown .ivu-menu-item-selected  a {
    color: #F4815A !important;
  }
  .ivu-menu-light.ivu-menu-vertical .ivu-menu-item-active:not(.ivu-menu-submenu) {
    background: @pale-purple;
    &:first-child {
      background: #fff !important;
    }
  }
  .bar_list  {
    & .ivu-menu{
      background-color: @pale-purple !important;
      color: #20242c;
      text-align: center;
      & .ivu-menu-item {  // ivue commponent에서 padding-left가 48px로 되어있어 강제로 가운데 맞춤
        padding-left: 24px !important;
        padding-right: 24px !important;
      }
    }
  }
</style>