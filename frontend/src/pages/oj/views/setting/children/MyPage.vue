<template>
  <div class="setting-main">
    <div>
      <div v-if="profile.user">
        <!-- <p style="font-size: 18px">
          <span @v-if="profile.user" class="emphasis" style="margin: 2em; margin-top:10px; margin-botton:15px; font-weight:600">{{profile.user.username}}</span>
          <span v-if="profile.school">{{profile.school}}</span>
        </p>
        <p v-if="profile.mood">
          {{profile.mood}}
        </p> -->
        <div class="flex-container">
          <div class="score">
            <div class="left">
              <p class="emphasis">{{profile.accepted_number}}</p>
              <p>{{$t('m.UserHomeSolved')}}</p>
            </div>
            <div class="middle">
              <p class="emphasis">{{profile.submission_number}}</p>
              <p>{{$t('m.UserHomeserSubmissions')}}</p>
            </div>
            <div class="right">
              <p class="emphasis">{{profile.total_score}}</p>
              <p>{{$t('m.UserHomeScore')}}</p>
            </div>
          </div>
          <div class="btn-menu">
            <div class="button"
              @click="goCommentList" style="margin-right: 140px;">
              <Icon size=25 type="ios-chatboxes-outline" />
              댓글 단 글
            </div>
            <div class="button"
              @click="goLikeList">
              <Icon size=25 type="ios-heart-outline" />
              좋아요 한 글
            </div>
          </div>
        </div>
        <div>
          <div id="problems">
            <div class="solved-container" v-if="problems.length">{{$t('m.List_Solved_Problems')}}
              <Poptip v-if="refreshVisible" trigger="hover" placement="right-start">
                <Icon type="ios-help-outline"></Icon>
                <div slot="content">
                  <p>If you find the following problem id does not exist,<br> try to click the button.</p>
                  <Button type="info" @click="freshProblemDisplayID">regenerate</Button>
                </div>
              </Poptip>
            </div>
            <p class="no-solved" v-else>{{$t('m.UserHomeIntro')}}</p>
            <div class="btns">
              <div class="problem-btn" v-for="problemID of problems" :key="problemID">
                <Button class="btn-padding" @click="goProblem(problemID)">{{problemID}}</Button>
              </div>
            </div>
          </div>
        </div>
        <div>
          <div id="icons">
            <a :href="profile.github">
              <Icon type="social-github-outline" size="30"></Icon>
            </a>
            <a :href="'mailto:'+ profile.user.email">
              <Icon class="icon" type="ios-email-outline" size="30"></Icon>
            </a>
            <a :href="profile.blog">
              <Icon class="icon" type="ios-world-outline" size="30"></Icon>
            </a>
          </div>
        </div>
      </div>

      <!-- github같은 잔디 (현재 비활성화) -->
      <!-- <Grass></Grass> -->

      <!-- account setting, profile setting button -->
      <!-- <div>
        <div class="btn-menu">
          <div style="margin-top: 10px;">
            <Button
              shape="circle"
              @click="goCommentList"
              style="margin-left: 5px;">
              댓글 단 글
            </Button>
            <Button
              shape="circle"
              @click="goLikeList"
              style="margin-left: 5px;">
              좋아요 한 글
            </Button>
          </div>
        </div>
      </div> -->
    </div>
  </div>
</template>
<script>
  import { mapActions } from 'vuex'
  import time from '@/utils/time'
  import api from '@oj/api'
  import Grass from '../../user/Grass.vue'
  export default {
    components: {
      Grass
    },
    data () {
      return {
        username: '',
        profile: {},
        problems: []
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      ...mapActions(['changeDomTitle']),
      init () {
        this.username = this.$route.query.username
        api.getUserInfo(this.username).then(res => {
          this.changeDomTitle({title: res.data.data.user.username})
          this.profile = res.data.data
          this.getSolvedProblems()
        })
      },
      goProfileSetting () {
        this.$router.push({name: 'profile-setting'}).catch(() => {})
      },
      goAccountSetting () {
        this.$router.push({name: 'account-setting'}).catch(() => {})
      },
      goCommentList () {
        this.$router.push({name: 'comment-list'}).catch(() => {})
      },
      goLikeList () {
        this.$router.push({name: 'like-list'}).catch(() => {})
      },
      getSolvedProblems () {
        let ACMProblems = this.profile.acm_problems_status.problems || {}
        let OIProblems = this.profile.oi_problems_status.problems || {}
        // todo oi problems
        let ACProblems = []
        for (let problems of [ACMProblems, OIProblems]) {
          Object.keys(problems).forEach(problemID => {
            if (problems[problemID]['status'] === 0) {
              ACProblems.push(problems[problemID]['_id'])
            }
          })
        }
        ACProblems.sort()
        this.problems = ACProblems
      },
      goProblem (problemID) {
        this.$router.push({name: 'problem-details', params: {problemID: problemID}}).catch(() => {})
      },
      freshProblemDisplayID () {
        api.freshDisplayID().then(res => {
          this.$success('Update successfully')
          this.init()
        })
      }
    },
    computed: {
      refreshVisible () {
        if (!this.username) return true
        if (this.username && this.username === this.$store.getters.user.username) return true
        return false
      }
    },
    watch: {
      '$route' (newVal, oldVal) {
        if (newVal !== oldVal) {
          this.init()
        }
      }
    }
  }
</script>

<style lang="less" scoped>
  @import '../../../../../styles/common.less';
  .container {
    position: relative;
    text-align: center;
    margin: 170px auto;
    p {
      margin-top: 8px;
      margin-bottom: 8px;
    }
    .avatar-container {
      position: absolute;
      left: 50%;
      transform: translate(-50%);
      z-index: 1;
      top: -90px;
      .avatar {
        width: 140px;
        height: 140px;
        border-radius: 50%;
        box-shadow: 0 1px 1px 0;
      }
    }
    .emphasis {
      font-size: 25px;
      font-weight: 400;
      -webkit-text-stroke: 1px;
      text-align: center;
    }
    #split {
      margin: 20px auto;
      width: 90%;
    }
    .flex-container {
      display: flex;
      flex-direction: column;
      margin-top: 30px;
      text-align: center;
      font-weight: 400;
      font-size: 16px;
      box-shadow: 0px 3px 10px rgba(0, 0, 0, 0.25);
      border-radius: 5px;
      color: @black;
      .score {
        margin: 20px 0;
        width: inherit;
        display: flex;
        justify-content: space-around;
        .left, .middle, .right {
          flex: 1 1;

        }
        .middle {
          border-right: 2px solid @light-gray;
          border-left: 2px solid @light-gray;
        }
      }
      .btn-menu {
        width: inherit;
        display: flex;
        justify-content: center;
        background-color: #EEEEEE;
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
        font-size: 16px;
        margin-right: 10px;
        color: @gray;
        .button {
          padding: 10px 0;
          cursor: pointer;
          &:hover {
            color: @black;
            transition: color .3s ease-in-out;
          }
        }
      }
    }
    #problems {
      color: @purple;
      .no-solved {
        text-align: center;
        color: @gray;
        margin-top: 100px;
      }
      .solved-container {
        -webkit-text-stroke: .5px;
        border-bottom: 2px solid @purple;
      }
      margin-top: 40px;
      font-size: 18px;
      font-weight: 400;
      .btns {
        margin-top: 10px;
        .problem-btn {
          display: inline-block;
          .btn-padding {
            padding: 0 10px !important;
            margin-right: 5px;
          }
        }
      }
    }
    #icons {
      position: absolute;
      padding-bottom: auto 20px;
      left: 50%;
      transform: translate(-50%);
      .icon {
        padding-left: 20px;
      }
    }
  }
</style>
