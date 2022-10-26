<template>
    <div class="flex-container">
    <div id="main">
        <div class="community">
          <!--<div class="community_menu_name">커뮤니티</div>-->
          <div class="community_menu">
            <div class="community_menu_element" @click="handleTypeChange('0')">
              <div v-if="routeName == 'comment-list'" class="community_menu_list" >
                댓글 단 게시글
              </div>
              <div v-if="routeName == 'like-list'" class="community_menu_list" >
                좋아요 한 게시글
              </div>
            </div>
          </div>
        </div>
        <div class="community_free">
          <!-- <div>
              !-- 게시글 목록 --
            <Table :show-header="false" :disabled-hover="true" :columns="columns" :data="articles" :loading="loadingTable"></Table>
          </div> -->

          <ul class="article-table">
            <li v-if="articles.length < 1">
              <ul class="no-article-entry">
                <div>해당 내역이 존재하지 않아요 :(</div>
              </ul>
            </li>
            <li v-else v-for="(item) in articles">
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
                    <Icon type="md-heart" class="heart" size="16" color="#C4C4C4"/>
                    <li>{{item.like_count}}</li>
                  </div>
                  <div>
                    <Icon type="md-text" class="comment" size="16" color="#c4C4C4" />
                    <li>{{item.comment_count}}</li>
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
  import { mapGetters } from 'vuex'
  import api from '@oj/api'
  import utils from '@/utils/utils'
  import time from '@/utils/time'
  import Pagination from '@oj/components/Pagination'
  export default {
    components: {
      Pagination
    },
    data () {
      return {
        formFilter: { // 게시글을 불러올 때 필터 설정용 데이터
          username: ''
        },
        routeName: '',
        loadingTable: false,
        articles: [], // 게시글 목록
        total: 30,
        limit: 12, // 한 페이지에 출력할 최대 게시글 개수
        page: 1
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      init () {
        this.routeName = this.$route.name
        let query = this.$route.query
        this.formFilter.username = query.username || ''
        if (this.page < 1) {
          this.page = 1
        }
        this.getArticles()
        console.log(this.articles)
      },
      buildQuery () { // 쿼리로 설정한 필터값을 전송용 데이터로 빌드
        return {
          username: this.formFilter.username,
          page: this.page
        }
      },
      getArticles () { // 게시글 목록 가져오기
        let params = this.buildQuery() // 게시글 필터 데이터
        let offset = (this.page - 1) * this.limit
        this.loadingTable = true
        if (this.routeName === 'comment-list') {
          api.getCommentArticleList(offset, this.limit, params).then(res => { // 필터값을 전송하여 게시글 데이터 가져옴
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
        } else if (this.routeName === 'like-list') {
          api.getLikeArticleList(offset, this.limit, params).then(res => { // 필터값을 전송하여 게시글 데이터 가져옴
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
        }
      },
      changeRoute () { // 쿼리값을 변경 후 route 변경
        let query = utils.filterEmptyValue(this.buildQuery())
        let routeName = 'comment-list'
        this.$router.push({
          name: routeName,
          query: utils.filterEmptyValue(query)
        }).catch(() => {})
      },
      convertDate (item) {
        return time.utcToLocal(item.create_time, 'YYYY-MM-DD HH:mm')
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
      }
    },
    computed: {
      ...mapGetters(['website', 'modalStatus', 'user']),

      previewStyle () {
        return {
          'width': this.preview.w + 'px',
          'height': this.preview.h + 'px',
          'overflow': 'hidden'
        }
      }
    }
  }
</script>

<!-- <style lang="less" scoped>

  // .flex-container {
  //   flex-wrap: wrap;
  //   justify-content: flex-start;
  // }
</style> -->
<style scoped lang="less">
  @import '../../../../../styles/common.less';
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
    margin: 30px 0;
    font-size: 16px;
    text-align: center;
    padding: 0 30px;
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
        font-size: 24px;
        font-weight: bold;
        color: @dark-orange;
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
      margin-top: 20px;
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
    .no-article-entry {
      margin: 100px 50px;
      list-style: none;
      display: flex;
      justify-content: space-between;
      color: #c1c1c1;
      font-weight: bold;
      font-size: 25px;
    }
    .article-entry {
      margin: 10px 50px;
      list-style: none;
      display: flex;
      justify-content: space-between;
      div {
        justify-content: center;
      }
      div:nth-of-type(1) {
        a {
          color: @black;
        }
        display: flex;
        flex-direction: column;
        div:nth-of-type(1) {
          font-size: 16px;
        }
        div:nth-of-type(2) {
          font-size: 12px;
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
            font-size: 12px;
            margin-right: 20px;
            line-height: 50px;
          }
          display: flex;
          flex-direction: row;
        }

        div:nth-of-type(2) {
          li:first-of-type {
            font-size: 12px;
            line-height: 50px;
          }
          display: flex;
          flex-direction: row;
        }
      }
    }

    .heart, .comment {
      margin-right: 8px;
      margin-top: 17px;
    }
</style>
