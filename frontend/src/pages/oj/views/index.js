import ProblemList from './problem/ProblemList.vue'
import Logout from './user/Logout.vue'
import UserHome from './user/UserHome.vue'
import GuardMessage from './user/GuardMessage.vue'
import About from './help/About.vue'
// import Languages from './help/Languages.vue'
import NotFound from './general/404.vue'
import Home from './general/Home.vue'
import Announcements from './general/Announcements.vue'
import AnnouncementList from './general/AnnouncementList.vue'
import Grass from './user/Grass.vue'
// Grouping Components in the Same Chunk
const SubmissionList = () => import(/* webpackChunkName: "submission" */ '@oj/views/submission/SubmissionList.vue')
const SubmissionDetails = () => import(/* webpackChunkName: "submission" */ '@oj/views/submission/SubmissionDetails.vue')

const ACMRank = () => import(/* webpackChunkName: "userRank" */ '@oj/views/rank/ACMRank.vue')
const OIRank = () => import(/* webpackChunkName: "userRank" */ '@oj/views/rank/OIRank.vue')

const ApplyResetPassword = () => import(/* webpackChunkName: "password" */ '@oj/views/user/ApplyResetPassword.vue')
const ResetPassword = () => import(/* webpackChunkName: "password" */ '@oj/views/user/ResetPassword.vue')

const Problem = () => import(/* webpackChunkName: "Problem" */ '@oj/views/problem/Problem.vue')
const ProblemSubmission = () => import(/* webpackChunkName: "Problem" */ '@oj/views/problem/ProblemSubmission.vue')

const ArticleList = () => import('@oj/views/article/ArticleList.vue')
const CreateArticle = () => import('@oj/views/article/CreateArticle.vue')
const Article = () => import('@oj/views/article/ArticleDetails.vue')
const Notification = () => import('@oj/views/article/Notification.vue')
const Join = () => import('@oj/views/preHome/Join.vue')
const Languages = () => import('@oj/views/help/Languages.vue')
const CategoryList = () => import('@oj/views/problem/CategoryList.vue')

export {
  Join, Home, NotFound, Announcements, GuardMessage,
  Logout, UserHome, About, Languages,
  ProblemList, Problem,
  ACMRank, OIRank,
  SubmissionList, SubmissionDetails,
  ApplyResetPassword, ResetPassword,
  ArticleList, CreateArticle, Article, Notification, AnnouncementList, CategoryList,
  Grass,
  ProblemSubmission
}
