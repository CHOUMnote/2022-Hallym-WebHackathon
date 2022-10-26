<template>
  <div class="container">
    <div class="flex-container ">
      <div id="contest-main">
        <!--children-->
        <transition name="fadeInUp">
          <router-view></router-view>
        </transition>
        <!--children end-->
        <div class="flex-item" v-if="route_name === 'contest-details'">
          <template>
            <div id="contest-desc">
              <Panel :padding="20" shadow>
                <div slot="title">
                  {{contest.title}}
                </div>
                <div slot="extra">
                  <Tag type="dot" :color="countdownColor">
                    <span id="countdown">{{countdown}}</span>
                  </Tag>
                </div>
                <div v-html="contest.description" class="markdown-body"></div>
                <div v-if="passwordFormVisible" class="contest-password">
                  <Input v-model="contestPassword" type="password"
                         placeholder="contest password" class="contest-password-input"
                         @on-enter="checkPassword"/>
                  <Button type="info" @click="checkPassword">Enter</Button>
                </div>
              </Panel>
              <Table :columns="columns" :data="contest_table" disabled-hover style="margin-bottom: 40px;"></Table>
            </div>
          </template>
        </div>
  
      </div>
      <div v-show="showMenu" id="contest-menu">
        <VerticalMenu @on-click="handleRoute">
          <VerticalMenu-item class="list" :route="{name: 'contest-details', params: {contestID: contestID}}">
            <Icon type="md-eye" />
            <!-- <Icon type="home"></Icon> -->
            {{$t('m.Overview')}}
          </VerticalMenu-item>
  
          <VerticalMenu-item class="list" :disabled="contestMenuDisabled"
                             :route="{name: 'contest-announcement-list', params: {contestID: contestID}}">
            <Icon type="ios-chatbubbles" />
            <!-- <Icon type="chatbubble-working"></Icon> -->
            {{$t('m.Announcements')}}
          </VerticalMenu-item>
  
          <VerticalMenu-item class="list" :disabled="contestMenuDisabled"
                             :route="{name: 'contest-problem-list', params: {contestID: contestID}}">
            <Icon type="ios-photos"></Icon>
            {{$t('m.Problems')}}
          </VerticalMenu-item>
  
          <VerticalMenu-item v-if="OIContestRealTimePermission"
                             class="list" :disabled="contestMenuDisabled"
                             :route="{name: 'contest-submission-list'}">
            <Icon type="md-arrow-round-up" />
            <!-- <Icon type="navicon-round"></Icon> -->
            제출 현황
            <!-- {{$t('m.Submissions')}} -->
          </VerticalMenu-item>
  
          <!-- 랭킹 -->
          <!-- <VerticalMenu-item v-if="OIContestRealTimePermission"
                             class="list" :disabled="contestMenuDisabled"
                             :route="{name: 'contest-rank', params: {contestID: contestID}}">
            <Icon type="ios-stats" /> -->
            <!-- <Icon type="stats-bars"></Icon> -->
            <!-- {{$t('m.Rankings')}} -->
          <!-- </VerticalMenu-item> -->
  
          <VerticalMenu-item v-if="showAdminHelper && isContestAdmin"
                             class="list" :route="{name: 'acm-helper', params: {contestID: contestID}}">
            <Icon type="ios-paw"></Icon>
            도움말
            <!-- {{$t('m.Admin_Helper')}} -->
          </VerticalMenu-item>
        </VerticalMenu>
      </div>
    </div>
  </div>
  </template>
  
  <script>
    import moment from 'moment'
    import api from '@oj/api'
    import { mapState, mapGetters, mapActions } from 'vuex'
    import { types } from '@/store'
    import { CONTEST_STATUS_REVERSE, CONTEST_STATUS } from '@/utils/constants'
    import time from '@/utils/time'

    export default {
      name: 'ContestDetail',
      components: {},
      data () {
        return {
          CONTEST_STATUS: CONTEST_STATUS,
          route_name: '',
          btnLoading: false,
          contestID: '',
          contestPassword: '',
          columns: [
            {
              title: this.$i18n.t('m.StartAt'),
              render: (h, params) => {
                return h('span', time.utcToLocal(params.row.start_time, 'YYYY-MM-DD HH:mm:ss'))
              }
            },
            {
              title: this.$i18n.t('m.EndAt'),
              render: (h, params) => {
                return h('span', time.utcToLocal(params.row.end_time, 'YYYY-MM-DD HH:mm:ss'))
              }
            },
            {
              title: this.$i18n.t('m.ContestType'),
              render: (h, params) => {
                if (params.row.contest_type === undefined) {
                  return h('span', this.$i18n.t('m.' + params.row.contest_type))
                }
                return h('span', this.$i18n.t('m.' + params.row.contest_type.replace(' ', '_')))
              }
            },
            {
              title: this.$i18n.t('m.Rule'),
              render: (h, params) => {
                return h('span', this.$i18n.t('m.' + params.row.rule_type))
              }
            },
            {
              title: this.$i18n.t('m.Creator'),
              render: (h, data) => {
                return h('span', data.row.created_by.username)
              }
            }
          ]
        }
      },
      mounted () {
        this.contestID = this.$route.params.contestID
        this.route_name = this.$route.name
        this.$store.dispatch('getContest').then(res => {
          this.changeDomTitle({title: res.data.data.title})
          let data = res.data.data
          let endTime = moment(data.end_time)
          if (endTime.isAfter(moment(data.now))) {
            this.timer = setInterval(() => {
              this.$store.commit(types.NOW_ADD_1S)
            }, 1000)
          }
        })
      },
      methods: {
        ...mapActions(['changeDomTitle']),
        handleRoute (route) {
          this.$router.push(route).catch(() => {})
        },
        checkPassword () {
          if (this.contestPassword === '') {
            this.$error('Password can\'t be empty')
            return
          }
          this.btnLoading = true
          api.checkContestPassword(this.contestID, this.contestPassword).then((res) => {
            this.$success('Succeeded')
            this.$store.commit(types.CONTEST_ACCESS, {access: true})
            this.btnLoading = false
          }, (res) => {
            this.btnLoading = false
          })
        }
      },
      computed: {
        ...mapState({
          showMenu: state => state.contest.itemVisible.menu,
          contest: state => state.contest.contest,
          contest_table: state => [state.contest.contest],
          now: state => state.contest.now
        }),
        ...mapGetters(
          ['contestMenuDisabled', 'contestRuleType', 'contestStatus', 'countdown', 'isContestAdmin',
            'OIContestRealTimePermission', 'passwordFormVisible']
        ),
        countdownColor () {
          if (this.contestStatus) {
            return CONTEST_STATUS_REVERSE[this.contestStatus].color
          }
        },
        showAdminHelper () {
          return this.isContestAdmin && this.contestRuleType === 'ACM'
        }
      },
      watch: {
        '$route' (newVal) {
          this.route_name = newVal.name
          this.contestID = newVal.params.contestID
          this.changeDomTitle({title: this.contest.title})
        }
      },
      beforeDestroy () {
        clearInterval(this.timer)
        this.$store.commit(types.CLEAR_CONTEST)
      }
    }
</script>

<style scoped lang="less">
  body {
    padding-bottom: 0 !important;
    max-height: 100vh !important;
  }
  pre {
    display: inline-block;
  }

  #countdown {
    font-size: 16px;
  }
  .container {
    width: 100%;
    //padding: 0 40px;
  }
  .flex-container {
    #contest-main {
      flex: 1 1;
      width: 0;
    }
  }
    #countdown {
      font-size: 16px;
    }
    .container {
      width: 100%;
      padding: 0 40px;
    }
    .flex-container {
      #contest-main {
        flex: 1 1;
        width: 0;
        
      }
      #contest-desc {
        flex: auto;
      }
      #contest-menu {
        flex: none;
        width: 210px;
        margin-left: 20px;
        .list {
          cursor: pointer;
        }
      }
  
      .contest-password {
        margin-top: 20px;
        margin-bottom: -10px;
        &-input {
          width: 200px;
          margin-right: 10px;
        }
      }
    }
  @media screen and (max-width : 900px) {
    .container {
      padding: 0;
    }
    .flex-container {
      width: 100vw;
      margin: 0;
      flex-direction: column-reverse;
      align-items: center;

    }
    #contest-main {
      width: 90% !important;
      //overflow: hidden;
    }
    #contest-menu {
      width: 90% !important;
      margin: 0 0 20px 0 !important;
    }
  }
  </style>
  