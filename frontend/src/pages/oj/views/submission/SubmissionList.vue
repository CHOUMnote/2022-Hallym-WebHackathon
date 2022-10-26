<template>
  <div class="flex-container">
    <div id="main">
      <Panel shadow style="min-width: 500px;">
        <div slot="title">제출 현황</div>
        <!-- <div slot="title">{{title}}</div> -->
        <div slot="extra">
          <ul class="filter">
            <li>
              <Dropdown @on-click="handleResultChange">
                <span>{{status}}
                  <!-- <Icon type="arrow-down-b"></Icon> -->
                  <Icon type="md-arrow-dropdown" />
                </span>
                <Dropdown-menu slot="list">
                  <Dropdown-item name="">{{$t('m.All')}}</Dropdown-item>
                  <Dropdown-item v-for="status in Object.keys(JUDGE_STATUS)" :key="status" :name="status">
                    {{$t('m.' + JUDGE_STATUS[status].name.replace(/ /g, "_"))}}
                  </Dropdown-item>
                </Dropdown-menu>
              </Dropdown>
            </li>


            <li>
              <i-switch size="large" v-model="formFilter.myself" @on-change="handleQueryChange">
                <span slot="open">{{$t('m.Mine')}}</span>
                <span slot="close">{{$t('m.All')}}</span>
              </i-switch>
            </li>
            <li>
              <Input v-model="formFilter.username" placeholder="검색할 아이디를 입력하세요" @on-enter="handleQueryChange"/>
              <!-- <Input v-model="formFilter.username" :placeholder="$t('m.Search_Author')" @on-enter="handleQueryChange"/> -->
            </li>

            <!-- <li>
              <Button type="info" icon="md-refresh" @click="getSubmissions">{{$t('m.Refresh')}}</Button>
            </li> -->
          </ul>
        </div>
        <!-- <Table stripe :disabled-hover="true" :columns="columns" :data="submissions" :key="renderKey" :loading="loadingTable" size="small"></Table> -->
        <div class="submission-container">
          <table v-if="!getRejudgeAccess" class="submission-list">
            <thead>
              <tr>
                <th style="width:20%">아이디</th>
                <th style="width:20%">문제 번호</th>
                <th style="width:15%">채점 결과</th>
                <th style="width:10%">시간</th>
                <th style="width:10%">메모리</th>
                <th style="width:10%">언어</th>
                <th style="width:15%">제출일</th>
              </tr>
            </thead>
            <tbody v-for="submission in submissions">
              <tr>
                <td id="user-id" @click="redirectToUser(submission)">{{ submission.username }}</td>
                <td id="problem-id" @click="redirectToProblem(submission)">{{ submission.problem }}</td>
                <td><Tag :color=toColor(submission) :checkable="checkIfAvailable(submission)" v-bind:style="[checkIfAvailable(submission) ? {'cursor' : 'pointer'}:{'cursor' : 'default'}]" @on-change="redirectToDetails(submission)"> {{ toResult(submission) }} </Tag></td>
                <td>{{ toTime(submission) }}</td>
                <td>{{ toMemory(submission) }}</td>
                <td>{{ submission.language }}</td>
                <td>{{ toDate(submission) }}</td>
              </tr>
            </tbody>
          </table>
          <table v-else class="submission-list">
            <thead>
              <tr>
                <th style="width:15%">아이디</th>
                <th style="width:15%">문제 번호</th>
                <th style="width:15%">채점 결과</th>
                <th style="width:10%">시간</th>
                <th style="width:10%">메모리</th>
                <th style="width:10%">언어</th>
                <th style="width:15%">제출일</th>
                <th style="width:10%; text-align: center;">재체점</th>
              </tr>
            </thead>
            <tbody v-for="(submission, idx) in submissions">
              <tr>
                <td id="user-id" @click="redirectToUser(submission)">{{ submission.username }}</td>
                <td id="problem-id" @click="redirectToProblem(submission)">{{ submission.problem }}</td>
                <td><Tag :color=toColor(submission) :checkable="checkIfAvailable(submission)" v-bind:style="[checkIfAvailable(submission) ? {'cursor' : 'pointer'}:{'cursor' : 'default'}]" @on-change="redirectToDetails(submission)"> {{ toResult(submission) }} </Tag></td>
                <td>{{ toTime(submission) }}</td>
                <td>{{ toMemory(submission) }}</td>
                <td>{{ submission.language }}</td>
                <td>{{ toDate(submission) }}</td>
                <td style="text-align: center;"><Icon type="md-refresh" size="18" class="icon-hv" @click="handleRejudge(submission.id, idx)"></Icon></td>
              </tr>
            </tbody>
          </table>
        </div>
        <Pagination :total="total" :page-size="limit" @on-change="changeRoute" :current.sync="page" style="margin: 20px 0 10px; display: flex; justify-content: center; float: none;"></Pagination>
      </Panel>
    </div>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import { JUDGE_STATUS, USER_TYPE } from '@/utils/constants'
  import utils from '@/utils/utils'
  import time from '@/utils/time'
  import Pagination from '@/pages/oj/components/Pagination'

  export default {
    name: 'submissionList',
    components: {
      Pagination
    },
    data () {
      return {
        renderKey: 0,
        formFilter: {
          myself: false,
          result: '',
          username: ''
        },
        loadingTable: false,
        submissions: [],
        total: 30,
        limit: 25,
        page: 1,
        contestID: '',
        problemID: '',
        routeName: '',
        JUDGE_STATUS: '',
        rejudge_column: false,
        refreshStatus: null
      }
    },
    mounted () {
      this.init()
      this.JUDGE_STATUS = Object.assign({}, JUDGE_STATUS)
      // 去除submitting的状态 和 两个
      delete this.JUDGE_STATUS['9']
      delete this.JUDGE_STATUS['2']
    },
    methods: {
      init () {
        clearTimeout(this.refreshStatus)
        this.contestID = this.$route.params.contestID
        let query = this.$route.query
        this.problemID = query.problemID
        this.formFilter.myself = query.myself === '1'
        this.formFilter.result = query.result || ''
        this.formFilter.username = query.username || ''
        this.page = parseInt(query.page) || 1
        if (this.page < 1) {
          this.page = 1
        }
        this.routeName = this.$route.name
        this.getSubmissions()
        this.getRejudgeAccess()
      },
      buildQuery () {
        return {
          myself: this.formFilter.myself === true ? '1' : '0',
          result: this.formFilter.result,
          username: this.formFilter.username,
          page: this.page
        }
      },
      getSubmissions () {
        let params = this.buildQuery()
        params.contest_id = this.contestID
        params.problem_id = this.problemID
        let offset = (this.page - 1) * this.limit
        let func = this.contestID ? 'getContestSubmissionList' : 'getSubmissionList'
        this.loadingTable = true
        api[func](offset, this.limit, params).then(res => {
          let data = res.data.data
          for (let v of data.results) {
            v.loading = false
          }
          this.adjustRejudgeColumn()
          this.loadingTable = false
          this.submissions = data.results
          try {
            // settimeout api call router 변경시 exception 추출
            for (let idx = 0; this.submissions.length; idx++) {
              this.getRealtimeStatus(this.submissions[idx].id, idx)
            }
          } catch (e) { }
          this.total = data.total
        }).catch(() => {
          this.loadingTable = false
          clearTimeout(this.refreshStatus)
        })
      },
      forceRender () {
        this.renderKey += 1
      },
      getRejudgeAccess () {
        if (!this.rejudgeColumnVisible || this.rejudge_column) {
          return false
        } else {
          return true
        }
      },
      getRealtimeStatus (id, index) {
        if (id === undefined) {
          clearTimeout(this.refreshSatus)
        }
        if (this.refreshSatus) {
          clearTimeout(this.refreshSatus)
          return
        }
        if (this.submissions.length === 0) {
          clearTimeout(this.refreshStatus)
        }
        const checkStatus = () => {
          api.getSubmissionStatus(id).then(__ => {
            if (this.submissions[index] === undefined || this.submissions[index].result === undefined) {
              clearTimeout(this.refreshStatus)
            } else if (this.submissions[index].id !== __.data.data.id) {
              clearTimeout(this.refreshStatus)
            } else {
              api.getSafeSubmissionStatus(id).then(res => {
                if (res.data.data.result === undefined) {
                  clearTimeout(this.refreshStatus)
                } else if (this.submissions[index] === undefined) {
                  clearTimeout(this.refreshStatus)
                } else {
                  if (this.submissions[index].id !== res.data.data.id) {
                    clearTimeout(this.refreshStatus)
                  } else {
                    this.submissions[index].result = res.data.data.result
                    this.submissions[index].username = res.data.data.username
                    this.submissions[index].statistic_info = res.data.data.statistic_info
                    if (this.submissions[index].result === '7' || this.submissions[index].result === 7) {
                      this.refreshStatus = setTimeout(checkStatus, 1000)
                    } else {
                      this.refreshStatus = setTimeout(checkStatus, 1000)
                    }
                  }
                }
              }, ___ => {
                clearTimeout(this.refreshStatus)
              })
            }
          }, _ => {
            clearTimeout(this.refreshStatus)
          })
        }
        this.refreshStatus = setTimeout(checkStatus, 1000)
      },
      changeRoute () {
        clearTimeout(this.refreshStatus)
        let query = utils.filterEmptyValue(this.buildQuery())
        query.contestID = this.contestID
        query.problemID = this.problemID
        let routeName = query.contestID ? 'contest-submission-list' : 'submission-list'
        this.$router.push({
          name: routeName,
          query: utils.filterEmptyValue(query)
        }).catch(() => {})
      },
      checkIfAvailable (submission) {
        if (submission.show_link) {
          return true
        } else {
          return false
        }
      },
      goRoute (route) {
        this.$router.push(route).catch(() => {})
      },
      toTime (submission) {
        return utils.submissionTimeFormat(submission.statistic_info.time_cost)
      },
      toMemory (submission) {
        return utils.submissionMemoryFormat(submission.statistic_info.memory_cost)
      },
      toDate (submission) {
        return time.utcToLocal(submission.create_time)
      },
      toColor (submission) {
        return JUDGE_STATUS[submission.result].color
      },
      toResult (submission) {
        return this.$i18n.t('m.' + JUDGE_STATUS[submission.result].name.replace(/ /g, '_'))
      },
      adjustRejudgeColumn () {
        if (!this.rejudgeColumnVisible || this.rejudge_column) {
          return
        }
        this.rejudge_column = true
      },
      handleResultChange (status) {
        this.page = 1
        this.formFilter.result = status
        this.changeRoute()
      },
      handleQueryChange () {
        this.page = 1
        this.changeRoute()
      },
      handleRejudge (id, index) {
        this.submissions[index].loading = true
        api.submissionRejudge(id).then(async () => {
          this.submissions[index].loading = false
        }, () => {
          this.submissions[index].loading = false
        })
      },
      redirectToProblem (submission) {
        if (this.contestID) {
          this.$router.push(
            {
              name: 'contest-problem-details',
              params: {problemID: submission.problem, contestID: this.contestID}
            }).catch(() => {})
        } else {
          this.$router.push({name: 'problem-details', params: {problemID: submission.problem}}).catch(() => {})
        }
      },
      redirectToDetails (submission) {
        if (submission.show_link) {
          this.$router.push('/status/' + submission.id).catch(() => {})
        }
      },
      redirectToUser (submission) {
        this.$router.push(
          {
            name: 'user-home',
            query: {username: submission.username}
          }).catch(() => {})
      }
    },
    computed: {
      ...mapGetters(['isAuthenticated', 'user']),
      title () {
        if (!this.contestID) {
          return this.$i18n.t('m.Status')
        } else if (this.problemID) {
          return '제출 현황'
        } else {
          return this.$i18n.t('m.Submissions')
        }
      },
      status () {
        return this.formFilter.result === '' ? this.$i18n.t('m.Status') : this.$i18n.t('m.' + JUDGE_STATUS[this.formFilter.result].name.replace(/ /g, '_'))
      },
      rejudgeColumnVisible () {
        return !this.contestID && this.user.admin_type === USER_TYPE.SUPER_ADMIN
      }
    },
    beforeRouteLeave (to, from, next) {
      // 구성 요소 전환 후 지속적인 요청 방지
      clearTimeout(this.refreshStatus)
      next()
    },
    unmounted () {
      clearTimeout(this.refreshStatus)
    },
    beforeDestroy () {
      if (this.refreshStatus) {
        clearTimeout(this.refreshStatus)
      }
    },
    watch: {
      '$route' (newVal, oldVal) {
        if (newVal !== oldVal) {
          clearTimeout(this.refreshStatus)
          this.init()
        }
      },
      'rejudgeColumnVisible' () {
        this.adjustRejudgeColumn()
      },
      'isAuthenticated' () {
        this.init()
      }
    }
  }
</script>

<style scoped lang="less">
  @import '../../../../styles/common.less';
  
  .ivu-btn-text {
    color: @purple;
  }

  .ivu-card {
    padding: 0 15px 15px 15px;
    margin: 0 25px;
  }
  .submission-container {
    margin-top: 20px;
    padding: 0 20px;
  }
  .submission-list {
    border-collapse: collapse;
    width: 100% !important; 
    table-layout: fixed;
    text-align: left;
    padding: 8px;
    font-size: 12px;
    margin: auto;
    td {
      padding: 8px;
      border-bottom: 1px solid @light-gray;
    }
    th {
      border-bottom: 1px solid #c4c4c4;
      padding: 8px;
    }

    tbody {
      color: @gray;
      -webkit-text-stroke: .3px;

      #problem-id:hover, #user-id:hover {
        cursor: pointer;
        transition: color .2s ease-in;
        color: @purple;
        font-weight: 500;
      }
    }
  }
  .icon-hv {
      transition: all 0;
      cursor: pointer;
      color: @gray;
    &:hover {
      transition: all 0.3s;
      -webkit-transform: rotate(360deg);
      -moz-transform: rotate(360deg);
      -ms-transform: rotate(360deg);
      -o-transform: rotate(360deg);
      transform: rotate(360deg);
      color: @dark-purple;
    }
  }
  @media screen and (max-width : 900px) {
    #main {
      .ivu-card .ivu-card-dis-hover .ivu-card-shadow {
        min-width: 550px;
      }
    }
    
  }
</style>
