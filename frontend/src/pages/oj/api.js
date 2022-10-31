import Vue from 'vue'
import store from '@/store'
import axios from 'axios'

Vue.prototype.$http = axios
axios.defaults.baseURL = '/api'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'
axios.defaults.xsrfCookieName = 'csrftoken'

export default {
  createReview (content, articleid, star) {
    return ajax('create_review', 'get', {
      data: {
        content,
        articleid,
        star
      }
    })
  },
  getReviewList (articleid) {
    return ajax('review_list', 'get', {
      articleid
    })
  },
  getInactiveTime () {
    return ajax('get_inactive_time', 'get')
  },
  getGrassList () {
    return ajax('get_grass_data', 'get')
  },
  callAuthEmail (data) {
    return ajax('auth_email_call', 'post', {
      data
    })
  },
  authEmail (email, token) {
    return ajax('authed_email', 'post', {
      data: {
        email,
        token
      }
    })
  },
  getProblemPercent (categoryId) {
    return ajax('percent', 'get', {
      params: {
        category_id: categoryId
      }
    })
  },
  getProblemCategoryList (offset, limit, params) {
    params.limit = limit
    params.offset = offset
    return ajax('categories', 'get', {
      params
    })
  },
  getReadNotification () {
    return ajax('read_notification', 'get')
  },
  deleteNotification (notificationID) { // 알림 삭제
    return ajax('delete_notification', 'get', {
      params: {
        notification_id: notificationID
      }
    })
  },
  checkNotification (notificationID) { // 알림 확인
    return ajax('check_notification', 'get', {
      params: {
        notification_id: notificationID
      }
    })
  },
  getNotificationList () {
    return ajax('notification_list', 'get')
  },
  modifyComment (data) { // 댓글 수정
    return ajax('modify_comment', 'post', {
      data
    })
  },
  likeArticle (articleID) { // 게시글 좋아요
    return ajax('like_article', 'get', {
      params: {
        article_id: articleID // 게시글 ID 전송
      }
    })
  },
  deleteComment (commentID) { // 댓글 삭제
    return ajax('delete_comment', 'get', {
      params: {
        id: commentID // 게시글 ID 전송
      }
    })
  },
  createComment (data) { // 댓글 작성
    return ajax('create_comment', 'post', {
      data
    })
  },
  modifyArticle (title, content, id) { // 게시글 수정
    return ajax('modify_article', 'post', {
      data: {
        title, // 게시글 제목
        content, // 게시글 내용
        id // 게시글 ID
      }
    })
  },
  deleteArticle (articleID) { // 게시글 삭제
    return ajax('delete_article', 'get', {
      params: {
        article_id: articleID // 게시글 ID 전송
      }
    })
  },
  getArticle (articleID) { // 게시글 detail
    return ajax('article', 'get', {
      params: {
        article_id: articleID // 게시글 ID 전송
      }
    })
  },
  createArticle (data) { // 게시글 생성
    return ajax('create_article', 'post', {
      data // title, content, boardtype 데이터 전송
    })
  },
  getArticleList (offset, limit, params) { // 게시글 목록
    params.limit = limit
    params.offset = offset
    return ajax('article_list', 'get', {
      params // myself, username, page, boardtype 데이터 전송
    })
  },
  getCommentArticleList (offset, limit, params) { // 게시글 목록
    params.limit = limit
    params.offset = offset
    return ajax('comment_article_list', 'get', {
      params // myself, username, page, boardtype 데이터 전송
    })
  },
  getLikeArticleList (offset, limit, params) { // 게시글 목록
    params.limit = limit
    params.offset = offset
    return ajax('like_article_list', 'get', {
      params // myself, username, page, boardtype 데이터 전송
    })
  },
  applyVerifyEmail (data) {
    return ajax('apply_verify_email', 'post', {
      data
    })
  },
  verifyEmail (data) {
    return ajax('verify_email', 'post', {
      data
    })
  },
  getWebsiteConf (params) {
    return ajax('website', 'get', {
      params
    })
  },
  getAnnouncementList (offset, limit) {
    let params = {
      offset: offset,
      limit: limit
    }
    return ajax('announcement', 'get', {
      params
    })
  },
  login (data) {
    return ajax('login', 'post', {
      data
    })
  },
  checkUsernameOrEmail (username, email) {
    return ajax('check_username_or_email', 'post', {
      data: {
        username,
        email
      }
    })
  },
  register (data) {
    return ajax('register', 'post', {
      data
    })
  },
  logout () {
    return ajax('logout', 'get')
  },
  getCaptcha () {
    return ajax('captcha', 'get')
  },
  getUserInfo (username = undefined) {
    return ajax('profile', 'get', {
      params: {
        username
      }
    })
  },
  updateProfile (profile) {
    return ajax('profile', 'put', {
      data: profile
    })
  },
  freshDisplayID (userID) {
    return ajax('profile/fresh_display_id', 'get', {
      params: {
        user_id: userID
      }
    })
  },
  twoFactorAuth (method, data) {
    return ajax('two_factor_auth', method, {
      data
    })
  },
  tfaRequiredCheck (username) {
    return ajax('tfa_required', 'post', {
      data: {
        username
      }
    })
  },
  getSessions () {
    return ajax('sessions', 'get')
  },
  deleteSession (sessionKey) {
    return ajax('sessions', 'delete', {
      params: {
        session_key: sessionKey
      }
    })
  },
  applyResetPassword (data) {
    return ajax('apply_reset_password', 'post', {
      data
    })
  },
  resetPassword (data) {
    return ajax('reset_password', 'post', {
      data
    })
  },
  changePassword (data) {
    return ajax('change_password', 'post', {
      data
    })
  },
  deleteAccount (data) {
    return ajax('delete_account', 'post', {
      data
    })
  },
  changeEmail (data) {
    return ajax('change_email', 'post', {
      data
    })
  },
  getLanguages () {
    return ajax('languages', 'get')
  },
  getProblemTagList () {
    return ajax('problem/tags', 'get')
  },
  getProblemList (offset, limit, searchParams) {
    let params = {
      paging: true,
      offset,
      limit
    }
    Object.keys(searchParams).forEach((element) => {
      if (searchParams[element]) {
        params[element] = searchParams[element]
      }
    })
    return ajax('problem', 'get', {
      params: params
    })
  },
  pickone () {
    return ajax('pickone', 'get')
  },
  getProblem (problemID) {
    return ajax('problem', 'get', {
      params: {
        problem_id: problemID
      }
    })
  },
  getContestList (offset, limit, searchParams) {
    let params = {
      offset,
      limit
    }
    if (searchParams !== undefined) {
      Object.keys(searchParams).forEach((element) => {
        if (searchParams[element]) {
          params[element] = searchParams[element]
        }
      })
    }
    return ajax('contests', 'get', {
      params
    })
  },
  getContest (id) {
    return ajax('contest', 'get', {
      params: {
        id
      }
    })
  },
  getContestAccess (contestID) {
    return ajax('contest/access', 'get', {
      params: {
        contest_id: contestID
      }
    })
  },
  checkContestPassword (contestID, password) {
    return ajax('contest/password', 'post', {
      data: {
        contest_id: contestID,
        password
      }
    })
  },
  getContestAnnouncementList (contestId) {
    return ajax('contest/announcement', 'get', {
      params: {
        contest_id: contestId
      }
    })
  },
  getContestProblemList (contestId) {
    return ajax('contest/problem', 'get', {
      params: {
        contest_id: contestId
      }
    })
  },
  getContestProblem (problemID, contestID) {
    return ajax('contest/problem', 'get', {
      params: {
        contest_id: contestID,
        problem_id: problemID
      }
    })
  },
  submitCode (data) {
    return ajax('submission', 'post', {
      data
    })
  },
  getSubmissionList (offset, limit, params) {
    params.limit = limit
    params.offset = offset
    return ajax('submissions', 'get', {
      params
    })
  },
  getContestSubmissionList (offset, limit, params) {
    params.limit = limit
    params.offset = offset
    return ajax('contest_submissions', 'get', {
      params
    })
  },
  getSubmission (id) {
    return ajax('submission', 'get', {
      params: {
        id
      }
    })
  },
  getSafeSubmissionStatus (id) {
    return ajax('safe_submission_status', 'get', {
      params: {
        id
      }
    })
  },
  getSubmissionStatus (id) {
    return ajax('submission_status', 'get', {
      params: {
        id
      }
    })
  },
  submissionExists (problemID) {
    return ajax('submission_exists', 'get', {
      params: {
        problem_id: problemID
      }
    })
  },
  submissionRejudge (id) {
    return ajax('admin/submission/rejudge', 'get', {
      params: {
        id
      }
    })
  },
  updateSubmission (data) {
    return ajax('submission', 'put', {
      data
    })
  },
  getUserRank (offset, limit, rule = 'acm') {
    let params = {
      offset,
      limit,
      rule
    }
    return ajax('user_rank', 'get', {
      params
    })
  },
  getContestRank (params) {
    return ajax('contest_rank', 'get', {
      params
    })
  },
  getACMACInfo (params) {
    return ajax('admin/contest/acm_helper', 'get', {
      params
    })
  },
  updateACInfoCheckedStatus (data) {
    return ajax('admin/contest/acm_helper', 'put', {
      data
    })
  }
}

/**
 * @param url
 * @param method get|post|put|delete...
 * @param params like queryString. if a url is index?a=1&b=2, params = {a: '1', b: '2'}
 * @param data post data, use for method put|post
 * @returns {Promise}
 */
function ajax (url, method, options) {
  if (options !== undefined) {
    var {params = {}, data = {}} = options
  } else {
    params = data = {}
  }
  return new Promise((resolve, reject) => {
    axios({
      url,
      method,
      params,
      data
    }).then(res => {
      // API는 정상적으로(status=20x) 반환되며, 오류 유무로 오류를 판단
      if (res.data.error !== null) {
        Vue.prototype.$error(res.data.data)
        reject(res)
        // 백엔드가 로그인으로 반환되면 세션이 유효하지 않으며 현재 로그인한 사용자는 로그아웃해야 함
        if (res.data.data.startsWith('Please login')) {
          this.$router.push({path: '/login'}).catch(() => {})
        }
      } else {
        resolve(res)
        // if (method !== 'get') {
        //   Vue.prototype.$success('Succeeded')
        // }
      }
    }, res => {
      // API 요청 예외, 일반적으로 서버 오류 또는 네트워크 오류
      reject(res)
      Vue.prototype.$error(res.data.data)
    })
  })
}
