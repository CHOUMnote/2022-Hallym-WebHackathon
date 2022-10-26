<template>
  <div class="category">
    <div class="title">
      <p @click="goCategoryList">문제 카테고리</p>
    <div class="next" @click="goCategoryList"><Icon type="ios-arrow-forward" size="40"/></div>
    </div>
    <!-- <hr style="color: gray;"> -->
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
</template>

<script>
  import api from '@oj/api'
  import utils from '@/utils/utils'
  export default {
    data () {
      return {
        problemCategoryList: {},
        page: 1, // 페이지로 보일 떄 시작 할 리스트 페이지 시점
        limit: 10, // 최대 표시할 개수
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
      init () {
        let params = this.buildQuery()
        let offset = (this.page - 1) * this.limit
        api.getProblemCategoryList(offset, this.limit, params).then(res => {
          this.problemCategoryList = res.data.data.result
        })
      },
      buildQuery () { // 쿼리로 설정한 필터값을 전송용 데이터로 빌드
        return {
          page: this.page,
          search: this.formFilter.search,
          searchtype: this.formFilter.searchtype
        }
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
      }
    }
  }
</script>

<style lang="less" scoped>
@import '../../../../styles/common.less';

  .progress{
    display: absolute;
    bottom: 0;
  }
  .category{
    position: relative;
    width:100%;
    margin: 20px 0 120px !important;
    background-color: @white;
    border-radius: @size-border-radius;
    box-shadow: 2px 5px 20px 2px rgba(90, 82, 128, 0.31);
    .title {
      .next {
        padding: 5px;
        position: absolute;
        top: 0;
        right : 15px;
        & i {
          transition: all 0.3s ease-in-out;
          color: @white !important;
        }
        &:hover i {
          transform: rotate( 360deg );
          color: @purple !important;
        }
      }
      background-color: @dark-orange;
      border-radius: 5px 5px 0 0;
      padding: 10px;
      color: @white;
      font-size: 20px;
      text-align: center;
      font-weight: @weight-bold;
      & p {
        cursor: pointer;
        width: fit-content;
        text-align: center;
        margin: 0 auto;
      }
      & p:hover {
        text-decoration:underline;
      }
    }
  }

  .box_container {
    padding: 10px 30px 30px;
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
    width: 250px;
    height: 180px;
    font-size: 16px;
    /* background: salmon; */
    border: 2px solid @light-orange;
    background-color: @white;
    border-radius: 0px 20px;
    box-shadow: 0px 4px 20px @light-orange;
    margin: 0 1.5% 20px 1.5%;
    padding: 24px;
    cursor: pointer;
    &:hover {
      box-shadow: 0px 4px 20px @dark-orange;
      transition-duration: @animation-duration;
    }
    h3, div {
      padding-bottom: 10px;
    }
    h3 {
      font-size: 20px;
      color: @black;
    }
    .description {
      font-weight: @weight-bold;
      color: @gray;
      font-size: 16px;
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
    width: 100%;
    //padding: 10px 0 0 10px;
    .percent {
      color: @gray;
      font-size: 12px;
      font-weight: 600;
    }
    progress {
      width: 80%;
      height: 10px;
      border: none;
      &::-webkit-progress-bar {
        background-color: @light-gray;
        border-radius: 15px;
      }
      &::-webkit-progress-value {
        background: #7556fc; /* Old browsers */
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