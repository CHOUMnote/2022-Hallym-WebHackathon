<template>
  <!-- <Row type="flex" justify="space-around">
    <Col :span="22"> -->
    <!-- <Panel :padding="10">
      <div slot="title">{{$t('m.ACM_Ranklist')}}</div>
      <div class="echarts">
        <ECharts :options="options" ref="chart" auto-resize></ECharts>
      </div>
    </Panel> -->
    <!-- <Table :data="dataRank" :columns="columns" :loading="loadingTable" size="small"></Table>
    <Pagination :total="total" :page-size.sync="limit" :current.sync="page"
                @on-change="getRankData" show-sizer
                @on-page-size-change="getRankData(1)"></Pagination>
    </Col>
  </Row> -->
  <div class="main">
    <div class="ranking-container">
      <h3>사용자 순위</h3>
      <table class="ranking-list">
        <!-- 제목 -->
        <thead>
          <tr class="ranking_title">
            <td style="width: 20%">순위</td>
            <td style="width: 20%">아이디</td>
            <td style="width: 20%">맞은 문제</td>
            <td style="width: 20%">제출</td>
            <td style="width: 20%">정답 비율</td>
          </tr>
        </thead>
        <!-- 내용 -->
        <tbody v-for="(data, index) in dataRank" @click="goUser(data.user)">
          <tr v-if="index == 0">
            <td  class="image">
              <img class="rankings-img" src="../../../../assets/gold crown.png">
              <span class="no top">1</span>
            </td>
            <td class="name">{{data.user.username}}</td>
            <td>{{data.accepted_number}}</td>
            <td>{{data.submission_number}}</td>
            <td>{{toPercent(data)}}</td>
          </tr>
          <tr v-else-if="index == 1">
            <td class="image">
              <img class="rankings-img" src="../../../../assets/silver crown.png"/>
              <span class="no top">2</span>
            </td>
            <td class="name">{{data.user.username}}</td>
            <td>{{data.accepted_number}}</td>
            <td>{{data.submission_number}}</td>
            <td>{{toPercent(data)}}</td>
          </tr>
          
          <tr v-else-if="index == 2" class="ranker">
            <td class="image">
              <img class="rankings-img" src="../../../../assets/bronse crown.png"/>
              <span class="no top third" style="color: white">3</span>
            </td>
            <td class="name">{{data.user.username}}</td>
            <td>{{data.accepted_number}}</td>
            <td>{{data.submission_number}}</td>
            <td>{{toPercent(data)}}</td>
          </tr>
          <tr v-else-if="index > 2">
            <td class="no"> {{index + 1}} </td>
            <td class="name">{{data.user.username}}</td>
            <td>{{data.accepted_number}}</td>
            <td>{{data.submission_number}}</td>
            <td>{{toPercent(data)}}</td>
          </tr>
        </tbody>
      </table>
      <Pagination :total="total" :page-size.sync="limit" :current.sync="page"
                  @on-change="getRankData" show-sizer
                  @on-page-size-change="getRankData(1)"
                  style="margin: 20px 0 10px; display: flex; justify-content:center; float: none;"></Pagination>
      </div>
  </div>
</template>

<script>
  import api from '@oj/api'
  import Pagination from '@oj/components/Pagination'
  import utils from '@/utils/utils'
  import { RULE_TYPE } from '@/utils/constants'

  export default {
    name: 'acm-rank',
    components: {
      Pagination
    },
    data () {
      return {
        page: 1,
        limit: 100,
        total: 0,
        loadingTable: false,
        dataRank: [],
        columns: [
          {
            title: '순위',
            align: 'center',
            width: 60,
            render: (h, params) => {
              return h('span', {}, params.index + (this.page - 1) * this.limit + 1)
            }
          },
          {
            title: '아이디',
            align: 'center',
            render: (h, params) => {
              return h('a', {
                style: {
                  'display': 'inline-block',
                  'max-width': '200px'
                },
                on: {
                  click: () => {
                    this.$router.push(
                      {
                        name: 'user-home',
                        query: {username: params.row.user.username}
                      }).catch(() => {})
                  }
                }
              }, params.row.user.username)
            }
          },
          {
            title: this.$i18n.t('m.mood'),
            align: 'center',
            key: 'mood'
          },
          {
            title: '맞은 문제',
            align: 'center',
            key: 'accepted_number'
          },
          {
            title: '제출',
            align: 'center',
            key: 'submission_number'
          },
          {
            title: this.$i18n.t('m.Rating'),
            align: 'center',
            render: (h, params) => {
              return h('span', utils.getACRate(params.row.accepted_of_all_submission_number, params.row.submission_number))
            }
          }
        ],
        options: {
          tooltip: {
            trigger: 'axis'
          },
          legend: {
            data: [this.$i18n.t('m.AC'), this.$i18n.t('m.Total')]
          },
          grid: {
            x: '3%',
            x2: '3%'
          },
          toolbox: {
            show: true,
            feature: {
              dataView: {show: true, readOnly: true},
              magicType: {show: true, type: ['line', 'bar', 'stack']},
              saveAsImage: {show: true}
            },
            right: '10%'
          },
          calculable: true,
          xAxis: [
            {
              type: 'category',
              data: ['root'],
              axisLabel: {
                interval: 0,
                showMinLabel: true,
                showMaxLabel: true,
                align: 'center',
                formatter: (value, index) => {
                  return utils.breakLongWords(value, 10)
                }
              }
            }
          ],
          yAxis: [
            {
              type: 'value'
            }
          ],
          series: [
            {
              name: this.$i18n.t('m.AC'),
              type: 'bar',
              data: [0],
              markPoint: {
                data: [
                  {type: 'max', name: 'max'}
                ]
              }
            },
            {
              name: this.$i18n.t('m.Total'),
              type: 'bar',
              data: [0],
              markPoint: {
                data: [
                  {type: 'max', name: 'max'}
                ]
              }
            }
          ]
        }
      }
    },
    mounted () {
      this.getRankData(1)
    },
    methods: {
      getRankData (page) {
        let offset = (page - 1) * this.limit
        // let bar = this.$refs.chart
        // bar.showLoading({maskColor: 'rgba(250, 250, 250, 0.8)'})
        this.loadingTable = true
        api.getUserRank(offset, this.limit, RULE_TYPE.ACM).then(res => {
          this.loadingTable = false
          if (page === 1) {
            this.changeCharts(res.data.data.results.slice(0, 10))
          }
          this.total = res.data.data.total
          this.dataRank = res.data.data.results
          // bar.hideLoading()
        }).catch(() => {
          this.loadingTable = false
          // bar.hideLoading()
        })
      },
      changeCharts (rankData) {
        let [usernames, acData, totalData] = [[], [], []]
        rankData.forEach(ele => {
          usernames.push(ele.user.username)
          acData.push(ele.accepted_number)
          totalData.push(ele.submission_number)
        })
        this.options.xAxis[0].data = usernames
        this.options.series[0].data = acData
        this.options.series[1].data = totalData
      },
      goUser (user) {
        this.$router.push({
          name: 'user-home',
          query: {username: user.username}
        }).catch(() => {})
      },
      toPercent (rank) {
        return utils.getACRate(rank.accepted_of_all_submission_number, rank.submission_number)
      }
    }
  }
</script>

<style scoped lang="less">
@import '../../../../styles/common.less';
  h3 {
    font-size: @font-medium;
    text-align: left;
    margin-bottom: 20px;
    color: @default-font-color;
  }

  .main {
    margin: auto;
    padding: 30px 20px;
    background-color: @white;
    border-radius: 5px;
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);
    text-align: center;
    width: 95vw;
  }
  .ranking-container {
    width: 75vw;
    margin: auto;
  }
  .ranking-list {
    -webkit-text-stroke: .5px;
    border-collapse: collapse;
    width: 100% !important; 
    table-layout: fixed;
    text-align: center;
    padding: 8px;
    margin: auto;
    thead {
      border-bottom: 1px solid #c4c4c4;
      color: @gray;
      background-color: @light-gray;
    }
    td {
      padding: 8px;
    }
    th {
      padding: 8px;
    }
    tbody {
      color: @black;
      -webkit-text-stroke: .3px;
      height: 60px;
      font-size: @font-micro;
      tr {
        cursor: pointer;
      }
      &:hover {
        .name {
          color: @orange;
          transition: color .3s ease-in-out;
        }
      }

      .image {
        position: relative;
        img {
          width: 30px;
          height: 30px;
        }
        .top {
          position:absolute;
          transform: translate( -50%, -50% );
          top: 55%;
          left: 50%;
          color: @black;
          -webkit-text-stroke: .5px;
        }
        .third {
          color: @white;
        }
      }
    }
  }
</style>