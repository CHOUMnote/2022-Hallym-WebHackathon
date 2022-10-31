<template>
  <div class="flex-container">
    <div id="main">
        <div class="community">
          <!--<div class="community_menu_name">커뮤니티</div>-->
          <div class="community_menu">
            <!-- <div class="community_menu_element" @click="handleTypeChange('0')">
              <div class="community_menu_list" v-bind:style="[this.formFilter.boardtype === '' || this.formFilter.boardtype === '0' ?{'color' : '#F5A547'}:{}]" >
                전체 게시판
              </div>
            </div> -->
            <div class="community_menu_element" @click="handleTypeChange('1')">
              <div class="community_menu_list" v-bind:style="[this.formFilter.boardtype === '1' ?{'color' : '#F5A547'}:{}]">
                자유 게시판
              </div>
            </div>
            <!-- <div class="community_menu_element" @click="handleTypeChange('2')">
              <div class="community_menu_list" v-bind:style="[this.formFilter.boardtype === '2' ?{'color' : '#F5A547'}:{}]">
                질문 게시판
              </div>
            </div> -->
            <!-- <div class="community_menu_element" @click="handleTypeChange('3')">
              <div class="community_menu_list" v-bind:style="[this.formFilter.boardtype === '3' ?{'color' : '#F5A547'}:{}]">
                요청 게시판
              </div>
            </div> -->
          </div>

          <button type="button" id="add-new" @click="Create">+</button>
        </div>
        <div class="community_free">
          <!-- 게시판 상단 부분 -->
          <!--<div class="community_free_title" slot="title">{{mainTitle}}</div>-->

          <div class="community_free_bar" slot="extra">
            <div>
              <div id="order-by">
                <!-- 게시판 정렬 선택 -->
                <div class="community_free_bar_order_by" @click="handleSortChange('0')">
                  <div class = "community_free_bar_order_element" v-bind:style="[this.sort === '' || this.sort == '0' ? {'color' : '#858585'}:{}]">최신순</div>
                </div>
                <div class="community_free_bar_order_by" @click="handleSortChange('1')">
                  <div class = "community_free_bar_order_element" v-bind:style="[this.sort === '1' ? {'color' : '#858585'}:{}]">좋아요순</div>
                </div>
                <div class="community_free_bar_order_by" @click="handleSortChange('2')">
                  <div class = community_free_bar_order_element v-bind:style="[this.sort === '2' ? {'color' : '#858585'}:{}]">댓글순</div>
                </div>
              </div>

              <ul v-if="formFilter.boardtype === '2'" class="filter">
              <!-- 질문 게시판의 경우 언어 카테고리 -->
              <div id="separator"></div>
              <li class="submenu_list">
                <Dropdown @on-click="handleLanguageChange">
                  <span><div style="padding-right:3px; display: inline-flex;" v-bind:style="[this.language != '' ? {'color' : '#858585'}:{}]">{{ toLanguage(this.language) }}</div><div style="display: inline-flex;"><Icon type="md-arrow-dropdown" /></div></span>
                  <Dropdown-menu slot="list">
                    <Dropdown-item name="Java">Java</Dropdown-item>
                    <Dropdown-item name="C">C</Dropdown-item>
                    <Dropdown-item name="C++">C++</Dropdown-item>
                    <Dropdown-item name="Python">Python</Dropdown-item>
                  </Dropdown-menu>
                </Dropdown>
              </li>
              </ul>
            </div>

              <div>
                <ul>
                  <li class="submenu_list">
                    <!-- 게시글 검색 카테고리 선택 - searchtype 결정 -->
                    <Select v-model="formFilter.searchtype" style="width:73px">
                      <Option v-for="item in searchTypeList" :value="item.value" :key="item.value">
                        {{ item.label }}
                      </Option>
                    </Select>
                  </li>

                  <li class="submenu_list">
                    <!-- 게시글 검색 내용 입력 - search -->
                    <Input @on-search="handleQueryChange" v-model="formFilter.search" search placeholder="검색어를 입력하세요."></Input>
                  </li>
                  <!-- <li class="submenu_list">
                    <Button type="primary" icon="ios-search" @click="handleQueryChange"></Button>
                  </li> -->
                </ul>
              </div>
              
              <!-- 게시판 정렬 선택 -->
              <!-- <li class="submenu_list" style="width=200px">
                <Dropdown @on-click="handleSortChange">
                  <span><div style="padding-right:3px; display: inline-flex;">정렬</div><div style="display: inline-flex;"><Icon type="md-arrow-dropdown" /></div></span>
                  <Dropdown-menu slot="list">
                    <Dropdown-item name="0">최신순</Dropdown-item>
                    <Dropdown-item name="1">좋아요순</Dropdown-item>
                    <Dropdown-item name="2">댓글순</Dropdown-item>
                  </Dropdown-menu>
                </Dropdown>
              </li> -->

              <!-- 게시판 타입 선택 -->
              <!-- <li class="submenu_list">
                <Dropdown @on-click="handleTypeChange">
                  <span>게시판<Icon type="arrow-down-b"></Icon></span>
                  <Dropdown-menu slot="list">
                    <Dropdown-item name="">전체</Dropdown-item>
                    <Dropdown-item name="1">자유</Dropdown-item>
                    <Dropdown-item name="2">질문</Dropdown-item>
                  </Dropdown-menu>
                </Dropdown>
              </li> -->

              <!-- All - 전체 게시글 출력 / Mine - 자신이 작성한 게시글만 출력 -->
              <!-- <li class="submenu_list">
                <i-switch size="large" v-model="formFilter.myself" @on-change="handleQueryChange">
                  <span slot="open">{{$t('m.Mine')}}</span>
                   <span slot="close">{{$t('m.All')}}</span>
                </i-switch>
              </li> -->

                <!-- 게시글 작성 버튼 -->
              <!-- <li class="submenu_list">
                <Button type="primary" @click="Create">Create Article</Button>
              </li> -->

              <!-- 새로고침 버튼 -->
              <!-- <li class="submenu_list">
                <Button type="info" icon="refresh" @click="getArticles">{{$t('m.Refresh')}}</Button>
              </li> -->
          </div>
          <!-- <div>
              !-- 게시글 목록 --
            <Table :show-header="false" :disabled-hover="true" :columns="columns" :data="articles" :loading="loadingTable"></Table>
          </div> -->

          <ul class="article-table">
            <li v-for="(item) in articles">
              <ul class="article-entry">
                <div>
                  <div>
                    <li><a @click="toArticle(item)"> {{item.title}} </a></li>
                  </div>
                  <div>
                    <li><a @click="toUser(item)"> {{item.username}} </a></li>
                    <li> | {{ convertDate(item) }}</li>
                  </div>
                </div>
                <div>
                  <div>
                    <Icon type="md-heart" class="heart" size="20" color="#C4C4C4"/>
                    <li>{{item.like_count}}</li>
                  </div>
                  <div>
                    <Icon type="md-text" class="comment" size="20" color="#c4C4C4" />
                    <li>{{item.comment_count}}</li>
                  </div>
                </div>
              </ul>
              <hr>
            </li>
          </ul>

        <!-- 하단 -->
          <div style="display:flex; justify-content: center">

            <!-- <div style="margin:auto auto; line-height:center">
              <ul>
                <li class="submenu_list">
                  !-- 게시글 검색 카테고리 선택 - searchtype 결정 --
                  <Select v-model="formFilter.searchtype" style="width:100px">
                    <Option v-for="item in searchTypeList" :value="item.value" :key="item.value">
                      {{ item.label }}
                    </Option>
                  </Select>
                </li>

                <li class="submenu_list">
                  !-- 게시글 검색 내용 입력 - search --
                  <Input v-model="formFilter.search" placeholder="검색" style="width: 300px"></Input>
                </li>
                <li class="submenu_list">
                  <Button type="primary" icon="ios-search" @click="handleQueryChange">검색</Button>
                </li>
              </ul>
            </div>-->
            <div style="float:right">
              <Pagination :total="total" :page-size="limit" @on-change="changeRoute" :current.sync="page"></Pagination>
            </div>
          </div>

        </div> <!-- float right div -->
      </div>
    </div>
</template>

<script>
  import api from '@oj/api'
  import time from '@/utils/time'
  import Pagination from '@/pages/oj/components/Pagination'
  import utils from '@/utils/utils'
  
  export default {
    name: 'ArticleList',
    components: {
      Pagination
    },
    data () {
      return {
        searchTypeList: [
          {
            value: '0',
            label: '전체'
          },
          {
            value: '1',
            label: '제목'
          },
          {
            value: '2',
            label: '내용'
          },
          {
            value: '3',
            label: '작성자'
          }
        ],
        mainTitle: '',
        formFilter: { // 게시글을 불러올 때 필터 설정용 데이터
          myself: false, // true - 내가 작성한 게시글만, false - 전체 게시글
          username: '', // 현재 접속 중인 유저명 - 이 유저명을 통해 myself 값 설정
          boardtype: '', // 게시판 타입 - 자유 게시판 = 1, 질문 게시판 = 2
          search: '', // 게시글 검색 시 검색할 내용
          searchtype: '' // 게시글 검색 시 검색할 카테고리 - 제목 = 0, 내용 = 1, 작성자명 = 2
        },
        columns: [ // 열 속성 - 추후 추가 예정
          // {
          //   title: '번호',
          //   align: 'center',
          //   render: (h, params) => {
          //     return h('span', params.row.id)
          //   }
          // },
          {
            title: '제목',
            align: 'center',
            render: (h, params) => {
              return h('a',
                {
                  style: {
                  },
                  on: { // 게시글 제목 클릭 시 해당 게시글 detail 뷰로 이동, 게시글 고유 ID 전송
                    click: () => {
                      this.$router.push({name: 'article-details', params: {articleID: params.row.id}}).catch(() => {})
                    }
                  }
                }, params.row.title)
            }
          },
          {
            title: '작성일',
            align: 'center',
            render: (h, params) => {
              return h('div', {
                style: {
                }
              }, time.utcToLocal(params.row.create_time, 'YYYY-MM-DD HH:mm:ss'))
            }
          },
          {
            title: '작성자',
            align: 'center',
            render: (h, params) => {
              return h('a', {
                style: {
                },
                on: { // 작성자명 클릭 시 해당 작성자의 프로필로 이동
                  click: () => {
                    this.$router.push(
                      {
                        name: 'user-home',
                        query: {username: params.row.username}
                      }).catch(() => {})
                  }
                }
              }, params.row.username)
            }
          },
          {
            title: '좋아요',
            align: 'center',
            render: (h, params) => {
              return h('div', {
                style: {
                }
              }, params.row.like_count)
            }
          },
          {
            title: '댓글',
            align: 'center',
            render: (h, params) => {
              return h('div', {
                style: {
                }
              }, params.row.comment_count)
            }
          }
        ],
        loadingTable: false,
        articles: [], // 게시글 목록
        total: 30,
        limit: 12, // 한 페이지에 출력할 최대 게시글 개수
        page: 1, // 현재 페이지
        sort: 0, // 게시글 정렬 기준, 0 - 최신순 / 1 - 좋아요순 / 2 - 댓글 순
        language: '' // 질문 게시판의 경우 원하는 언어의 게시글만 출력하기 위한 변수
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        let contentCount = 4 // 이후 컨텐츠(게시판)이 추가 될 경우 이를 늘릴 것
        // 쿼리로 필터 설정
        let query = this.$route.query
        this.formFilter.myself = query.myself === '1'
        this.formFilter.username = query.username || ''
        // 지정 된 type이 아닐 경우 board type 강제 변환
        if (this.$route.query.boardtype !== '' && (parseInt(this.$route.query.boardtype) >= contentCount || parseInt(this.$route.query.boardtype) < 0)) {
          this.formFilter.boardtype = '-1'
          this.changeRoute()
          return
        }
        this.formFilter.boardtype = query.boardtype || ''
        this.formFilter.search = query.search || ''
        this.formFilter.searchtype = query.searchtype || ''
        this.formFilter.language = query.language || ''
        this.page = parseInt(query.page) || 1
        if (this.page < 1) {
          this.page = 1
        }
        switch (this.formFilter.boardtype) {
          case '1' :
            this.mainTitle = '자유 게시판'
            break
          case '2' :
            this.mainTitle = '질문 게시판'
            break
          case '3' :
            this.mainTitle = '요청 게시판'
            break
          default :
            this.mainTitle = '전체 게시판'
        }
        this.getArticles() // 쿼리로 설정한 데이터(필터)를 통해 게시글 데이터를 가져옴
        this.handleColumnVisible(this.formFilter.boardtype) // 게시판의 종류에 따라 Table의 column들을 변경하는 함수
      },
      buildQuery () { // 쿼리로 설정한 필터값을 전송용 데이터로 빌드
        return {
          myself: this.formFilter.myself === true ? '1' : '0',
          username: this.formFilter.username,
          page: this.page,
          boardtype: this.formFilter.boardtype,
          sort: this.sort,
          search: this.formFilter.search,
          searchtype: this.formFilter.searchtype,
          language: this.language
        }
      },
      getArticles () { // 게시글 목록 가져오기
        let params = this.buildQuery() // 게시글 필터 데이터
        let offset = (this.page - 1) * this.limit
        this.loadingTable = true
        api.getArticleList(offset, this.limit, params).then(res => { // 필터값을 전송하여 게시글 데이터 가져옴
          let data = res.data.data
          for (let v of data.results) {
            v.loading = false
          }
          this.loadingTable = false
          this.articles = data.results // 필터를 거쳐 나온 게시글 데이터
          this.total = data.total
        }).catch(() => {
          this.loadingTable = false
        })
      },
      Create () { // 게시글 작성
        this.$router.push({name: 'create-article'}).catch(() => {})
      },
      changeRoute () { // 쿼리값을 변경 후 route 변경
        let query = utils.filterEmptyValue(this.buildQuery())
        let routeName = 'article-list'
        this.$router.push({
          name: routeName,
          query: utils.filterEmptyValue(query)
        }).catch(() => {})
      },
      handleTypeChange (boardtype) { // 게시판 타입 변경, 1 = 자유 / 2 = 질문
        // 중복 페이지 클릭 방지
        if (this.formFilter.boardtype === boardtype) {
          return
        }
        if (this.language !== '2') { // 질문 게시판이 아닌 경우 쿼리에서 language를 지움
          this.language = ''
        }
        this.page = 1
        this.formFilter.boardtype = boardtype
        this.changeRoute()
      },
      handleQueryChange () { // 게시판 페이지 변경
        this.page = 1
        this.changeRoute()
      },
      handleSortChange (sorttype) { // 게시글 정렬 변경
        if (this.sort === sorttype) {
          return
        }
        this.sort = sorttype
        this.changeRoute()
      },
      handleSearchTypeChange (searchtype) { // 게시글 검색 카테고리 변경
        this.formFilter.searchtype = searchtype
      },
      handleColumnVisible (boardtype) { // 게시판 타입에 따라 column을 추가하거나 제거하는 함수
        if (boardtype === '2' && !this.language) { // 현재 질문 게시판으로 이동하되 language 쿼리가 비어 있는 경우 언어 column 추가
          this.columns.push(
            {
              title: '언어',
              align: 'center',
              render: (h, params) => {
                return h('span', params.row.problemtype)
              }
            })
        } else if (boardtype !== '2') { // 질문 게시판이 아닌 게시판으로 이동하는 경우 언어 column을 지움
          this.columns.splice(6, 1)
        }
      },
      handleLanguageChange (language) { // 질문 게시판의 경우 출력하고자하는 게시글의 언어 카테고리 설정
        this.language = language
        this.changeRoute()
      },
      toArticle (item) {
        this.$router.push({name: 'article-details', params: {articleID: item.id}}).catch(() => {})
      },
      toUser (item) {
        this.$router.push(
          {
            name: 'user-home',
            query: {username: item.username}
          }).catch(() => {})
      },
      convertDate (item) {
        return time.utcToLocal(item.create_time, 'YYYY-MM-DD HH:mm')
      },
      toLanguage (language) {
        if (language === '') return '언어'
        else return this.language
      }
    },
    watch: {
      '$route' (newVal, oldVal) {
        if (newVal === '-1' || parseInt(newVal.query.boardtype) < 0) {
          this.$router.push({path: '/404'}).catch(() => {})
        }
        if (newVal !== oldVal) {
          this.init()
        }
      }
    }
  }
</script>

<style scoped lang="less">
  @import '../../../../styles/common.less';
  .flex-container {
    #main {
      margin: 0 5% 0 5%;
      padding-top: 15px;
      background-color: @white;
      width: 80%;
    }
  }
  .community {
    display: flex;
    justify-content: space-between;
    margin: 10px 0;
    font-size: 16px;
    text-align: center;
    padding: 0 50px;
  }

  .community_menu {
    display: flex;
    font-size: 16px;
    line-height: 35px;
    color: @gray;
  }

    #order-by {
      display: flex;
      font-size: 12px;
      color: #C0C0C0;
    }

    .community_menu_element {
      padding: 0 25px 0 0;
    }
    .community_menu_list {
        // color: black;
        transition: all 0.3s ease-in-out;
        cursor: pointer;
        // border-bottom: 1px solid rgb(90, 90, 90);
    }
    .community_menu_list:hover {
        border-radius: 2px;
        // background-color: rgba(110, 182, 248, 0.925);
        color: @dark-orange;
    }
    .community_free_bar_order_by {
      padding: 0 15px 0 0;
    }

    .community_free_bar_order_element {
      cursor: pointer;
      transition: all 0.3s ease-in-out;
    }

    .community_free_bar_order_element:hover {
      color: @gray;
    }

    .community_free {
        //display: inline-block;
        //vertical-align: top;
        //width: 80%;
        //height: 60%;
        // padding: 0 20px 0 20px;
        /* background-color: rgb(136, 167, 138); */
    }
    .community_free_bar{
        display: flex;
        justify-content: space-between;
        margin: 10px 0 0 0;
        padding: 10px 50px;
        background-color: #F9F9F9;
        line-height: 40px;
        div:nth-of-type(1) {
          display: flex;
        }
    }

    .filter {
      display: flex;
      li {
        color: #c0c0c0;
        &:hover {
          color: #858585;
          transition: all .3s ease-in-out;
        }
      }
    }

    #separator {
      border-left: 2px solid #c0c0c0;
      border-radius: 20px;
      margin-right: 15px;
    }
    // .community_free_title {
    //     /* display: block; */
    //     /* margin-top: -10px; */
    //     padding: 0 0 10px 0;
    //     border-bottom: 2px solid black;
    //     font-size: 24px;
    //     color: #1f4e79;
    //     /* background-color: rgb(255, 234, 239); */
    // }
    .submenu_list {
      cursor: pointer;
      display: inline-block;
      //margin-right: 10px;
    }

    #add-new {
      cursor: pointer;
      padding: 0 10px;
      height: 35px;
      background-color: @white;
      border: solid 1px @gray;
      color: @gray;
      font-size: @font-regular;
      transition: all 0.3s ease-in-out;
    }

    #add-new:hover {
      background-color: @light-orange;
      color: @dark-orange;
      border: solid 1px @dark-orange;
    }

    .article-table {
      list-style: none;
      hr {
        border: 0;
        border-top: 1px solid #C4C4C4;
      }
    }

    .article-entry {
      margin: 10px 50px;
      list-style: none;
      display: flex;
      justify-content: space-between;
      div:nth-of-type(1) {
        a {
          color: @black;
        }
        display: flex;
        flex-direction: column;
        div:nth-of-type(1) {
          font-size: @font-regular;
        }
        div:nth-of-type(2) {
          a, li {
            color: @gray;
            transition: all 0.3s ease-in-out;
          }
          a:hover {
            color: @orange;
            
          }
          li:first-child {
            margin-right: 4px;
          }
        }
      }
      div:nth-of-type(2) {
        display: flex;
        div:first-child {
          li:first-of-type {
            margin-right: 20px;
            line-height: 50px;
          }
          display: flex;
          flex-direction: row;
        }

        div:nth-of-type(2) {
          li:first-of-type {
            line-height: 50px;
          }
          display: flex;
          flex-direction: row;
        }
      }
    }

    .heart, .comment {
      margin-right: 10px;
      margin-top: 15px;
    }

    @media screen and (max-width: 900px) {
      #main {
        margin: 0 !important;
        min-width: 90vw;
        .community {
          padding: 0 10px 0;
          flex-direction: column;
          .community_menu {
            .community_menu_element {
              min-width: 90px;
              padding-right: 15px;
              .community_menu_list {
                font-size: 0.8em;
              }
            }
          }
        }
        .community_free {
          width: 100%;
          .community_free_bar {
            display: block;
            padding: 10px 20px;
          }
          .article-entry {
            margin: 10px 20px;
          }
        }
      }
      
    }

    
</style>
