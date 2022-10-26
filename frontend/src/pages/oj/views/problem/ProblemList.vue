<template>
  <div>
    <div slot="extra">
      <div class="category-name" v-bind:style="[typeof this.$route.query.category === 'undefined' ? {'display' : 'none'}:{}]">
        <Button id="back-button" icon="md-arrow-back" size="large" onclick="history.back()" type="text"></Button>
        {{ categoryName() }} </div>
      <div class="category" v-bind:style="[typeof this.$route.query.category !== 'undefined' ? {'display' : 'none'}:{}]" >
        <div class="title" @click="goCategoryList">문제 카테고리</div>
        <div class="box_container">
          <div class="item_box">
            <div class="item" v-for="category in problemCategoryList" :key="category.title" @click="goProblemList(category.id, category.title)">
            <h3>{{ category.title }}</h3>
            <!-- <Icon color="#858585" type="ios-arrow-forward" /> -->
            <div class="description" v-katex v-html="category.description"></div>
            <div class="progress">
              <p class="percent">달성률: {{ category.percent }}%</p>
              <progress max="100" :value="category.percent"></progress>
            </div>
            <!-- <div class="progress"><Progress :percent="category.percent" /></div> -->
            </div>
          </div>
        </div>
      </div>
      <div class="main-list">
        <div class="left-menu">
          <div class="top-menu" v-bind:style="[typeof this.$route.query.category !== 'undefined' ? {'display' : 'none'}:{}]">
            <div>
              <div class="search-bar">
                <Input @on-search="filterByKeyword" v-model="query.keyword" search placeholder="검색어를 입력하세요."></Input>
              </div>
              <div class="filter-difficulty">
                <Dropdown @on-click="filterByDifficulty" trigger="click">
                  <span>{{query.difficulty === '' ? this.$i18n.t('m.Difficulty') : this.$i18n.t('m.' + query.difficulty)}}
                    <Icon type="arrow-down-b"></Icon> 
                    <Icon type="md-arrow-dropdown" />
                  </span>
                  <Dropdown-menu slot="list">
                    <Dropdown-item name="">{{$t('m.All')}}</Dropdown-item>
                    <Dropdown-item class="green" name="Level1">Level 1</Dropdown-item>
                    <Dropdown-item class="green" name="Level2">Level 2</Dropdown-item>
                    <Dropdown-item class="green" name="Level3">Level 3</Dropdown-item>
                    <Dropdown-item class="green" name="Level4">Level 4</Dropdown-item>
                    <Dropdown-item class="green" name="Level5">Level 5</Dropdown-item>

                    <Dropdown-item class="orange" name="Level6">Level 6</Dropdown-item>
                    <Dropdown-item class="orange" name="Level7">Level 7</Dropdown-item>
                    <Dropdown-item class="orange" name="Level8">Level 8</Dropdown-item>
                    <Dropdown-item class="orange" name="Level9">Level 9</Dropdown-item>
                    <Dropdown-item class="orange" name="Level10">Level 10</Dropdown-item>

                    <Dropdown-item class="red" name="Level11">Level 11</Dropdown-item>
                    <Dropdown-item class="red" name="Level11">Level 12</Dropdown-item>
                    <Dropdown-item class="red" name="Level11">Level 13</Dropdown-item>
                    <Dropdown-item class="red" name="Level11">Level 14</Dropdown-item>
                    <Dropdown-item class="red" name="Level11">Level 15</Dropdown-item>
                  </Dropdown-menu>
                </Dropdown>
              </div>
                                  <!-- <li>
                                    <i-switch size="large" @on-change="handleTagsVisible">
                                      <span slot="open">{{$t('m.Tags')}}</span>
                                      <span slot="close">{{$t('m.Tags')}}</span>
                                    </i-switch>
                                  </li> -->
            </div>
            <div class="pick-random">
              <Button long id="pick-one" @click="pickone" type="primary">
                <Icon type="ios-shuffle" size="15" />
                랜덤 선택
                <!-- {{$t('m.Pick_One')}} -->
              </Button>
            </div>
          </div>
          <table class="problem-list">
            <thead>
              <tr>
                <th style="width:17%">문제 번호</th>
                <th style="width:40%">제목</th>
                <th style="width:13%">난이도</th>
                <th style="width:15%">제출</th>
                <th style="width:15%">정답 비율</th>
              </tr>
            </thead>
            <tbody v-for="problem in problemList">
              <tr>
                <td id="problem-id">{{ problem._id }}</td>
                <td id="problem-title" @click="redirectToProblem(problem)">{{ problem.title }}</td>
                <td :class="[(problem.difficulty === 'Level1' || problem.difficulty === 'Level2' || 
                              problem.difficulty === 'Level3' || problem.difficulty === 'Level4' || 
                              problem.difficulty === 'Level5' ? 'green' : ''), 
                    (problem.difficulty === 'Level6' || problem.difficulty === 'Level7' ||
                    problem.difficulty === 'Level8' || problem.difficulty === 'Level9' ||
                    problem.difficulty === 'Level10' ? 'orange' : ''),
                    (problem.difficulty === 'Level11' || problem.difficulty === 'Level12' ||
                    problem.difficulty === 'Level13' || problem.difficulty === 'Level14' ||
                    problem.difficulty === 'Level15' ? 'red' : '')]">
                    {{$t('m.' + problem.difficulty)}}
                </td>
                <td>{{ problem.submission_number }}</td>
                <td> {{ convertToACRate(problem) }}</td>
              </tr>
            </tbody>
          </table>
          <Pagination
          :total="total" 
          :page-size.sync="query.limit" 
          @on-change="pushRouter" 
          @on-page-size-change="pushRouter" 
          :current.sync="query.page" 
          :show-sizer="true"
          style="display: flex; justify-content:flex-end; margin: 10px 0 0 0"></Pagination>
        </div>
        <div class="right-menu" v-bind:style="[typeof this.$route.query.category !== 'undefined' ? {'display' : 'none'}:{}]">
          <div slot="title" class="taglist-title">{{$t('m.Tags')}}</div>
          <Button v-for="tag in tagList"
              :key="tag.name"
              @click="filterByTag(tag.name)"
              :disabled="query.tag === tag.name"
              shape="circle"
              class="tag-btn">{{tag.name}}
          </Button>
        </div>
      </div>
    </div>
  </div>
  <!-- <Row type="flex" :gutter="18" style="margin-left:50px; margin-right:50px">
    <Col :span="19">
      <Panel shadow>
        <div slot="title">{{$t('m.Problem_List')}}</div>
        <div slot="extra">
          <ul class="filter">
            <li>
              <Dropdown @on-click="filterByDifficulty">
                <span>{{query.difficulty === '' ? this.$i18n.t('m.Difficulty') : this.$i18n.t('m.' + query.difficulty)}}
                 <Icon type="arrow-down-b"></Icon> 
                  <Icon type="md-arrow-dropdown" />
                </span>
                <Dropdown-menu slot="list">
                  <Dropdown-item name="">{{$t('m.All')}}</Dropdown-item>
                  <Dropdown-item name="Low">{{$t('m.Low')}}</Dropdown-item>
                  <Dropdown-item name="Mid" >{{$t('m.Mid')}}</Dropdown-item>
                  <Dropdown-item name="High">{{$t('m.High')}}</Dropdown-item>
                </Dropdown-menu>
              </Dropdown>
            </li> -->
                                <!-- <li>
                                  <i-switch size="large" @on-change="handleTagsVisible">
                                    <span slot="open">{{$t('m.Tags')}}</span>
                                    <span slot="close">{{$t('m.Tags')}}</span>
                                  </i-switch>
                                </li> -->
            <!-- <li>
              <Input v-model="query.keyword"
                   @on-enter="filterByKeyword"
                   @on-click="filterByKeyword"
                   placeholder="keyword"
                   icon="ios-search-strong"/>
            </li>
            <li>
              <Button type="info" @click="onReset">
                <Icon type="refresh"></Icon>
                {{$t('m.Reset')}}
              </Button>
            </li>
          </ul>
        </div>
        <Table style="width: 100%; font-size: 16px;"
             :columns="problemTableColumns"
             :data="problemList"
             :loading="loadings.table"
             disabled-hover>
        </Table>
      </Panel>
      <Pagination
          :total="total" :page-size.sync="query.limit" @on-change="pushRouter" @on-page-size-change="pushRouter" :current.sync="query.page" :show-sizer="true"></Pagination>

    </Col> -->

    <!-- <Col :span="5">
      <Panel :padding="10">
        <div slot="title" class="taglist-title">{{$t('m.Tags')}}</div>
        <Button v-for="tag in tagList"
            :key="tag.name"
            @click="filterByTag(tag.name)"
            :disabled="query.tag === tag.name"
            shape="circle"
            class="tag-btn">{{tag.name}}
        </Button>
        <Button long id="pick-one" @click="pickone">
          <Icon type="shuffle"></Icon>
          {{$t('m.Pick_One')}}
        </Button>
      </Panel>
      <Spin v-if="loadings.tag" fix size="large"></Spin>
    </Col>
  </Row>-->
</template>

<script>
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import utils from '@/utils/utils'
  import { ProblemMixin } from '@oj/components/mixins'
  import Pagination from '@oj/components/Pagination'

  export default {
    name: 'ProblemList',
    mixins: [ProblemMixin],
    components: {
      Pagination
    },
    data () {
      return {
        problemCategoryList: {},
        tagList: [],
        problemTableColumns: [
          {
            title: '문제 번호',
            key: '_id',
            align: 'center',
            width: 120,
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  click: () => {
                    this.$router.push({name: 'problem-details', params: {problemID: params.row._id}}).catch(() => {})
                  }
                },
                style: {
                  padding: '2px 0'
                }
              }, params.row._id)
            }
          },
          {
            title: this.$i18n.t('m.Title'),
            minWidth: 300,
            align: 'center',
            render: (h, params) => {
              return h('Button', {
                props: {
                  type: 'text',
                  size: 'large'
                },
                on: {
                  click: () => {
                    this.$router.push({name: 'problem-details', params: {problemID: params.row._id}}).catch(() => {})
                  }
                },
                style: {
                  padding: '2px 0',
                  margin: '0 10px',
                  overflowX: 'auto',
                  textAlign: 'left',
                  width: '100%'
                }
              }, params.row.title)
            }
          },
          {
            title: this.$i18n.t('m.Level'),
            align: 'center',
            minWidth: 85,
            render: (h, params) => {
              let t = params.row.difficulty
              let color = 'blue'
              if (t === 'Low') color = 'green'
              else if (t === 'High') color = 'yellow'
              return h('Tag', {
                props: {
                  color: color
                }
              }, this.$i18n.t('m.' + params.row.difficulty))
            }
          },
          {
            title: '제출',
            minWidth: 85,
            align: 'center',
            key: 'submission_number'
          },
          {
            title: '정답 비율',
            minWidth: 85,
            align: 'center',
            render: (h, params) => {
              return h('span', this.getACRate(params.row.accepted_number, params.row.submission_number))
            }
          }
        ],
        problemList: [],
        limit: 20,
        total: 0,
        loadings: {
          table: true,
          tag: true
        },
        routeName: '',
        query: {
          keyword: '',
          difficulty: '',
          tag: '',
          category: '',
          page: 1,
          limit: 10
        },
        formFilter: { // 카테고리를 불러올 때 필터 설정용 데이터
          search: '', // 카테고리 검색 시 검색할 내용
          searchtype: '' // 카테고리 검색 시 검색할 카테고리 - 전체 = 0, 제목 = 1, 댓글 = 2
        }
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init (simulate = false) {
        this.routeName = this.$route.name
        let query = this.$route.query
        this.query.difficulty = query.difficulty || ''
        this.query.keyword = query.keyword || ''
        this.query.tag = query.tag || ''
        this.query.page = parseInt(query.page) || 1
        this.query.category = query.category || ''
        if (this.query.page < 1) {
          this.query.page = 1
        }
        this.query.limit = parseInt(query.limit) || 10
        if (!simulate) {
          this.getTagList()
        }
        this.getProblemList()
        let params = this.buildQuery()
        let offset = (this.page - 1) * this.limit
        api.getProblemCategoryList(offset, this.limit, params).then(res => {
          this.problemCategoryList = res.data.data.result
        })
      },
      pushRouter () {
        this.$router.push({
          name: 'problem-list',
          query: utils.filterEmptyValue(this.query)
        }).catch(() => {})
      },
      buildQuery () { // 쿼리로 설정한 필터값을 전송용 데이터로 빌드
        return {
          page: this.page,
          search: this.formFilter.search,
          searchtype: this.formFilter.searchtype
        }
      },
      categoryName () {
        return this.$route.query.title
      },
      getProblemList () {
        let offset = (this.query.page - 1) * this.query.limit
        this.loadings.table = true
        api.getProblemList(offset, this.limit, this.query).then(res => {
          this.loadings.table = false
          this.total = res.data.data.total
          this.problemList = res.data.data.results
        }, res => {
          this.loadings.table = false
        })
      },
      getTagList () {
        api.getProblemTagList().then(res => {
          this.tagList = res.data.data
          this.loadings.tag = false
        }, res => {
          this.loadings.tag = false
        })
      },
      goProblemList (id, title) {
        let query = {
          keyword: '',
          difficulty: '',
          tag: '',
          category: id,
          title: title,
          page: 1,
          limit: 10
        }
        this.$router.push({
          name: 'problem-list',
          query: utils.filterEmptyValue(query)
        }).catch(() => {})
      },
      goCategoryList () {
        this.$router.push({path: 'category-list'}).catch(() => {})
      },
      filterByTag (tagName) {
        this.query.tag = tagName
        this.query.page = 1
        this.pushRouter()
      },
      filterByDifficulty (difficulty) {
        this.query.difficulty = difficulty
        this.query.page = 1
        this.pushRouter()
      },
      filterByKeyword () {
        this.query.page = 1
        this.pushRouter()
      },
      handleTagsVisible (value) {
        if (value) {
          this.problemTableColumns.push(
            {
              title: this.$i18n.t('m.Tags'),
              align: 'center',
              render: (h, params) => {
                let tags = []
                params.row.tags.forEach(tag => {
                  tags.push(h('Tag', {}, tag))
                })
                return h('div', {
                  style: {
                    margin: '8px 0'
                  }
                }, tags)
              }
            })
        } else {
          this.problemTableColumns.splice(this.problemTableColumns.length - 1, 1)
        }
      },
      onReset () {
        this.$router.push({name: 'problem-list'}).catch(() => {})
      },
      pickone () {
        api.pickone().then(res => {
          this.$success('Good Luck')
          this.$router.push({name: 'problem-details', params: {problemID: res.data.data}}).catch(() => {})
        })
      },
      redirectToProblem (problem) {
        this.$router.push({name: 'problem-details', params: {problemID: problem._id}}).catch(() => {})
      },
      convertToACRate (item) {
        return this.getACRate(item.accepted_number, item.submission_number)
      }
    },
    computed: {
      ...mapGetters(['isAuthenticated'])
    },
    watch: {
      '$route' (newVal, oldVal) {
        if (newVal !== oldVal) {
          this.init(true)
        }
      },
      'isAuthenticated' (newVal) {
        if (newVal === true) {
          this.init()
        }
      }
    }
  }
</script>

<style scoped lang="less">
  @import '../../../../styles/common.less';
  .main-list {
    display: flex;
    margin: 15px;
    .left-menu {
      display: flex;
      flex-direction: column;
      padding: 15px 15px 0 15px;
      .top-menu {
        display: flex;
        flex-direction: row;
        justify-content: space-between;
        div:first-child {
          display: flex;
          justify-content:start;
          .search-bar {
            margin-right: 15px;
            
          }
          .filter-difficulty {
            line-height: 30px;
            background-color: @light-gray;
            border-radius: 4px;
            padding-top: 1px;
            padding-left: 7px;
            padding-right: 7px;
            &:hover {
              background-color: #e8e8e8;
              transition: background-color .3s ease-in-out;
            }
          }
        }
      }
    }
    .right-menu {
      padding: 15px;
      margin-right: 15px;
      border-radius: 4px;
      min-width: 200px;
      box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);
      .taglist-title {
        line-height: 30px;
        font-size: 20px;
        margin-bottom: 10px;
      }

      .tag-btn {
        margin-right: 10px;
        margin-bottom: 10px;
      }
    }
  }
  // .right-menu {
  //   float: right;
  // }
  .problem-list {
    border-collapse: collapse;
    width: 100% !important; 
    table-layout: fixed;
    text-align: left;
    margin: auto;
    td {
      padding: 8px;
    }
    th {
      border-bottom: 1px solid #c4c4c4;
      padding: 8px;
    }

    tbody {
      color: @gray;
      -webkit-text-stroke: .3px;
      &:nth-child(even){
        background-color: #f5f5f5;
      }

      &:hover {
        #problem-title {
          cursor: pointer;
          transition: color .2s ease-in;
          color: @purple;
          font-weight: 500;
        }
      }
    }
  }

  .green {
    color: @green;
  } 
  .orange {
    color: @dark-orange;
  }
  .red {
    color: @red;
  }
  .progress{
    display: absolute;
    bottom: 0;
  }

  .category-name {
    font-size: 30px;
    -webkit-text-stroke: 1px;
    margin: 0 30px;
  }

  .category{
    margin: 30px;
    //background-color: @white;
    border-radius: @size-border-radius;
    box-shadow: 0 1px 5px 0 rgba(0, 0, 0, 0.1);
    .title {
      background-color: @dark-orange;
      border-radius: 5px 5px 0 0;
      padding: 10px;
      color: @white;
      font-size: 16px;
      text-align: center;
      font-weight: @weight-bold;
      cursor: pointer;
      &:hover {
        text-decoration: underline;
      }
    }
  }


  .box_container {
    padding: 0px 30px;
  }

  .item_box{
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
    //white-space: nowrap;
    align-content: flex-start;
    margin-top: 20px;
    padding: 0 0 10px 0;
    &::-webkit-scrollbar {
      height: 12px;
      background-color: transparent;
      width: 15px;
    }
    &::-webkit-scrollbar-thumb {
      background-color: @gray;
      border-radius: 25px;
    }
    &::-webkit-scrollbar-track {
      background-color: @light-gray;
      border-radius: 25px;
    }
    .item{
    position: relative;
    flex: 0 0 auto;
    /* width: 37vh;
    height: 20vh; */
    width: 150px;
    height: 150px;
    font-size: 12px;
    /* background: salmon; */
    border: 2px solid @light-orange;
    background-color: @white;
    border-radius: 0px 20px;
    // box-shadow: 0px 4px 20px #DDD7FA;
    box-shadow: none;
    margin: 0 1.5% 20px 1.5%;
    padding: 24px;
    cursor: pointer;
    &:hover {
      box-shadow: 0px 4px 20px @orange;
      transition-duration: @animation-duration;
    }
    h3, div {
      padding-bottom: 10px;
    }
    h3 {
      font-size: 16px;
      color: @black;
    }
    .description {
      font-weight: @weight-bold;
      color: @gray;
      font-size: 12px;
      height: 40%;
      overflow: hidden;
    }
    p {
      width: 100%;
      padding-top: 10px;
    }
  }
  }
  .progress{
    position: absolute;
    bottom: 0;
    width: 80%;
    //padding: 10px 0 0 10px;
    .percent {
      color: @gray;
      font-size: 8px;
      font-weight: 600;
    }
    progress {
      width: 80%;
      height: 10px;
      border: none;
      &::-webkit-progress-bar {
        background-color: @light-gray;
        border-radius: 25px;
      }
      &::-webkit-progress-value {
        background-color: #6EEE03;
        border-radius: 25px;
      }
    }
  }

  #back-button {
    font-size: 90%;
    padding: 0px 8px;
    color: @gray;
    &:hover, &:focus {
      color: @black;
      border-color: transparent;
      box-shadow: 0 0 0 transparent;
      background-color: transparent;
    }
  }
</style>
<style lang="less" scoped>
  .filter-difficulty .ivu-dropdown .ivu-select-dropdown {
    height: 210px;
    overflow-y: scroll;
  }
  @media screen and (max-width: 900px) {
    .category-name {
      margin: 0;
    }
    .category {
      margin: 20px 15px !important;
    }
    .main-list {
      flex-direction: column-reverse;
      margin: 15px auto !important;
      .left-menu {
        .top-menu {
          max-height: 32px;
        }
      }
      .right-menu {
        margin: 0 0 0 20px !important;
        max-width: 90%;
      }
    }
  }
</style>