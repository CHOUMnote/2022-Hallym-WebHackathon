
<template>
  <div class="demo-split">
    <div class="ss_header">
      <div class="header-left">
        <div class="logo" @click="goHome">COU</div>
        <div class="problem-name" style="color: #bdbdbd" >[2022년 3월 코딩 테스트]</div>
        <div class="problem-name"> {{ problem.title }}</div>
      </div>
      <div class="header-right">
        <div class="help">
          <p @click="help_btn" class="help-btn">도움말</p>
        </div>
        <div v-if="!isAfterSubmit">
          <Button v-if="isActive" type="primary" size="large" style="z-index: '1'" :loading="submitted" class="hide-btn" @click="toggle(false)">공개
            <Icon type="md-eye" />
          </Button>
          <Button v-else type="primary" size="large" style="z-index: '1'" :loading="submitted" class="hide-btn" @click="toggle(true)">비공개
            <Icon type="md-eye-off" />
          </Button>
        </div>
        <div v-else="isAfterSubmit">
          <Button v-if="isActive" type="primary" size="large" style="z-index: '1'" disabled>공개로 제출 됨</Button>
          <Button v-else type="error" size="large" style="z-index: '1'" disabled>비공개로 제출 됨</Button>
        </div>
        <div>
          <!-- 제출 오남용을 방지하기 위해 제출 한 번으로 제한 -->
          <Button v-if="!isAfterSubmit" type="primary" size="large" style="z-index: '4'" :loading="submitted" @click="submitCode"
                  :disabled="problemSubmitDisabled" class="submit-btn">
            <span v-if="submitted">채점중</span>
            <span v-else>{{$t('m.Submit')}}</span>
          </Button>
          <Button v-else type="primary" size="large" @click="goSubmissionList" class="submit-btn">
            채점 현황 보러가기
            <Icon type="ios-arrow-forward"></Icon>
          </Button>
        </div>
      </div>  
    </div>
    <Split v-model="split3" v-bind:min="min1" v-bind:max="max1">
      <div slot="left" class="left-split-pane" >
        <Tabs value="name1" :animated="false">
          <TabPane :label="problem.title" name="name1" >   <!-- style="padding: 0 30px 10px 30px" -->
            <div class="problem_contents">
              <div id="problem-content" class="markdown-body" v-katex>
                <p class="title">{{$t('m.Description')}}</p>
                <p class="content" v-html="problem.description"></p>
                <p class="title">입력 <span v-if="problem.io_mode.io_mode=='File IO'">({{$t('m.FromFile')}}: {{ problem.io_mode.input }})</span></p>
                <p class="content" v-html="problem.input_description"></p>
                <p class="title">출력 <span v-if="problem.io_mode.io_mode=='File IO'">({{$t('m.ToFile')}}: {{ problem.io_mode.output }})</span></p>
                <p class="content" v-html="problem.output_description"></p>
                <div v-for="(sample, index) of problem.samples" :key="index">
                  <div class="flex-container-submit-mode sample split-sapple">
                    <div class="sample-input">
                      <p class="title">{{$t('m.Sample_Input')}} {{index + 1}}
                        <a class="copy"
                            v-clipboard:copy="sample.input"
                            v-clipboard:success="onCopy"
                            v-clipboard:error="onCopyError">
                          <Icon type="md-clipboard"></Icon>
                        </a>
                      </p>
                      <div style="white-space: pre;" class="input-for-pre">{{sample.input}}</div>
                    </div>
                    <div class="sample-output">
                      <p class="title">{{$t('m.Sample_Output')}} {{index + 1}}</p>
                      <div style="white-space: pre;" class="input-for-pre">{{sample.output}}</div>
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
              </div>
            </div>
          </TabPane>
        </Tabs>
      </div>
      <div slot="right" class="right-split-pane">
        <div style="clear:both;"></div>
        <!-- Right Padding -->
        <div class="problem_input">
          <!-- <Problem></Problem> -->
            <!-- height는 SubmitCodeMirror랑 같게 할 것 -->
          <SubmitCodeMirror :value.sync="code"
                      :languages="problem.languages"
                      :language="language"
                      :theme="theme"
                      :my_status="problem.my_status"
                      :statusVisible="statusVisible"
                      :contestID="this.contestID"
                      :OIContestRealTimePermission="OIContestRealTimePermission"
                      :submissionStatus="submissionStatus"
                      :submissionId = "submissionId"
                      :submissionExists="submissionExists"
                      :contestEnded="contestEnded"
                      @resetCode="onResetToTemplate"
                      @changeTheme="onChangeTheme"
                      @changeLang="onChangeLang"></SubmitCodeMirror>
          <!-- <Row type="flex" justify="space-between">
            제출 상태 icon
            <Col :span="10">
              <div class="status" v-if="statusVisible">
                <template v-if="!this.contestID || (this.contestID && OIContestRealTimePermission)">
                  <span>{{$t('m.Status')}}</span>
                  <Tag class="result" :color="submissionStatus.color" @click.native="handleRoute('/status/'+submissionId)">
                    {{$t('m.' + submissionStatus.text.replace(/ /g, "_"))}}
                  </Tag>
                </template>
                <template v-else-if="this.contestID && !OIContestRealTimePermission">
                  <Alert type="success" show-icon>{{$t('m.Submitted_successfully')}}</Alert>
                </template>
              </div>
              <div v-else-if="problem.my_status === 0">
                <Alert type="success" show-icon>{{$t('m.You_have_solved_the_problem')}}</Alert>
              </div>
              <div v-else-if="this.contestID && !OIContestRealTimePermission && submissionExists">
                <Alert type="success" show-icon>{{$t('m.You_have_submitted_a_solution')}}</Alert>
              </div>
              <div v-if="contestEnded">
                <Alert type="warning" show-icon>{{$t('m.Contest_has_ended')}}</Alert>
              </div>
            </Col>
          </Row> -->
        </div>
      </div>
    </Split>
    <!-- </div> -->
    <!-- <div class="ss_footer">
      <div class="footer_title" style="color:white" >2022년 3월 코딩 테스트</div>
      <div style="float: right">
        <div v-if="!isAfterSubmit" class="footer_btn" style="color:white">
          <Button v-if="isActive" type="primary" size="large" style="z-index: '1'" :loading="submitted" @click="toggle(false)">공개</Button>
          <Button v-else type="error" size="large" style="z-index: '1'" :loading="submitted" class="show" @click="toggle(true)">비공개</Button>
        </div>
        <div v-else="isAfterSubmit" class="footer_btn" style="color:white">
          <Button v-if="isActive" type="primary" size="large" style="z-index: '1'" disabled>공개로 제출 됨</Button>
          <Button v-else type="error" size="large" style="z-index: '1'" disabled>비공개로 제출 됨</Button>
        </div>
        <div class="footer_btn" style="color:white">
          제출 오남용을 방지하기 위해 제출 한 번으로 제한 -->
          <!-- <Button v-if="!isAfterSubmit" type="primary" size="large" style="z-index: '4'" :loading="submitted" @click="submitCode"
                  :disabled="problemSubmitDisabled">
            <span v-if="submitted">채점중</span>
            <span v-else>{{$t('m.Submit')}}</span>
          </Button>
          <Button v-else type="primary" size="large" @click="goSubmissionList">
            채점 현황 보러가기
            <Icon type="ios-arrow-forward"></Icon>
          </Button>
        </div>
      </div>
    </div> -->
  </div>
</template>




<script>
  import {mapGetters, mapActions} from 'vuex'
  import {types} from '../../../../store'
  import SubmitCodeMirror from '@oj/components/SubmitCodeMirror.vue'
  import CodeMirror from '@oj/components/CodeMirror.vue'
  import NavBar from '@oj/components/NavBar.vue'
  import storage from '@/utils/storage'
  import {FormMixin} from '@oj/components/mixins'
  import {JUDGE_STATUS, CONTEST_STATUS, buildProblemCodeKey} from '@/utils/constants'
  import api from '@oj/api'
  import {pie, largePie} from './chartData'

  // 이 상태의 그래픽 점유만 표시
  const filtedStatus = ['-1', '-2', '0', '1', '2', '3', '4', '8']

  export default {
    name: 'ProblemSubmission',
    components: {
      NavBar,
      CodeMirror,
      SubmitCodeMirror
    },
    mixins: [FormMixin],
    data () {
      return {
        openHelpModal: false,
        lastURL: '',
        version: process.env.VERSION,
        // submit 화면 여부
        isAfterSubmit: false,
        isActive: false,
        split3: 0.4,
        min1: '270px',
        max1: '97vw',
        statusVisible: false,
        captchaRequired: false,
        graphVisible: false,
        submissionExists: false,
        captchaCode: '',
        captchaSrc: '',
        contestID: '',
        problemID: '',
        submitting: false,
        code: '',
        language: 'C++',
        theme: 'base16-light',
        submissionId: '',
        submitted: false,
        hintHidden: true,
        result: {
          result: 9
        },
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
          io_mode: {'io_mode': 'Standard IO'}
        },
        pie: pie,
        largePie: largePie,
        // echarts 无法获取隐藏dom的大小，需手动指定
        largePieInitOpts: {
          width: '500',
          height: '480'
        }
      }
    },
    beforeRouteEnter (to, from, next) {
      let problemCode = storage.get(buildProblemCodeKey(to.params.problemID, to.params.contestID))
      if (problemCode) {
        next(vm => {
          vm.lastURL = from
          vm.language = problemCode.language
          vm.code = problemCode.code
          vm.theme = problemCode.theme
        })
      } else {
        next()
      }
    },
    mounted () {
      this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, {menu: false})
      this.init()
      this.getWebsiteConfig()
    },
    methods: {
      ...mapActions(['changeDomTitle', 'getWebsiteConfig']),
      help_btn () {
        // this.openHelpModal = true
        this.$Notice.open({
          title: '도움말',
          duration: 0,
          render: h => {
            return h('p', [
              '입력과 출력은 모두 Standard IO를 통해 읽고 출력하게 됩니다. 해당 문서는 ',
              h('a', {
                on: {
                  click: () => {
                    let routeData = this.$router.resolve({
                      name: 'languages'
                    })
                    window.open(routeData.href, '_blank')
                  }
                }
              }, '언어별 도움말'),
              '을 참고해주세요'
            ])
          }
        })
      },
      toggle (shared) {
        this.isActive = shared
      },
      init () {
        this.$Loading.start()
        // routes.js에 정의 된 params
        this.contestID = this.$route.params.contestID
        this.problemID = this.$route.params.problemID
        let func = this.$route.name === 'problem-submission' ? 'getProblem' : 'getContestProblem'
        api[func](this.problemID, this.contestID).then(res => {
          this.$Loading.finish()
          let problem = res.data.data
          this.changeDomTitle({title: problem.title})
          api.submissionExists(problem.id).then(res => {
            this.submissionExists = res.data.data
          })
          problem.languages = problem.languages.sort()
          this.problem = problem
          console.log(problem)
          this.changePie(problem)
          // 로컬에 코드가 있고 템플릿을 로드할 필요가 없음을 나타내는 beforeRouteEnter에서 수정됨
          if (this.code !== '') {
            return
          }
          // try to load problem template
          this.language = this.problem.languages[0]
          let template = this.problem.template
          if (template && template[this.language]) {
            this.code = template[this.language]
          }
        }, () => {
          this.$Loading.error()
        })
      },
      changePie (problemData) {
        // 특정 상태일때만 표시
        for (let k in problemData.statistic_info) {
          if (filtedStatus.indexOf(k) === -1) {
            delete problemData.statistic_info[k]
          }
        }
        let acNum = problemData.accepted_number
        let data = [
          {name: 'WA', value: problemData.submission_number - acNum},
          {name: 'AC', value: acNum}
        ]
        this.pie.series[0].data = data
        // 큰 그림의 AC만 선택합니다. 여기서 딥카피를 수행해야 합니다.
        let data2 = JSON.parse(JSON.stringify(data))
        data2[1].selected = true
        this.largePie.series[1].data = data2

        // 결과에 따라 범례를 설정합니다. 제출되지 않은 범례는 표시되지 않습니다.
        let legend = Object.keys(problemData.statistic_info).map(ele => JUDGE_STATUS[ele].short)
        if (legend.length === 0) {
          legend.push('AC', 'WA')
        }
        this.largePie.legend.data = legend

        // ac 데이터를 추출하고 마지막에 넣습니다.
        let acCount = problemData.statistic_info['0']
        delete problemData.statistic_info['0']

        let largePieData = []
        Object.keys(problemData.statistic_info).forEach(ele => {
          largePieData.push({name: JUDGE_STATUS[ele].short, value: problemData.statistic_info[ele]})
        })
        largePieData.push({name: 'AC', value: acCount})
        this.largePie.series[0].data = largePieData
      },
      handleRoute (route) {
        this.$router.push(route).catch(() => {})
      },
      onChangeLang (newLang) {
        if (this.problem.template[newLang]) {
          if (this.code.trim() === '') {
            this.code = this.problem.template[newLang]
          }
        }
        this.language = newLang
      },
      onChangeTheme (newTheme) {
        this.theme = newTheme
      },
      onResetToTemplate () {
        this.$Modal.confirm({
          content: this.$i18n.t('m.Are_you_sure_you_want_to_reset_your_code'),
          onOk: () => {
            let template = this.problem.template
            if (template && template[this.language]) {
              this.code = template[this.language]
            } else {
              this.code = ''
            }
          }
        })
      },
      checkSubmissionStatus () {
        // 일부 문제를 방지하려면 setTimeout을 사용하십시오.
        if (this.refreshStatus) {
          // 이전 제출 상태 확인이 중지되지 않은 경우 중지하십시오. 그렇지 않으면 시간 초과에 대한 참조가 손실되고 무한 요청이 발생합니다.
          clearTimeout(this.refreshStatus)
        }
        const checkStatus = () => {
          let id = this.submissionId
          api.getSubmission(id).then(res => {
            this.result = res.data.data
            if (Object.keys(res.data.data.statistic_info).length !== 0) {
              this.submitting = false
              this.submitted = false
              this.isAfterSubmit = true
              clearTimeout(this.refreshStatus)
              this.init()
            } else {
              this.refreshStatus = setTimeout(checkStatus, 2000)
            }
          }, res => {
            this.submitting = false
            clearTimeout(this.refreshStatus)
          })
        }
        this.refreshStatus = setTimeout(checkStatus, 2000)
      },
      submitCode () {
        if (this.code.trim() === '') {
          this.$error(this.$i18n.t('m.Code_can_not_be_empty'))
          return
        }
        this.submissionId = ''
        this.result = {result: 9}
        this.submitting = true
        let data = {
          problem_id: this.problem.id,
          language: this.language,
          code: this.code,
          contest_id: this.contestID
        }
        if (this.captchaRequired) {
          data.captcha = this.captchaCode
        }
        const submitFunc = (data, detailsVisible) => {
          this.statusVisible = true
          api.submitCode(data).then(res => {
            this.submissionId = res.data.data && res.data.data.submission_id
            this.updateShareSubmission(this.submissionId, this.isActive)
            // 실시간 상태확인
            this.submitting = false
            this.submissionExists = true
            if (!detailsVisible) {
              this.$Modal.success({
                title: this.$i18n.t('m.Success'),
                content: this.$i18n.t('m.Submit_code_successfully')
              })
              return
            }
            this.submitted = true
            this.checkSubmissionStatus()
          }, res => {
            this.getCaptchaSrc()
            if (res.data.data.startsWith('Captcha is required')) {
              this.captchaRequired = true
            }
            this.submitting = false
            this.statusVisible = false
          })
        }

        if (this.contestRuleType === 'OI' && !this.OIContestRealTimePermission) {
          if (this.submissionExists) {
            this.$Modal.confirm({
              title: '',
              content: '<h3>' + this.$i18n.t('m.You_have_submission_in_this_problem_sure_to_cover_it') + '<h3>',
              onOk: () => {
                // 대화 상자와 다음 프롬프트 대화 상자 간의 충돌을 일시적으로 해결합니다(그렇지 않으면 깜박임).
                setTimeout(() => {
                  submitFunc(data, false)
                }, 1000)
              },
              onCancel: () => {
                this.submitting = false
              }
            })
          } else {
            submitFunc(data, false)
          }
        } else {
          submitFunc(data, true)
        }
      },
      updateShareSubmission (submissionId, shared) {
        let data = {id: submissionId, shared: shared}
        api.updateSubmission(data).then(res => {
        }, () => {
          this.$error(this.$i18n.t('m.Error'))
        })
      },
      onCopy (event) {
        this.$success('Code copied')
      },
      onCopyError (e) {
        this.$error('Failed to copy code')
      },
      undoPage () {
        this.$router.push({path: this.lastURL.path}).catch(() => {})
      },
      goHome () {
        this.$router.push('/').catch(() => {})
      },
      goSubmissionList () {
        if (this.contestID) {
          this.$router.push({name: 'contest-submission-list', query: {problemID: this.problemID}}).catch(() => {})
        } else {
          this.$router.push({name: 'submission-list', query: {problemID: this.problemID}}).catch(() => {})
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
      contestEnded () {
        return this.contestStatus === CONTEST_STATUS.ENDED
      },
      submissionStatus () {
        return {
          text: JUDGE_STATUS[this.result.result]['name'],
          color: JUDGE_STATUS[this.result.result]['color']
        }
      },
      submissionRoute () {
        if (this.contestID) {
          return {name: 'contest-submission-list', query: {problemID: this.problemID}}
        } else {
          return {name: 'submission-list', query: {problemID: this.problemID}}
        }
      }
    },
    beforeRouteLeave (to, from, next) {
      // 구성 요소 전환 후 지속적인 요청 방지
      clearInterval(this.refreshStatus)

      this.$store.commit(types.CHANGE_CONTEST_ITEM_VISIBLE, {menu: true})
      storage.set(buildProblemCodeKey(this.problem._id, from.params.contestID), {
        code: this.code,
        language: this.language,
        theme: this.theme
      })
      next()
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

<style lang="less" scoped>
  @import '../../../../styles/common.less';
  .card-title {
    margin-left: 8px;
  }

  .flex-container {
    max-width: calc(~"100vw - 100px");
    margin-left: 50px;
    margin-right: 50px;
    justify-content: flex-start;
    #problem-main {
      flex: auto;
      margin-right: 18px;
    }
    #right-column {
      flex: none;
      width: 220px;
    }
  }
  .flex-container-submit-mode {
    max-width: calc(~"100vw - 100px");
    margin-left: 0px;
    margin-right: 0px;
    justify-content: flex-start;
  }
  #problem-content {
    margin-top: -50px;
    margin-left: 10px;
    .title {
      font-size: 17px;
      font-weight: 400;
      -webkit-text-stroke: .5px;
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
      margin: 0 20px 0 0;
      font-size: 15px;
    }
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
  .split-sapple {
    justify-content: flex-start;
    flex-flow: row wrap;
    -ms-flex-flow: row wrap;
  }
  #submit-code {
    margin-top: 20px;
    margin-bottom: 20px;
    .status {
      position: relative;
      float: left;
      span {
        margin-right: 10px;
        margin-left: 10px;
      }
    }
    .captcha-container {
      display: inline-block;
      .captcha-code {
        width: auto;
        margin-top: -20px;
        margin-left: 20px;
      }
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
  .problem_contents{
    /* width: ; */
    height: 75vh;
    font-size: 16px;
    overflow-y: scroll;
    &::-webkit-scrollbar {
      width: 20px;
      height: 20px;
    }

    &::-webkit-scrollbar-track {
      background-color: transparent;
    }

    &::-webkit-scrollbar-thumb {
      background-color: @dark-white;
      border-radius: 20px;
      border: 6px solid transparent;
      background-clip: content-box;
    }
  }

  .problem_input{
    padding: 0 20px 0 20px;
    background-color: @white;
    height: 100%;
  }

  .input-for-pre {
    min-width: 90px;

  }

  .demo-split {
    height: 87vh;
    margin-left: 0px !important;
    margin-right: 0px !important;
    /* margin: -80px -45px -250px -45px; 
    /* border: 1px solid #dcdee2; */
  }
  .ss_header{
    background: @purple;
    color: @black;
    position: relative;
    display: flex;
    justify-content: space-between;
    left: 0px;
    top: 0px;
    width: 100%;
    height: 60px;
    line-height: 60px;
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);

    .header-left {
      display: flex;
      .problem-name {
        font-size: 120%;
        -webkit-text-stroke: .5px;
        color: @white;
        padding: 0 4px;
      }
    }

    .header-right {
      display: flex;
      
      .hide-btn {
        background-color: @light-purple;
        border-radius: 5px;
        -webkit-text-stroke: .3px;
        &:focus {
          color: @white;
        }
        &:hover {
          background-color: #947dff;
        }
      }
    }

    #undo-icon {
      float: left;
      width: 40px;
      text-align: center;
      line-height: 60px;
      color: @purple;
      * {
        transition: all 0.1s ease-in-out;
      }
      &:hover {
        cursor: pointer;
        color: @purple;
        * {
          color: @purple;
        }
      }
    }
    .logo {
      float: left;
      color: @white;
      font-size: 28px;
      font-weight: 900;
      margin: 0 20px;
      -webkit-text-stroke: 1px;
      &:hover {
        cursor: pointer;
      }
    }
    div {
      line-height: 60px;
    }
  }

  .solve_submit_footer{
    background: rgb(29, 29, 29);
    color: white;
  }

  .footer_title {
    float: left;
    color: white;
    font-size: 18px;
    padding: 0 10px;
  }
  
  .footer_btn{
    float: left;
    color: white;
    /* font-size: 16px; */
    padding: 0 5px;
  }

  .ss_footer {
    background-color: rgb(51, 51, 51);
    position: absolute;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 60px;
    line-height: 60px;
    z-index: 99;
    /* text-align: center; */
  }  

  @media screen and (max-width: 1200px) {
    .demo-split{
      margin: -80px -50px -200px -50px;
    }
  }
  @media screen and (min-width: 1200px) {
    .demo-split{
      margin: -80px -50px -200px -50px;
    }
  }

  .left-split-pane{

    padding: 10px;
    height: 100%;
    background: @white;
  }

  .right-split-pane{
    /* padding: 10px; */
    height: 100%;
    min-width: 600px;
    /* background: forestgreen; */
  }

  .right-split-pane.no-padding{
    height: 100%;
    padding: 0;
  }

  .rtop-split-pane{
    height : 100%;
    padding: 10px;
    background-color: #262626;
  }

  .rbottom-split-pane{
    min-height: 5%;
    height: 100%;
    padding: 10px;
    background-color: #262626;
  }

  .demo-split{
    height: 87vh;
    /* border: 1px solid #dcdee2; */
  }
  .demo-split-pane{
    padding: 10px;
  }
  .demo-split-pane.no-padding{
    height: 90%;
    padding: 0;
  }


  #submit-codes {
    margin-top: 40px;
    margin-bottom: 20px;
  }

  .status {
    float: left;
  }
  
  .status > span {
    margin-right: 10px;
    margin-left: 10px;
  }

  .captcha-containers {
    display: inline-block;
  }
  .blockingdrag {
    -webkit-user-select:none;
    -moz-user-select:none;
    -ms-user-select:none;
    user-select:none
  }
  .captcha-codes {
    width: auto;
    height: 70vh;
    margin-top: -20px;
    margin-left: 20px;
  }

  .fl-rights {
    position: absolute;
    float: right;
  }
  .undo-btn {
    float: right;
    margin: 10px 25px 10px 0;
  }

  .problem-animate-enter-active {
    animation: fadeIn 1s;
  }
  .tag-card {
    & > .ivu-card-body {
      padding-left: 20px;
      padding-right: 20px;
    }
  }
  .help {
    cursor: pointer;
    margin-right: 10px;
    .help-btn {
      font-size: 14px;
      font-weight: 400;
      line-height: 65px;
      color: @white;
      background-color: transparent;
      border-color: transparent;
      transition: all 0.3s ease-in-out;
      &:hover {
        color: @light-purple;
      }
    }
  }
  .hide {
    display: flex;
    cursor: pointer;
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

  .submit-btn {
    background-color: #E05252;
    margin: 0 35px 0 10px;
    color: @white;
    -webkit-text-stroke: .3px;
    &:hover {
      background-color: @red;
      transition: background-color .3s ease-in-out;
    }
  }

  p {
    padding: 0;
    margin: 0;
  }

  .result {
    -webkit-text-stroke: .3px; 
    font-size: 15px;
    border-width: 2px;
  }
  
</style>
