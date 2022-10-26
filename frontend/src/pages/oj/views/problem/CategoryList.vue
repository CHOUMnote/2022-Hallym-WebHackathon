<template>
  <div class="flex-container">
    <div id="main">
        <div class="community">
          <div class="community_menu">
            <div class="community_menu_element">
              <div class="community_menu_list" >
                카테고리 리스트
              </div>
            </div>
          </div>

        </div>
        <div class="community_free">

          <div class="community_free_bar" slot="extra">
              <div id="order-by">
              </div>

              <div class="submenu" style="">
                <ul>
                  <li class="submenu_list">
                    <!-- 카테고리 검색 카테고리 선택 - searchtype 결정 -->
                    <Select v-model="formFilter.searchtype">
                      <Option v-for="item in searchTypeList" :value="item.value" :key="item.value">
                        {{ item.label }}
                      </Option>
                    </Select>
                  </li>

                  <li class="submenu_list">
                    <!-- 게시글 검색 내용 입력 - search -->
                    <Input @on-search="handleQueryChange" v-model="formFilter.search" search placeholder="검색어를 입력하세요."></Input>
                  </li>
                </ul>
              </div>
          </div>
          <ul class="article-table">
            <li v-for="(item) in problemCategoryList">
              <ul class="article-entry">
                <div>
                  <div>
                    <li><a @click="goProblemList(item.id, item.title)"> {{item.title}} </a></li>
                  </div>
                  <div>
                    <li><p v-katex v-html="item.description"></p></li>
                  </div>
                </div>
                <div class="progress">
                  <div class="percent">
                    <li>달성률 : {{item.percent}} %</li>
                  </div>
                  <div class="percent">
                    <li>
                      <progress max="100" :value="item.percent"></progress>
                    </li>
                  </div>
                </div>
              </ul>
              <hr>
            </li>
          </ul>

        <!-- 하단 -->
          <div style="display:flex; justify-content: center">
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
  import Pagination from '@/pages/oj/components/Pagination'
  import utils from '@/utils/utils'
  
  export default {
    name: 'CategoryList',
    components: {
      Pagination
    },
    data () {
      return {
        problemCategoryList: {},
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
          }
        ],
        formFilter: { // 카테고리를 불러올 때 필터 설정용 데이터
          search: '', // 카테고리 검색 시 검색할 내용
          searchtype: '' // 카테고리 검색 시 검색할 카테고리 - 전체 = 0, 제목 = 1, 댓글 = 2
        },
        loadingTable: false,
        total: 30,
        limit: 12, // 한 페이지에 출력할 최대 카테고리 개수
        page: 1 // 현재 페이지
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        // 쿼리로 필터 설정
        let query = this.$route.query

        this.formFilter.search = query.search || ''
        this.formFilter.searchtype = query.searchtype || '0'
        this.page = parseInt(query.page) || 1
        if (this.page < 1) {
          this.page = 1
        }
        this.getCategoryList() // 쿼리로 설정한 데이터(필터)를 통해 게시글 데이터를 가져옴
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
      buildQuery () { // 쿼리로 설정한 필터값을 전송용 데이터로 빌드
        return {
          page: this.page,
          search: this.formFilter.search,
          searchtype: this.formFilter.searchtype
        }
      },
      getCategoryList () { // 카테고리 목록 가져오기
        let params = this.buildQuery() // 카테고리 필터 데이터
        let offset = (this.page - 1) * this.limit
        this.loadingTable = true
        api.getProblemCategoryList(offset, this.limit, params).then(res => {
          this.problemCategoryList = res.data.data.result
          this.total = res.data.data.total
          this.loadingTable = false
        }).catch(() => {
          this.loadingTable = false
        })
      },
      changeRoute () { // 쿼리값을 변경 후 route 변경
        let query = utils.filterEmptyValue(this.buildQuery())
        let routeName = 'category-list'
        this.$router.push({
          name: routeName,
          query: utils.filterEmptyValue(query)
        }).catch(() => {})
      },
      handleQueryChange () { // 카테고리 페이지 변경
        this.page = 1
        this.changeRoute()
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

<style lang="less">
  @import '../../../../styles/common.less';
  .progress{
    .percent {
      color: @gray;
      font-size: 12px;
      font-weight: 600;
    }

    progress {
      width: 100px;
      height: 10px;
      border: none;
      &::-webkit-progress-bar {
        background-color: @light-gray;
        border-radius: 15px;
      }
      &::-webkit-progress-value {
        background: @green; /* Old browsers */
        // background: -moz-linear-gradient(left,  #e52759 0%, #f5a547 60%, #f8c07f 99%); /* FF3.6-15 */
        // background: -webkit-gradient(linear, left top, right top, color-stop(0%,#e52759), color-stop(60%,#f5a547), color-stop(99%,#f8c07f)); /* Chrome4-9,Safari4-5 */
        // background: -webkit-linear-gradient(left,  #e52759 0%,#f5a547 60%,#f8c07f 99%); /* Chrome10-25,Safari5.1-6 */
        // background: -o-linear-gradient(left,  #e52759 0%,#f5a547 60%,#f8c07f 99%); /* Opera 11.10-11.50 */
        // background: -ms-linear-gradient(left,  #e52759 0%,#f5a547 60%,#f8c07f 99%); /* IE10 preview */
        // background: linear-gradient(to right,  #e52759 0%,#f5a547 60%,#f8c07f 99%); /* W3C, IE10+, FF16+, Chrome26+, Opera12+, Safari7+ */
        // filter: progid:DXImageTransform.Microsoft.gradient( startColorstr='#e52759', endColorstr='#f8c07f',GradientType=1 ); /* IE6-9 */
        border-radius: 15px;
      }
    }
  }
</style>

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
        // display: inline-block;
        // vertical-align: top;
        /* padding: 0 0 20px 0; */
        // width: 17%;
        // height: 15%;
        // padding: 0 10px 20px 0;
        display: flex;
        justify-content: space-between;
        margin-top: 10px;
        position: relative;
        font-size: 16px;
        text-align: center;
    }

    .community_menu {
        position: relative;
        left: 50px;
        display: flex;
        /* vertical-align: top; */
        /* width: 20%; */
        /* height: 20%; */
        // margin-top: 10px;
        // padding: 0 0 20px 0;
        font-size: 16px;
        /* text-align: center; */
        /* background-color: rgb(232, 238, 177);  */
        // border-radius: 5px;
        /* border-top: 2px solid rgb(61, 61, 61); */
        line-height: 35px;
        color: @gray;
    }

    #order-by {
      position: relative;
      left: 50px;
      display: flex;
      font-size: 12px;
      color: #C0C0C0;
    }

    .community_menu_element {
      padding: 0 25px 0 0;
    }
    .community_menu_list {
        // color: black;
        font-size: 24px;
        font-weight: bold;
        color: @dark-orange;
        // border-bottom: 1px solid rgb(90, 90, 90);
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
        background-color: #F9F9F9;
        padding: 10px 0px;
        line-height: 40px;
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
    .submenu {
      position:relative; 
      right:50px;
    }
    .submenu_list {
      display: inline-block;
      //margin-right: 10px;
      .ivu-select .ivu-select-single .ivu-select-default {
        width: 73px;
      }
      .ivu-input-wrapper .ivu-input-wrapper-default .ivu-input-type {
        width: 300px;
      }
    }

    #add-new {
      cursor: pointer;
      position: relative;
      right: 50px;
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
  @media screen and (max-width : 900px) {
    #main {
      width: 90vw;
      .community {
        text-align: start;
        .community_menu {
          left: 0px;
          margin-left: 20px;
        }
      }
      .community_free {
        width: 100%;
        .community_free_bar {
          min-width: 400px;
          display: block;
          //justify-content: center;
          //left: 10px;
          .submenu {
            right: 0px;
            margin-left: 20px;
            ul {
              li:first-child {
                min-width: 20%;
              }
              li {
                min-width: 50%;
              }
            }
          }
        }
      }
      .article-table {
        .article-entry {
          margin: 10px 20px;
          min-width: 270px;
        }
      }
      
    }
  }
</style>
