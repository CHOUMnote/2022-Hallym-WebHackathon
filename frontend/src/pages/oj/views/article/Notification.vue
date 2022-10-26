<template>
  <div class="flex-container">
    <div id="main">
      <div>
        
        <div class="community_free">
        <div class="community_free_title" slot="title">알림</div>

          <!-- <div>
            <Table stripe :disabled-hover="true" :columns="columns" :data="notifications"></Table>
          </div> -->

          <!-- 알림 목록 -->
          <p class="no-notifications" v-if="notifications.length == 0">알림이 없습니다.</p>
          <ul v-else class="notifications-table">
            <li v-for="(item) in notifications">
              <ul v-bind:style="[!item.is_read ?{'background-color' : '#e0dafc4d'}:{}]" class="notifications-entry"  @click="redirectToArticle(item)">
                <div>
                  <div id="icon-container">
                    <Icon v-if="item.notificationtype === 'COMMENT'" class="icon" size=24 type="ios-chatboxes" />
                    <Icon v-if="item.notificationtype === 'LIKE'" class="icon" size=24 type="md-heart" />
                  </div>
                  <div>
                    <div id="notification-type">
                      <li>{{ item.notificationtype }}</li>
                    </div>
                    <div id="notification-content">
                      <li> {{item.content}} </li>
                    </div>
                    <div id="notification-date">
                      <li id="date-time"> {{ convertDate(item.create_time) }} </li>
                    </div>
                  </div>
                </div>
              </ul>
              <hr>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  import api from '@oj/api'
  import time from '@/utils/time'

  export default {
    name: 'Notification',
    data () {
      return {
        columns: [ // 열 속성 - 추후 추가 예정
          {
            title: 'URL',
            align: 'center',
            render: (h, params) => {
              return h('a',
                {
                  style: {
                    'display': 'inline-block',
                    'max-width': '150px'
                  },
                  on: {
                    click: () => {
                      window.open(params.row.url)
                    }
                  }
                }, params.row.url)
            }
          },
          {
            title: '타입',
            align: 'center',
            render: (h, params) => {
              return h('span', params.row.notificationtype)
            }
          },
          {
            title: '내용',
            align: 'center',
            render: (h, params) => {
              return h('span', params.row.content)
            }
          },
          {
            title: '받는 사람',
            align: 'center',
            render: (h, params) => {
              return h('span', params.row.target_username)
            }
          },
          {
            title: '보낸 사람',
            align: 'center',
            render: (h, params) => {
              return h('span', params.row.action_username)
            }
          }
        ],
        notifications: [] // 게시글 목록
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        this.getNotifications() // 알림 리스트 가져오기
      },
      getNotifications () {
        api.getNotificationList().then(res => { // 현재 접속한 유저의 알림을 전송 받음
          this.notifications = res.data.data
        }).catch(() => {
        })
      },
      deleteNotification (notificationid) { // 알림 삭제
        api.deleteNotification(notificationid).then(res => { // 알림 고유 ID를 전송해 알림 삭제
          this.$router.push({name: 'notification-list'}).catch(() => {})
        })
      },
      checkNotification (notificationid) { // 알림 확인
        api.checkNotification(notificationid).then(res => { // 알림 고유 ID를 전송해 알림 확인
          this.$router.push({name: 'notification-list'}).catch(() => {})
        })
      },
      convertDate (date) {
        return time.utcToLocal(date, 'YYYY-MM-DD HH:mm')
      },
      redirectToArticle (notification) {
        console.log(notification)
        api.checkNotification(notification.id).then(res => {
          this.$router.push({path: notification.url})
        })
      }
    }
  }
</script>

<style scoped lang="less">
@import '../../../../styles/common.less';
  .flex-container {
    #main {
      margin: 0 5% 0 5%;
      padding: 15px 0 65px 0;
      background-color: #ffffff;
      width: 80vw;
    }
  }
      .community {
        display: inline-block;
        vertical-align: top;
        /* padding: 0 0 20px 0; */
        width: 17%;
        height: 15%;
        padding: 0 10px 20px 0;
        font-size: 16px;
        text-align: center;
    }

    .community_menu_name {
        display: block;
        font-size: 24px;
        color: #1f4e79;
    }

    .community_menu {
        display: block;
        /* vertical-align: top; */
        /* width: 20%; */
        /* height: 20%; */
        margin-top: 10px;
        padding: 0 0 20px 0;
        font-size: 16px;
        /* text-align: center; */
        /* background-color: rgb(232, 238, 177);  */
        border-top: 2px solid rgb(61, 61, 61);
        color: black;
    }

    .community_menu_list_main{
        padding: 10px 0;
        color: rgb(255, 255, 255);
        border-bottom: 1px solid rgb(61, 61, 61);
        background: #1f4e79;
    }

    .community_menu_list {
        padding: 10px 0;
        // color: black;
        border-bottom: 1px solid rgb(61, 61, 61);
    }

    .community_menu_list:hover {
        background-color: rgb(71, 141, 233);
        color: white;
    }
    .community_free {
        //display: inline-block;
        //vertical-align: top;
        //width: 100vw;
        //height: 60%;
        padding: 0 20px 0 20px;
        /* background-color: rgb(136, 167, 138); */
    }
    .community_free_bar{
        display: flex;
        justify-content: right;
        margin: 20px 0 10px 0;
    }
    .community_free_title {
        /* display: block; */
        /* margin-top: -10px; */
        padding: 0 0 10px 0;
        //border-bottom: 2px solid black;
        font-size: 24px;
        color: @black;
        text-align: center;
        -webkit-text-stroke: 0.5px;
        /* background-color: rgb(255, 234, 239); */
    }
    .submenu_list {
      display: inline-block;
      margin-right: 10px;
    }

    ul {
      list-style: none;
    }

    .notifications-entry {
      padding: 10px 0;
      cursor: pointer;
      &:hover {
        background: rgb(0,0,0);
        background: linear-gradient(0deg, rgba(240, 240, 240, 0.3) 0%, rgba(255,255,255,0.6) 100%);
      }
      div:first-of-type {
        display: flex;
        #icon-container {
          margin: 10px 10px;
          width: 50px;
          height: 50px;
          border-radius: 50%;
          background: @orange;

          .icon {
            margin: auto;
            color: @white;
          }
        }
        div:nth-of-type(2) {
          display: flex;
          flex-direction: column;
          color: @black;
          #notification-type {
            line-height: 20px;
            -webkit-text-stroke: 0.3px;
            color: @dark-white;
          }

          #notification-content {
            line-height: 30px;
          }

          #notification-date {
            line-height: 20px;
            font-size: 80%;
          }
        }
      }
    }

    .no-notifications {
      text-align: center;
      line-height: 50px;
      font-size: @font-small;
      color: @black;
      -webkit-text-stroke: .2px;
    }

    hr {
        border: 0;
        border-top: 1px solid #C4C4C4;
    }
</style>
