<template>
  <div class="view">
    <Panel title="카테고리 목록">
      <div slot="header">
        <el-input
          v-model="keyword"
          prefix-icon="el-icon-search"
          placeholder="Keywords">
        </el-input>
      </div>
      <el-table
        v-loading="loading"
        element-loading-text="loading"
        ref="table"
        :data="problemCategoryList"
        style="width: 100%">
        <el-table-column
          width="150"
          prop="id"
          label="ID">
        </el-table-column>
        
        <el-table-column
          prop="title"
          label="제목">
          <template slot-scope="{row}">
            <span v-show="!row.isEditing">{{row.title}}</span>
            <el-input v-show="row.isEditing" v-model="row.title">
            </el-input>
          </template>
        </el-table-column>

        <el-table-column
          prop="문제 수"
          label="문제 수">
          <template slot-scope="{row}">
            <span>{{row.problems.length}}</span>
          </template>
        </el-table-column>

        <el-table-column
          fixed="right"
          label="수정"
          width="250">
          <div slot-scope="scope">
            <icon-btn name="Edit" icon="edit" @click.native="editProblemCategory(scope.row.id)"></icon-btn>
            <icon-btn icon="trash" name="Delete Category"
                      @click.native="deleteProblemCategory(scope.row.id)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>

      <div class="panel-options">
        <el-button type="primary" size="small"
                   @click="goCreateProblemCategory" icon="el-icon-plus">카테고리 생성
        </el-button>

        <el-pagination
          class="page"
          layout="prev, pager, next"
          @current-change="currentChange"
          :page-size="pageSize"
          :total="total">
        </el-pagination>
      </div>
    </Panel>
    
  </div>
</template>

<script>
  import api from '../../api.js'
  import utils from '@/utils/utils'
  import {mapGetters} from 'vuex'
  export default {
    name: 'ProblemCategoryList',
    data () {
      return {
        pageSize: 10,
        total: 0,
        problemCategoryList: [],
        loading: false,
        currentPage: 1,
        routeName: '',
        keyword: ''
      }
    },
    mounted () {
      this.routeName = this.$route.name
      this.getProblemCategoryList(this.currentPage)
    },
    computed: {
      ...mapGetters(['isSuperAdmin'])
    },
    methods: {
      handleDblclick (row) {
        row.isEditing = true
      },
      goCreateProblemCategory () {
        this.$router.push({name: 'problem-category'}).catch(() => {})
      },
      // 切换页码回调
      currentChange (page) {
        this.currentPage = page
        this.getProblemCategoryList(page)
      },
      getProblemCategoryList (page = 1) {
        this.loading = true
        let params = {
          limit: this.pageSize,
          offset: (page - 1) * this.pageSize,
          keyword: this.keyword
        }
        api.getProblemCategoryList(params).then(res => {
          this.loading = false
          this.total = res.data.data.total
          for (let problem of res.data.data.results) {
            problem.isEditing = false
          }
          this.problemCategoryList = res.data.data.results
        }, res => {
          this.loading = false
        })
      },
      editProblemCategory (categoryId) {
        this.$router.push({name: 'edit-problem-category', params: {categoryId}}).catch(() => {})
      },
      deleteProblemCategory (id) {
        api.deleteProblemCategory(id).then(res => {
          this.$router.go()
        })
      }
    },
    watch: {
      '$route' (newVal, oldVal) {
        this.routeName = newVal.name
        this.getProblemCategoryList(this.currentPage)
      },
      'keyword' () {
        this.getProblemCategoryList(this.currentPage)
      }
    }
  }
</script>

<style scoped lang="less">
</style>
