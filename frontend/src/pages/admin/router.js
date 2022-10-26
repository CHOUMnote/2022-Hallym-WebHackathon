import Vue from 'vue'
import VueRouter from 'vue-router'
// intro 구성요소 view\
import { Announcement, Conf, Contest, ContestList, Home, JudgeServer, Login,
  Problem, ProblemList, User, PruneTestCase, Dashboard, ProblemImportOrExport,
  ProblemCategoryList, ProblemCategory, ProblemTagList, ContestImg } from './views'
Vue.use(VueRouter)

export default new VueRouter({
  mode: 'history',
  base: '/admin/',
  scrollBehavior: () => ({y: 0}),
  routes: [
    {
      path: '/login',
      name: 'login',
      component: Login
    },
    {
      path: '/',
      component: Home,
      children: [
        {
          path: '/contest/:contestId/upload-img',
          name: 'upload-img-contest',
          component: ContestImg
        },
        {
          path: '/problem/tags',
          name: 'problem-tags',
          component: ProblemTagList
        },
        {
          path: '/problem/category/:categoryId',
          name: 'edit-problem-category',
          component: ProblemCategory
        },
        {
          path: '/problem/category',
          name: 'problem-category',
          component: ProblemCategory
        },
        {
          path: '/problem/categories',
          name: 'problem-category-list',
          component: ProblemCategoryList
        },
        {
          path: '',
          name: 'dashboard',
          component: Dashboard
        },
        {
          path: '/announcement',
          name: 'announcement',
          component: Announcement
        },
        {
          path: '/user',
          name: 'user',
          component: User
        },
        {
          path: '/conf',
          name: 'conf',
          component: Conf
        },
        {
          path: '/judge-server',
          name: 'judge-server',
          component: JudgeServer
        },
        {
          path: '/prune-test-case',
          name: 'prune-test-case',
          component: PruneTestCase
        },
        {
          path: '/problems',
          name: 'problem-list',
          component: ProblemList
        },
        {
          path: '/problem/create',
          name: 'create-problem',
          component: Problem
        },
        {
          path: '/problem/edit/:problemId',
          name: 'edit-problem',
          component: Problem
        },
        {
          path: '/problem/batch_ops',
          name: 'problem_batch_ops',
          component: ProblemImportOrExport
        },
        {
          path: '/contest/create',
          name: 'create-contest',
          component: Contest
        },
        {
          path: '/contest',
          name: 'contest-list',
          component: ContestList
        },
        {
          path: '/contest/:contestId/edit',
          name: 'edit-contest',
          component: Contest
        },
        {
          path: '/contest/:contestId/announcement',
          name: 'contest-announcement',
          component: Announcement
        },
        {
          path: '/contest/:contestId/problems',
          name: 'contest-problem-list',
          component: ProblemList
        },
        {
          path: '/contest/:contestId/problem/create',
          name: 'create-contest-problem',
          component: Problem
        },
        {
          path: '/contest/:contestId/problem/:problemId/edit',
          name: 'edit-contest-problem',
          component: Problem
        }
      ]
    },
    {
      path: '*', redirect: '/login'
    }
  ]
})
