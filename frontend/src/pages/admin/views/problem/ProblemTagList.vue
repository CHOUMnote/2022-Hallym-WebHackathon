<template>
  <div class="view">
    <Panel title="문제 태그">
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
        :data="problemTagList"
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
            <span v-show="!row.isEditing">{{row.name}}</span>
            <el-input v-show="row.isEditing" v-model="row.name">
            </el-input>
          </template>
        </el-table-column>


        <el-table-column
          fixed="right"
          label="수정"
          width="250">
          <div slot-scope="scope">
            <icon-btn name="Edit" icon="edit" @click.native="openTagDialog(scope.row.id)"></icon-btn>
            <icon-btn icon="trash" name="Delete Category"
                      @click.native="deleteProblemTag(scope.row.id)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>

      <div class="panel-options">
        <el-button type="primary" size="small"
                   @click="openTagDialog()" icon="el-icon-plus">문제 태그 생성
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

    <el-dialog title="태그 수정" :visible.sync="showTagDialog" :close-on-click-modal="false">
      <el-form :model="tag" label-width="120px" label-position="left">
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="태그명" required>
              <el-input v-model="tag.name"></el-input>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
      <span slot="footer" class="dialog-footer">
        <cancel @click.native="showTagDialog = false">취소</cancel>
        <save @click.native="saveTag()"></save>
      </span>
    </el-dialog>
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
        problemTagList: [],
        loading: false,
        currentPage: 1,
        routeName: '',
        keyword: '',
        showTagDialog: false,
        tag: {},
        isModify: false
      }
    },
    mounted () {
      this.routeName = this.$route.name
      this.getProblemTagList(this.currentPage)
    },
    computed: {
      ...mapGetters(['isSuperAdmin'])
    },
    methods: {
      handleDblclick (row) {
        row.isEditing = true
      },
      // 切换页码回调
      currentChange (page) {
        this.currentPage = page
        this.getProblemTagList(page)
      },
      getProblemTagList (page = 1) {
        this.loading = true
        let params = {
          limit: this.pageSize,
          offset: (page - 1) * this.pageSize,
          keyword: this.keyword
        }
        api.getProblemTagList(params).then(res => {
          // this.problemTagList = res.data.data
          this.loading = false
          this.total = res.data.data.total
          for (let problem of res.data.data.results) {
            problem.isEditing = false
          }
          this.problemTagList = res.data.data.results
        }, res => {
          this.loading = false
        })
      },
      openTagDialog (tagId) {
        this.showTagDialog = true
        if (tagId) {
          api.getProblemTag(tagId).then(res => {
            this.tag = res.data.data
            this.isModify = true
          })
        } else {
          this.tag = {}
          this.isModify = false
        }
      },
      saveTag () {
        this.showTagDialog = false
        if (this.isModify) {
          api.modifyProblemTag(this.tag.id, this.tag.name).then(res => {
            this.$router.go()
          })
        } else {
          api.createProblemTag(this.tag.name).then(res => {
            this.$router.go()
          })
        }
      },
      deleteProblemTag (id) {
        api.deleteProblemTag(id).then(res => {
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
