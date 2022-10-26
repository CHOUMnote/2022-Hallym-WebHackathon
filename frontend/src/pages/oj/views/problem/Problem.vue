<template>
  <div class="flex-container">
    <div id="problem-main">
      <!--problem main-->
      <Panel :padding='40' shadow>
        <div slot="title">{{problem.title}}</div>
        <div id="problem-content" class="markdown-body" v-katex>
          <p class="title">문제 설명</p>
          <p class="content" v-html="problem.description"></p>
          <!-- {{$t("m.music")}} -->
          <p class="title">입력 <span v-if="problem.io_mode.io_mode=='File IO'">({{$t("m.FromFile")}}: {{ problem.io_mode.input }})</span></p>
          <p class="content" v-html='problem.input_description'></p>
          <p class="title">출력 <span v-if="problem.io_mode.io_mode=='File IO'">({{$t("m.ToFile")}}: {{ problem.io_mode.output }})</span></p>
          <p class="content" v-html="problem.output_description"></p>
          <div v-for="(sample, index) of problem.samples" :key="index">
            <div class="in-out-container sample">
              <div class="sample-input">
                <p class="title">{{$t("m.Sample_Input")}} {{index + 1}}
                  <a class="copy"
                      v-clipboard:copy="sample.input"
                      v-clipboard:success="onCopy"
                      v-clipboard:error="onCopyError">
                    <Icon type="md-clipboard"></Icon>
                  </a>
                </p>
                <p style="white-space: pre;" class="input-for-pre">{{sample.input}}</p>
              </div>
              <div class="sample-output">
                <p class="title">{{$t("m.Sample_Output")}} {{index + 1}}</p>
                <p style="white-space: pre;" class="input-for-pre">{{sample.output}}</p>
              </div>
            </div>
          </div>
          <div v-if="problem.hint">
            <div class="hide" @click="hintHide()">
              <p class="title">{{$t('m.Hint')}}</p>
              <Button v-if="!hintHidden" size="large" class="hint-hide-btn"><Icon type="md-eye" /></Button>
              <Button v-else size="large" class="hint-hide-btn"><Icon type="md-eye-off" /></Button>
            </div>
            <p v-html="problem.hint" v-bind:style="[hintHidden ?{'visibility' : 'hidden'}:{'display' : 'block'}]"></p>
          </div>
          <div v-if="problem.source">
            <p class="title">{{$t("m.Source")}}</p>
            <p class="content">{{problem.source}}</p>
          </div>
        </div>
      </Panel>
    </div>
    <div id="right-column">
      <!-- 제출 버튼 -->
      <VerticalMenu style="margin-bottom: 20px;">
        <!-- <VerticalMenu-item :route="{name: "contest-problem-list", params: {contestID: contestID}}"> -->
          <Button v-if="isAuthenticated && isVerifiedEmail" type="primary" size="large" @click="goSubmitView" long>제출하기</Button>
          <Button v-else type="primary" size="large" disabled long>제출하기</Button>
        <!-- </VerticalMenu-item> -->
      </VerticalMenu>
      <VerticalMenu @on-click="handleRoute">
        <template v-if="this.contestID">
          <VerticalMenu-item :route="{name: 'contest-problem-list', params: {contestID: contestID}}">
            <Icon type="ios-photos"></Icon>
            {{$t("m.Problems")}}
          </VerticalMenu-item>
          <VerticalMenu-item :route="{name: 'contest-announcement-list', params: {contestID: contestID}}">
            <Icon type="chatbubble-working"></Icon>
            {{$t("m.Announcements")}}
          </VerticalMenu-item>
        </template>
        <VerticalMenu-item class="list" v-if="!this.contestID || OIContestRealTimePermission" :route="submissionRoute">
          <Icon type="navicon-round"></Icon>
          제출 현황
          <!-- {{$t("m.Submissions")}} -->
        </VerticalMenu-item>
        <template v-if="this.contestID">
          <VerticalMenu-item v-if="!this.contestID || OIContestRealTimePermission"
            :route="{name: 'contest-rank', params: {contestID: contestID}}">
            <Icon type="stats-bars"></Icon>
            {{$t("m.Rankings")}}
          </VerticalMenu-item>
          <VerticalMenu-item :route="{name: 'contest-details', params: {contestID: contestID}}">
            <Icon type="home"></Icon>
            {{$t("m.View_Contest")}}
          </VerticalMenu-item>
        </template>
      </VerticalMenu>
      <Card id="info" class="tag-card">
        <div slot="title" class="header">
          <Icon type="information-circled"></Icon>
          <span class="card-title">{{$t("m.Information")}}</span>
        </div>
        <ul>
          <li><p>문제 번호</p>
            <p>{{problem._id}}</p></li>
          <li>
            <p>{{$t("m.Time_Limit")}}</p>
            <p>{{problem.time_limit}}MS</p></li>
          <li>
            <p>{{$t("m.Memory_Limit")}}</p>
            <p>{{problem.memory_limit}}MB</p>
          </li>
          <!-- <li> -->
          <li>
            <p>{{$t("m.IOMode")}}</p>
            <p>{{problem.io_mode.io_mode}}</p>
          </li>
          <li>
            <p>{{$t("m.Created")}}</p>
            <p>{{problem.created_by.username}}</p>
          </li>
          <li v-if="problem.difficulty">
            <p>{{$t("m.Level")}}</p>
            <p>{{$t("m." + problem.difficulty)}}</p>
          </li>
          <li v-if="problem.total_score">
            <p>{{$t("m.Score")}}</p>
            <p>{{problem.total_score}}</p>
          </li>
          <li>
            <p>{{$t("m.Tags")}}</p>
            <p>
              <Poptip trigger="hover" placement="left-end">
                <a class="show">{{$t("m.Show")}}</a>
                <div slot="content">
                  <Tag v-for="tag in problem.tags" :key="tag">{{tag}}</Tag>
                </div>
              </Poptip>
            </p>
          </li>
        </ul>
      </Card>
    </div>
  </div>
 </template>



<script>
  import {mapGetters, mapActions} from 'vuex'
  import {types} from '../../../../store'
  import {FormMixin} from '@oj/components/mixins'
  import api from '@oj/api'
  import ProblemCategory from './ProblemCategory.vue'

  export default {
    name: 'Problem',
    mixins: [FormMixin],
    data () {
      return {
        version: process.env.VERSION,
        // submit 화면 여부
        contestID: '',
        problemID: '',
        submissionId: '',
        hintHidden: true,
        problem: {
          title: '',
          description: '',
          hint: '',
          my_status: '',
          template: {},
          languages: [],
          created_by: {
            username: ''
          },
          tags: [],
          io_mode: { 'io_mode': 'Standard IO' }
        }
      }
    },
    mounted () {
      this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, { menu: false })
      this.init()
      this.getWebsiteConfig()
    },
    methods: {
      ...mapActions(['changeDomTitle', 'getWebsiteConfig']),
      init () {
        this.$Loading.start()
        // routes.js에 정의 된 params
        this.contestID = this.$route.params.contestID
        this.problemID = this.$route.params.problemID
        let func = this.$route.name === 'problem-details' ? 'getProblem' : 'getContestProblem'
        api[func](this.problemID, this.contestID).then(res => {
          this.$Loading.finish()
          let problem = res.data.data
          this.changeDomTitle({ title: problem.title })
          problem.languages = problem.languages.sort()
          this.problem = problem
          // 로컬에 코드가 있고 템플릿을 로드할 필요가 없음을 나타내는 beforeRouteEnter에서 수정됨
        }, () => {
          this.$Loading.error()
        })
      },
      handleRoute (route) {
        this.$router.push(route).catch(() => { })
      },
      goSubmitView () {
        if (this.contestID) {
          this.$router.push({ name: 'contest-problem-submission' }).catch(() => {})
        } else {
          this.$router.push({ name: 'problem-submission' }).catch(() => {})
        }
      },
      onCopy (event) {
        this.$success('Code copied')
      },
      onCopyError (e) {
        this.$error('Failed to copy code')
      },
      goHome () {
        this.$router.push('/').catch(() => { })
      },
      goSubmissionList () {
        if (this.contestID) {
          this.$router.push({ name: 'contest-submission-list', query: { problemID: this.problemID } }).catch(() => {})
        } else {
          this.$router.push({ name: 'submission-list', query: { problemID: this.problemID } }).catch(() => { })
        }
      },
      hintHide () {
        this.hintHidden = !this.hintHidden
      }
    },
    computed: {
      ...mapGetters(['problemSubmitDisabled', 'contestRuleType', 'OIContestRealTimePermission', 'contestStatus', 'website', 'isVerifiedEmail', 'isAuthenticated']),
      contest () {
        return this.$store.state.contest.contest
      },
      submissionRoute () {
        if (this.contestID) {
          return {
            name: 'contest-submission-list',
            query: {
              problemID: this.problemID
            }
          }
        } else {
          return {
            name: 'submission-list',
            query: {
              problemID: this.problemID
            }
          }
        }
      }
    },
    watch: {
      '$route' () {
        this.init()
      },
      'website' () {
        this.changeDomTitle()
      }
    }
}
</script>

<style lang='less' scoped>
@import '../../../../styles/common.less';
  .card-title {
    margin-left: 8px;
  }

  .in-out-container {
    display: flex;
    left: 0;
    max-width: calc(~'100vw - 100px');
    justify-content: flex-start;
    flex-wrap: wrap;
    .sample {
      align-items: stretch;
      &-input, &-output {
        min-width: 200px;
        width: 45%;
        flex: 1 1 auto;
        display: flex;
        flex-direction: column;
        margin-right: 5%;
      }
      pre {
        flex: 1 1 auto;
        align-self: stretch;
        border-style: solid;
        background: transparent;
      }
    }
  }
  .flex-container {
    max-width: calc(~'100vw - 100px');
    justify-content: center;
    min-width: 725px; // left-item min width + right-item min width
    #problem-main {
      width: 75vw;
      min-width: 500px;
      margin-right: 18px;
      margin-left: 50px;
    }
    #right-column {
      min-width: 220px;
    }
  }
  #problem-content {
    margin-top: -50px;
    margin-left: 10px;
    .title {
      font-size: 18px;
      font-weight: 600;
      margin: 50px 0 20px 0;
      color: @purple;
      .copy {
        padding-left: 8px;
        i {
          color: @purple;
        }
      }
    }
    p.content {
      margin-right: 20px;
      font-size: 15px
    }

  }

  #info {
    ivu-card-body {
      margin-left: 20px;
      margin-right: 20px;
    }
    margin-bottom: 20px;
    margin-top: 20px;
    ul {
      list-style-type: none;
      li {
        border-bottom: 1px dotted #e9eaec;
        margin-bottom: 10px;
        p {
          display: inline-block;
          .show {
            color: @purple;
          }
        }
        p:first-child {
          width: 90px;
        }
        p:last-child {
          float: right;
        }
      }
    }
  }


  #pieChart-detail {
    margin-top: 20px;
    width: 500px;
    height: 480px;
  }

  .input-for-pre {
    min-width: 90px;

  }

  .hint-hide-btn {
    padding: 0px;
    margin-left: 10px;
    margin-top: 25px;
    border-color: transparent;
    color: @purple;
    &:hover, &:focus {
      border-color: transparent;
      box-shadow: none;
    }
  }

  .hide {
    display: flex;
    cursor: pointer;
  }

</style>
<style lang='less'>
@import '../../../../styles/common.less';
  .tag-card {
    & > .ivu-card-body {
      padding-left: 20px;
      padding-right: 20px;
    }
  }

  #right-column {
    .list:hover {
      cursor: pointer;
    }
  }
  .help-btn{
    float: left;
    color: white;
    font-size: 16px;
    padding: 0 10px;
    * {
      color: white;
      transition: all 0.1s ease-in-out;
    }

    &:hover * {
      background-color: #ffffff00;
      color: @purple;
    }
  }
</style>
