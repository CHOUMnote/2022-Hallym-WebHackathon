<template>
  <Panel shadow :padding="10">
    <div style="line-height: 50px; display: flex;" slot="title">
      <Button v-if="!listVisible" id="back-button" icon="md-arrow-back" size="large" @click="goBack" type="text"></Button>
      <div>{{title}}</div>
    </div>
    <div slot="extra">
      <!-- <Button v-if="listVisible" type="info" @click="init" :loading="btnLoading">{{$t('m.Refresh')}}</Button> -->
      <!-- <Button v-if="!listVisible" icon="ios-undo" @click="goBack">{{$t('m.Back')}}</Button> -->
    </div>

    <transition-group name="announcement-animate" mode="in-out">
      <div class="no-announcement" v-if="!announcements.length" key="no-announcement">
        <p>{{$t('m.No_Announcements')}}</p>
      </div>
      <template v-if="listVisible">
        <ul class="announcements-container" key="list">
          <li v-for="announcement in announcements" :key="announcement.title">
            <div class="entry">
              <div v-if="isAuthenticated" class="title"><a @click="goAnnouncement(announcement)">
                {{announcement.title}}</a></div>
              <div v-else class="title"><span class="non-a-tag">
                {{announcement.title}}</span></div>
              <div class="date-creator">
                <div class="creator"> {{announcement.created_by.username}} |</div>
                <div class="date">{{ convertDate(announcement.create_time) }}</div>
              </div>
            </div>
          </li>
        </ul>
        <Pagination v-if="!isContest"
                    key="page"
                    :total="total"
                    :page-size="limit"
                    @on-change="getAnnouncementList">
        </Pagination>
      </template>

      <template v-else>
        
        <div v-katex v-html="announcement.content" key="content" class="content-container markdown-body"></div>
      </template>
    </transition-group>
  </Panel>
</template>

<script>
  import api from '@oj/api'
  import time from '@/utils/time'
  import Pagination from '@oj/components/Pagination'
  import { mapGetters } from 'vuex'
  export default {
    name: 'Announcement',
    components: {
      Pagination
    },
    data () {
      return {
        limit: 10,
        total: 10,
        btnLoading: false,
        announcements: [],
        announcement: '',
        listVisible: true
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        if (this.isContest) {
          this.getContestAnnouncementList()
        } else {
          this.getAnnouncementList()
        }
      },
      getAnnouncementList (page = 1) {
        this.btnLoading = true
        api.getAnnouncementList((page - 1) * this.limit, this.limit).then(res => {
          this.btnLoading = false
          this.announcements = res.data.data.results
          this.total = res.data.data.total
        }, () => {
          this.btnLoading = false
        })
      },
      getContestAnnouncementList () {
        this.btnLoading = true
        api.getContestAnnouncementList(this.$route.params.contestID).then(res => {
          this.btnLoading = false
          this.announcements = res.data.data
        }, () => {
          this.btnLoading = false
        })
      },
      goAnnouncement (announcement) {
        this.announcement = announcement
        this.listVisible = false
      },
      goBack () {
        this.listVisible = true
        this.announcement = ''
      },
      convertDate (item) {
        return time.utcToLocal(item, 'YYYY-MM-DD HH:mm')
      }
    },
    computed: {
      ...mapGetters(['isAuthenticated']),
      title () {
        if (this.listVisible) {
          return this.isContest ? this.$i18n.t('m.Contest_Announcements') : this.$i18n.t('m.Announcements')
        } else {
          return this.announcement.title
        }
      },
      isContest () {
        return !!this.$route.params.contestID
      }
    }
  }
</script>

<style scoped lang="less">
@import '../../../../styles/common.less';
  .announcements-container {
    margin-top: -10px;
    margin-bottom: 10px;
    li {
      padding-top: 10px;
      list-style: none;
      padding-bottom: 10px;
      margin-left: 20px;
      font-size: @font-micro;
      border-bottom: 1px solid #C4C4C4;
      &:last-child {
        border-bottom: none;
      }
      .entry {
        display: flex;
        flex-direction: column;
        .title {
          text-align: left;
          a {
            color: @black;
            font-size: @font-regular;
            &:hover {
              color: @purple;
            }
          }
          span.non-a-tag {
            color: @black;
            font-size: @font-regular;
          }
        }
        .date-creator {
          display: flex;
          flex-direction: row;
          color: @gray;
          .creator {
            flex: none;
            text-align: center;
            margin-right: 5px;
          }
          .date {
            flex: none;
            text-align: center;
          }
        }
      }
    }
  }

  .content-container {
    padding: 0 20px 20px 20px;
  }

  .no-announcement {
    text-align: center;
    font-size: 16px;
  }

  .announcement-animate-enter-active {
    animation: fadeIn 1s;
  }

  #back-button {
    font-size: 120%;
    padding: 0px 8px;
    color: @gray;
    &:hover, &:focus {
      color: @black;
      border-color: transparent;
      box-shadow: 0 0 0 transparent;
    }
  }
</style>
