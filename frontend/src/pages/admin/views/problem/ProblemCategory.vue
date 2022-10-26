<template>
  <div class="problem">
    <Panel :title="title">
      <el-form ref="form" :model="problemCategory" :rules="rules" label-position="top" label-width="70px">
        <el-row :gutter="20">
          <el-col :span="18">
            <el-form-item prop="title" :label="$t('m.Title')" required>
              <el-input :placeholder="$t('m.Title')" v-model="problemCategory.title"></el-input>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="24">
            <el-form-item prop="input_description" :label="설명" required>
              <Simditor v-model="problemCategory.description"></Simditor>
            </el-form-item>
          </el-col>
        </el-row>
        
        <el-autocomplete
          icon="el-icon-search"
          size="medium"
          placeholder="문제 제목 검색"
          v-model="problemInput"
          @keyup.enter.native="addProblem"
          @select="addProblem"
          :fetch-suggestions="problemquerySearch">
        </el-autocomplete>

        <el-table
        v-loading="loading"
        element-loading-text="loading"
        ref="table"
        :data="problemList"
        style="width: 100%">
        <el-table-column
          width="100"
          prop="id"
          label="ID">
        </el-table-column>
        <el-table-column
          width="150"
          label="Display ID">
          <template slot-scope="{row}">
            <span v-show="!row.isEditing">{{row._id}}</span>
            <el-input v-show="row.isEditing" v-model="row._id">

            </el-input>
          </template>
        </el-table-column>
        <el-table-column
          prop="title"
          label="문제 제목">
          <template slot-scope="{row}">
            <span v-show="!row.isEditing">{{row.title}}</span>
            <el-input v-show="row.isEditing" v-model="row.title">
            </el-input>
          </template>
        </el-table-column>
        <el-table-column
          prop="created_by.username"
          label="작성자">
        </el-table-column>
        <el-table-column
          width="200"
          prop="create_time"
          label="작성일">
          <template slot-scope="scope">
            {{scope.row.create_time | localtime }}
          </template>
        </el-table-column>
        <el-table-column
          fixed="right"
          label="삭제"
          width="250">
          <div slot-scope="scope">
            <icon-btn icon="trash" name="문제 삭제"
                      @click.native="deleteProblem(scope.$index)"></icon-btn>
          </div>
        </el-table-column>
      </el-table>
        <save class="save-btn" @click.native="submit()">저장</save>
      </el-form>
    </Panel>
  </div>
</template>

<script>
  import Simditor from '../../components/Simditor'
  import api from '../../api'
  import {mapGetters} from 'vuex'
  export default {
    name: 'ProblemCategory',
    components: {
      Simditor
    },
    data () {
      return {
        rules: {
          title: {required: true, message: '제목을 입력해주세요', trigger: 'blur'},
          description: {required: true, message: '설명란은 비울 수 없습니다.', trigger: 'blur'}
        },
        problemCategory: {
          id: '',
          title: '',
          description: '',
          problems: []
        },
        problemList: [],
        routeName: '',
        problemInput: '',
        categoryId: ''
      }
    },
    computed: {
      ...mapGetters(['isSuperAdmin'])
    },
    mounted () {
      this.routeName = this.$route.name
      if (this.routeName === 'edit-problem-category') {
        this.mode = 'modify' // 수정
      }
      this.init()
    },
    methods: {
      init () {
        if (this.mode === 'modify') {
          this.categoryId = this.$route.params.categoryId
          api.getProblemListByCategoryId(this.categoryId).then(res => {
            let category = res.data.data
            this.problemCategory.id = category.id
            this.problemCategory.title = category.title
            this.problemCategory.description = category.description
            this.problemList = category.problem_list
            this.problemCategory.problems = category.problems
            this.problemAllList = category.problem_list
          })
        }
      },
      submit () {
        if (this.problemList.length === '' || this.problemList.length < 1 || this.problemList.length < '1') {
          this.$error('최소 한 개 이상의 문제가 존재해야 합니다.')
        } else {
          let data = Object.assign({}, this.problemCategory)
          if (this.mode === 'modify') {
            api.modifyProblemCategory(data).then(res => {
              this.$success('success!!')
              this.$router.push({name: 'problem-category-list'}).catch(() => {})
            })
          } else {
            api.createProblemCategory(data).then(res => {
              this.$success('success!!')
              this.$router.push({name: 'problem-category-list'}).catch(() => {})
            })
          }
        }
      },
      problemquerySearch (queryString, cb) {
        api.searchProblemList({ keyword: queryString }).then(res => {
          let ProblemList = []
          for (let problem of res.data.data) {
            ProblemList.push({value: problem.title})
          }
          cb(ProblemList)
        }).catch(() => {
        })
      },
      addProblem () {
        let title = this.problemInput
        let flag = true
        for (let problem of this.problemList) {
          if (problem.title === title) {
            flag = false
          }
        }
        if (title && flag) {
          api.addProblem(title).then(res => {
            this.problemList.push(res.data.data)
            this.problemCategory.problems.push(res.data.data.id)
          })
        }
        this.problemInput = ''
        this.problemCategory.problemListLength = this.problemList.length
      },
      deleteProblem (index) {
        this.problemList.splice(index, 1)
        this.problemCategory.problems.splice(index, 1)
        this.problemCategory.problemListLength = this.problemList.length
      }
    }
  }
</script>

<style lang="less" scoped>
  .problem {
    .difficulty-select {
      width: 120px;
    }
    .spj-radio {
      margin-left: 10px;
      &:last-child {
        margin-right: 20px;
      }
    }
    .input-new-tag {
      width: 78px;
    }
    .button-new-tag {
      height: 24px;
      line-height: 22px;
      padding-top: 0;
      padding-bottom: 0;
    }
    .tags {
      .el-tag {
        margin-right: 10px;
      }
    }
    .add-samples {
      width: 100%;
      background-color: #fff;
      border: 1px dashed #aaa;
      outline: none;
      cursor: pointer;
      color: #666;
      height: 35px;
      font-size: 14px;
      &:hover {
        background-color: #f9fafc;
      }
      i {
        margin-right: 10px;
      }
    }
    .add-sample-btn {
      margin-bottom: 10px;
    }
    .save-btn {
      margin-top: 10px;
    }
  }
</style>

<style>
  .problem-tag-poper {
    width: 200px !important;
  }
  .dialog-compile-error {
    width: auto;
    max-width: 80%;
    overflow-x: scroll;
  }
</style>
