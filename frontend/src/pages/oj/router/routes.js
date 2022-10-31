// all routes here.
import {
  About,
  ACMRank,
  Announcements,
  ApplyResetPassword,
  Languages,
  Home,
  NotFound,
  OIRank,
  Problem,
  ProblemList,
  ResetPassword,
  SubmissionDetails,
  SubmissionList,
  UserHome,
  ArticleList,
  CreateArticle,
  Article,
  Notification,
  AnnouncementList,
  Join,
  CategoryList,
  ProblemSubmission
} from '../views'
import Logout from '../views/user/Logout.vue'
import StartLogin from '../views/preHome/Start_Login.vue'
import MarketDetail from '../views/contest/MarketDetail.vue'

import * as Contest from '@oj/views/contest'
import * as Setting from '@oj/views/setting'

export default [
  {
    name: 'category-list',
    path: '/category-list',
    meta: {title: 'category-list'},
    component: CategoryList
  },
  {
    name: 'notification-list',
    path: '/notification-list',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'notification-list'},
    component: Notification
  },

  {
    name: 'start-login',
    path: '/login',
    meta: {title: 'StartLogin'},
    component: StartLogin
  },
  {
    name: 'join',
    path: '/join',
    meta: {title: 'Join'},
    component: Join
  },
  {
    path: '/article/modify/:articleID',
    name: 'modify-article',
    meta: {title: 'Article Modify'},
    component: CreateArticle
  },
  {
    name: 'article-details',
    path: '/article/:articleID',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Article Details'},
    component: Article
  },
  {
    name: 'article-list',
    path: '/article-list',
    meta: {title: 'Article List'},
    component: ArticleList
  },
  {
    name: 'create-article',
    path: '/create-article',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Create Article'},
    component: CreateArticle
  },
  {
    name: 'home',
    path: '/',
    meta: {title: 'Home'},
    alias: '/main-announcement',
    component: Home
  },
  {
    name: 'announcement-list',
    path: '/announcement-list',
    meta: {title: 'Announcement List'},
    component: AnnouncementList
  },
  {
    name: 'logout',
    path: '/logout',
    meta: {requiresAuth: true, title: 'Logout'},
    component: Logout
  },
  {
    name: 'apply-reset-password',
    path: '/apply-reset-password',
    meta: {title: 'Apply Reset Password'},
    component: ApplyResetPassword
  },
  {
    name: 'reset-password',
    path: '/reset-password/:token',
    meta: {title: 'Reset Password'},
    component: ResetPassword
  },
  {
    name: 'problem-list',
    path: '/problem',
    meta: {title: 'Problem List'},
    component: ProblemList
  },
  {
    name: 'problem-details',
    path: '/problem/:problemID',
    meta: {title: 'Problem Details'},
    component: Problem
  },
  {
    name: 'problem-submission',
    path: '/submission/:problemID',
    meta: {title: 'Problem Submission'},
    component: ProblemSubmission
  },
  {
    name: 'submission-list',
    path: '/status',
    meta: {title: 'Submission List'},
    component: SubmissionList
  },
  {
    name: 'submission-details',
    path: '/status/:id/',
    meta: {requiresAuth: true, isEmailVerify: true, tle: 'Submission Details'},
    component: SubmissionDetails
  },
  {
    name: 'contest-list',
    path: '/market',
    meta: {title: 'Contest List'},
    component: Contest.ContestList
  },
  {
    name: 'market-1',
    path: '/market/1',
    component: MarketDetail
  },
  {
    name: 'market-2',
    path: '/market/2',
    component: MarketDetail
  },
  {
    name: 'market-3',
    path: '/market/3',
    component: MarketDetail
  },
  {
    name: 'market-4',
    path: '/market/4',
    component: MarketDetail
  },
  {
    name: 'market-5',
    path: '/market/5',
    component: MarketDetail
  },
  {
    name: 'market-6',
    path: '/market/6',
    component: MarketDetail
  },
  {
    name: 'market-7',
    path: '/market/7',
    component: MarketDetail
  },
  {
    name: 'contest-details',
    path: '/contest/:contestID/',
    component: Contest.ContestDetails,
    meta: {requiresAuth: true, isEmailVerify: true, title: 'Contest Details'},
    children: [
      {
        name: 'contest-submission-list',
        path: 'submissions',
        component: SubmissionList
      },
      {
        name: 'contest-problem-list',
        path: 'problems',
        component: Contest.ContestProblemList
      },
      {
        name: 'contest-problem-details',
        path: 'problem/:problemID/',
        component: Problem
      },
      {
        name: 'contest-problem-submission',
        path: 'submission/:problemID/',
        component: ProblemSubmission
      },
      {
        name: 'contest-announcement-list',
        path: 'announcements',
        component: Announcements
      },
      {
        name: 'contest-rank',
        path: 'rank',
        component: Contest.ContestRank
      },
      {
        name: 'acm-helper',
        path: 'helper',
        component: Contest.ACMContestHelper
      }
    ]
  },
  {
    name: 'acm-rank',
    path: '/acm-rank',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'ACM Rankings'},
    component: ACMRank
  },
  {
    name: 'oi-rank',
    path: '/oi-rank',
    meta: {requiresAuth: true, isEmailVerify: true, title: 'OI Rankings'},
    component: OIRank
  },
  {
    name: 'user-home',
    path: '/user-home',
    component: UserHome,
    meta: {requiresAuth: true, title: 'User Home'}
  },
  {
    path: '/setting',
    component: Setting.Settings,
    children: [
      {
        name: 'default-setting',
        path: '',
        meta: {requiresAuth: true, title: 'Default Settings'},
        component: Setting.MyPage
      },
      {
        name: 'comment-list',
        path: 'comment',
        meta: {requiresAuth: true, title: 'Comment List'},
        component: Setting.AccountArticleList
      },
      {
        name: 'like-list',
        path: 'like',
        meta: {requiresAuth: true, title: 'Like List'},
        component: Setting.AccountArticleList
      },
      {
        name: 'profile-setting',
        path: 'profile',
        meta: {requiresAuth: true, title: 'Profile Settings'},
        component: Setting.ProfileSetting
      },
      {
        name: 'account-setting',
        path: 'account',
        meta: {requiresAuth: true, title: 'Account Settings'},
        component: Setting.AccountSetting
      },
      {
        name: 'security-setting',
        path: 'security',
        meta: {requiresAuth: true, isEmailVerify: true, title: 'Security Settings'},
        component: Setting.SecuritySetting
      },
      {
        name: 'my-page',
        path: 'mypage',
        meta: {requiresAuth: true, title: 'My Page'},
        component: Setting.MyPage
      }
    ]
  },
  {
    path: '/help',
    name: 'help',
    meta: {title: 'About'},
    component: About
  },
  {
    path: '/languages',
    name: 'languages',
    meta: {title: 'languages'},
    component: Languages
  },
  {
    path: '*',
    meta: {title: '404'},
    component: NotFound
  }
]
