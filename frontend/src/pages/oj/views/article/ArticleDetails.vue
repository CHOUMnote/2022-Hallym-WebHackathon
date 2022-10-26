<template>
  <div class="articles-container">
    
    <Panel shadow>
      <!-- 게시글 제목 -->
      <div slot="title" style="font-size: 1.5em; height: 63px; line-height: 63px;">
        <!-- 뒤로가기 버튼 -->
        <i id="back-button" class="mdi mdi-arrow-u-left-bottom" @click="goBack" ></i>
        <!-- <Button id="back-button" icon="md-arrow-back" size="large" @click="goBack" type="text"></Button> -->
        {{article.title}}
      </div>
      
      <!-- 게시글 정보 및 버튼 -->
      <div slot="extra">

        <!-- 게시글 수정 버튼(작성자만 보임) -->
        <Button v-if="is_writer" type="primary" icon="md-create" @click="goModify" class="modify-button"></Button>

        <!-- 게시글 삭제 버튼(작성자만 보임) -->
        <Button v-if="is_writer" type="primary" icon="md-trash" @click="deletemodal=true" class="delete-button"></Button>
        <Modal v-model="deletemodal">
          <p slot="header" style="color:red">경고</p>
          <p>게시물을 삭제합니다.</p>
          <div slot="footer" class="slotWrapper">
            <Button @click="articleDeleteModalClosed">취소</Button>
            <Button type="primary" @click="ok">확인</Button>
          </div>
        </Modal>
      </div>

      <!-- 작성자명 및 작성 시간-->
      <div class="user-date">
        <div>
          <img id="user-avatar" :src="profile.avatar"/>
          <div>
            <a @click="goUser"><b>{{username}}</b></a>
            <div id="user-time">{{article.create_time}}</div>
          </div>
        </div>
        <!-- 질문 게시판의 경우 문제 링크 -->
        <div id="problem-id-container" v-if="problemid">
          <Button id="problem-id-btn" type="text" @click="goProblemDetail(problemid)">#{{ problemid }}</Button>
        </div>
      </div>

      <!-- 게시글 내용 -->
      <div>
        <div v-katex v-html="article.content" key="content" class="content-container"></div>
      </div>

      <div style>
        <div>
          <div class="like-comment-section" slot="extra" :v-model="is_liked">
            <!-- 좋아요 버튼 -->
            <Button v-if="!is_liked" icon="ios-heart-outline" :border="false" @click="like" size="large" id="like-button" type="text">{{article.like_count}}</Button>
            <Button v-else icon="ios-heart" :border="false" @click="like" size="large" class="like_button" id="like-button" type="text">{{article.like_count}}</Button>
            <!-- 댓글 버튼 -->
            <Button icon="ios-chatboxes-outline" :border="false" @click="comment" size="large" id="comment-button" type="text">{{article.comment_count}}</Button>
          </div>
        </div>
      </div>
      <!-- 구분선 -->
      <div></div>

      <!-- 댓글 입력 -->
      <div class="comment-section">
        <textarea ref="commentInput" v-model.lazy="formComment.content" placeholder="댓글 입력" class="comment-submit-textarea" @input="resizeInput"></textarea>
        <div class="comment-submit-area">
          <Button id="comment_submit_btn" type="text" icon="ios-paper-plane" @click="commentSubmit"></Button>
        </div>
      </div>
      <!-- float 겹침 방지 (삭제하지마세요) -->
      <div style="clear:both;"></div>
      
      <!-- 댓글 목록 -->

      <div v-for="(comment, index) in comments" :key="comment.id" class="comment-list-box">
        <a :id="'comment'+comment.id" :name="'comment'+comment.id"></a>
            <!-- 사용자 정보영역 -->
              <div class="comment-user-time">
                <div>
                  <img id="user-avatar-2" :src="comment.avatar"/>
                  <div v-if="comment.username === 'UnknownUser'" class="none-linkdiv">
                    <b>알 수 없는 사용자</b>
                  </div>
                  <div v-else class="linkdiv" @click="goCommentUesr(comment.username)">
                    <b>{{ comment.username }}</b>
                  </div>
                </div>
                <div>
                  <!-- 수정 버튼 -->
                  <Button v-if="comment.is_comment_writer" icon="md-create" @click="onModalComment(comment)" class="modify-button smaller"></Button>
                  <!-- 삭제 버튼 -->
                  <Button v-if="comment.is_comment_writer" icon="md-trash"  @click="onDeleteModalComment(comment)" class="delete-button smaller"></Button>
              </div>
              </div>


            <pre v-katex v-html="comment.content" style="overflow: auto;"></pre>
            
            <div id="comment-time">
                {{ comment.create_time }}
            </div>
            <Modal v-model="deletemodalcomment">
              <p slot="header" style="color:#EE2E03">경고</p>
              <p style="font-size:14px">댓글을 삭제하시겠습니까?</p>
              <div slot="footer" class="slotWrapper">
                <Button @click="commentDeleteModalClosed">취소</Button>
                <Button type="primary" @click="commentDeleteOk(deleteComment_id)">확인</Button>
              </div>
            </Modal>

            <!-- 댓글 수정 modal창 -->
            <Modal v-model="commandmodal"
              :mask-closable="false" :fullscreen="fullscreen" :z-index="999">
              <p slot="header" style="color:#5030e5; text-align:center">
                <span>댓글 수정</span>
              </p>
              <div>
                <div class="fullscreen-btn">
                  <Button @click="isFullScreen">{{ fullscreen_btn_text }}</Button>
                </div>
                <Input type="textarea" :rows="8" v-model="tempComment.content"></Input>
              </div>
              <div slot="footer" class="slotWrapper">
                <Button @click="modalClosed">취소</Button>
                <Button type="primary" @click="modifyCommentOk(tempComment)">확인</Button>
              </div>
            </Modal>

      </div>
    </Panel>
  </div>
</template>

<script>
  import api from '@oj/api'
  import time from '@/utils/time'
  export default {
    name: 'ArticleDetails',
    data () {
      return {
        fullscreen_btn_text: '전체 화면',
        fullscreen: false,  // 전체화면 여부
        commandmodal: false,  // 댓글 수정창 modal
        deletemodalcomment: false,  // 댓글 삭제 경고창 modal
        deletemodal: false, // 게시글 삭제 경고창 modal
        is_writer: false, // 현재 보는 게시글의 작성자 여부
        article: { // 게시글 내용 출력용 data
          title: '',
          content: '',
          create_time: '',
          like_count: '',
          comment_count: ''
        },
        formComment: {
          articleid: '',
          content: ''
        },
        comments: [], // 댓글 목록
        articleID: '', // 게시글 ID
        username: '', // 게시글 작성자 명
        profile: {},
        comments_avatars: {}, // Deprecated
        problemid: '',
        deleteComment_id: null, // 댓글 삭제를 위한 임시 value
        tempComment: {  // 댓글 수정을 위한 임시 value
          id: null,
          content: ''
        },
        is_liked: false
      }
    },
    mounted () {
      this.init()
    },
    methods: {
      articleDeleteModalClosed () {
        this.deletemodal = false
      },
      commentDeleteModalClosed () {
        this.deletemodalcomment = false
      },
      modalClosed () {
        this.commandmodal = false
        this.cancel()
      },
      onModalComment (comment) {
        this.tempComment.id = comment.id
        this.tempComment.content = comment.content
        this.commandmodal = true
      },
      onDeleteModalComment (comment) {
        this.deleteComment_id = comment.id
        this.deletemodalcomment = true
      },
      isFullScreen () {
        if (this.fullscreen) {
          this.cancel()
        } else {
          this.fullscreen = true
          this.fullscreen_btn_text = '전체 화면 종료'
        }
      },
      modifyCommentOk (comment) {
        this.modifyComment(comment)
        this.tempComment.id = null
        this.tempComment.content = '' // 수정 완료후 tempComment를 clear
        this.refreshComment()
        this.modalClosed()
      },
      ok () { // 게시글 삭제 button ok call
        this.deleteArticle()
      },
      cancel () {
        this.fullscreen_btn_text = '전체 화면'
        this.fullscreen = false
      },
      commentDeleteOk (comment) { // 댓글 삭제 button ok call
        this.deleteComment(comment)
        this.deletemodalcomment = false
      },
      comment () {
        this.$refs.commentInput.focus()
      },
      convertUTC () {
        this.comments.forEach(element => {
          element.create_time = time.utcToLocal(element.create_time, 'YYYY-MM-DD HH:mm')
        })
      },
      init () {
        this.articleID = this.$route.params.articleID
        api.getArticle(this.articleID).then(res => { // 게시글 ID를 통해 해당 게시글 정보를 가져옴
          let article = res.data.data
          this.article.title = article.title
          this.article.content = article.content
          this.article.create_time = time.utcToLocal(article.create_time, 'YYYY-MM-DD HH:mm')
          this.is_writer = article.is_writer
          this.username = article.username
          api.getUserInfo(this.username).then(res => {
            this.profile = res.data.data
          })
          this.comments = article.comments
          this.is_liked = article.is_liked
          this.article.like_count = article.like_count
          this.article.comment_count = article.comment_count
          this.convertUTC()
          if (article.boardtype === 'QUESTION') {
            this.problemid = article.problemid
          }
        }, () => {
        })
      },
      refreshComment () {
        api.getArticle(this.articleID).then(res => {
          let article = res.data.data
          this.article.title = article.title
          this.article.content = article.content
          this.article.create_time = time.utcToLocal(article.create_time, 'YYYY-MM-DD HH:mm:ss')
          this.is_writer = article.is_writer
          this.username = article.username
          this.comments = article.comments
          this.is_liked = article.is_liked
          this.article.like_count = article.like_count
          this.article.comment_count = article.comment_count
          this.formComment.articleid = ''
          this.formComment.content = ''
          this.$refs['commentInput'].style.height = '90px' // resize comment area
          this.convertUTC()
          if (article.boardtype === 'QUESTION') {
            this.problemid = article.problemid
          }
        })
      },
      resizeInput () {
        let commentInput = this.$refs['commentInput']
        commentInput.style.height = '18px'
        commentInput.style.height = commentInput.scrollHeight + 'px'
      },
      goBack () { // 뒤로 가기 - 게시글 목록으로 이동
        this.$router.push({name: 'article-list'}).catch(() => {})
      },
      goModify () { // 게시글 수정 - 현재 게시글 ID를 전송
        this.$router.push({name: 'modify-article', params: {articleID: this.articleID}}).catch(() => {})
      },
      deleteArticle () { // 게시글 삭제
        api.deleteArticle(this.articleID).then(res => { // 게시글 ID를 전송해 해당 게시글을 삭제함
          this.$Message.error('삭제되었습니다.')
          this.$router.push({name: 'article-list'}).catch(() => {})
        })
      },
      commentSubmit () { // 댓글 작성
        this.formComment.articleid = this.articleID
        api.createComment(this.formComment).then(res => {
          this.$success('생성 완료')
          this.refreshComment()
        })
      },
      deleteComment (commentId) { // 댓글 삭제
        api.deleteComment(commentId).then(res => { // 댓글 ID를 전송해 해당 댓글을 삭제함
          this.$success('삭제되었습니다.')
          this.refreshComment()
          this.deleteComment_id = null
        }, () => {
          this.deleteComment_id = null
        })
      },
      modifyForm (comment) { // 댓글 수정 버튼 클릭 이벤트 리스너 - 댓글 수정 폼 출력
        this.tempComment = comment.content
        if (comment.modify) { // 댓글의 modify값 = 댓글 수정 폼 출력을 위한 변수, true - 보임 / false - 안보임
          this.$set(comment, 'modify', false) // 수정 폼이 보이는 상태에서 버튼 클릭 시 폼을 숨김
        } else {
          this.$set(comment, 'modify', true) // 수정 폼이 안 보이는 상태에서 버튼 클릭 시 폼을 출력
        }
      },
      like () { // 좋아요
        api.likeArticle(this.articleID).then(res => { // 게시글 ID를 전송
          // this.$success(res.data.data)
          this.refreshComment()
        })
      },
      modifyComment (comment) { // 댓글 수정 제출 버튼 클릭 이벤트 리스너
        // let data = {id: comment.id, content: this.modifyContent}
        let data = {id: comment.id, content: comment.content} // 댓글 ID, 새로 작성한 content 데이터 전송
        api.modifyComment(data).then(res => {
          this.$info('수정이 완료되었습니다.')
        }, () => {
          this.$error('Error')
        })
      },
      goUser () {
        this.$router.push(
          {
            name: 'user-home',
            query: {username: this.username}
          }
        ).catch(() => {})
      },
      goCommentUesr (usr) {
        this.$router.push(
          {
            name: 'user-home',
            query: {username: usr}
          }
        ).catch(() => {})
      },
      goProblemDetail (problemid) {
        this.$router.push(
          {
            name: 'problem-details',
            params: {problemID: problemid}
          }
        ).catch(() => {})
      }
    },
    watch: {
      '$route' (newVal, oldVal) {
        console.log(newVal)
        this.articleID = newVal.params.articleID
        this.init()
      }
    }
  }
</script>

<style scoped lang="less">
@import '../../../../styles/common.less';
  .articles-container {
    margin: 0 5% 0 5%;
    //padding-top: 15px;
    li {
      //padding-top: 15px;
      list-style: none;
      //padding-bottom: 15px;
      //margin-left: 20px;
      font-size: 16px;
      //border-bottom: 1px solid rgba(187, 187, 187, 0.5);
      &:last-child {
        border-bottom: none;
      }
    }
    a {
      color: @black;
      //margin-right: 20px;
      &:hover {
        color: @purple;
      }
    }
  }

  .user-date {
    display: flex;
    justify-content: space-between;
    margin: 5px 70px 5px 70px;
    div:nth-of-type(1) {
      display: flex;
      div:nth-of-type(1) {
        display:flex;
        flex-direction: column;
        line-height: 20px;
      }
    }
  }

  #user-avatar {
    height: 40px;
    width: 40px;
    border-radius: 50%;
    // background-color: @purple;
    margin-right: 10px;
    object-fit: cover;
  }

  #user-avatar-2 {
    height: 30px;
    width: 30px;
    border-radius: 50%;
    // background-color: @light-purple;
    margin-right: 10px;
    object-fit: cover;
  }

  #user-time {
    font-size: 10px;
  }

  .like-comment-section {
    padding: 15px 65px;
    background-color: #F9F9F9;
    margin-top: 10px;
  }

  #like-button, #comment-button {
    padding: 0 10px;
    border-radius: 10px;
    border-color: transparent;
    color: @black;
    margin-right: 20px;
    background-color: #e6e6e6;
    &:hover {
      outline: none;
      box-shadow: none;
      background-color: #d2d0d0;
    }
    &:focus {
      outline: none;
      box-shadow: none;
    }
  }

  #back-button {
    // height: 62px;
    font-size: 90%;
    padding: 0px 8px;
    color: @gray;
    transition: all 0.2s ease-in-out;
    &:hover, &:focus {
      color: @orange;
      border-color: transparent;
      box-shadow: 0 0 0 transparent;
    }
  }

  .fullscreen-btn {
    float: right;
    margin-bottom: 18px;
  }

  .comment-user-time {
    line-height: 30px;
    display: flex;
    justify-content: space-between;
    margin: 0 25px;
    div:nth-of-type(1) {
      display: flex;
    }
    div:nth-of-type(2) {
      display: flex;
    }
  }

  .linkdiv {
    float: left;
    //font-size:1.3em;
    margin-right: 15px;
    color: @black;
    cursor: pointer;
  }
  .none-linkdiv {
    float: left;
    //font-size:1.3em;
    margin-right: 15px;
    color: @black;
  }
  #comment-time {
    color: @gray;
    font-size: 10px;
    margin: 0px 65px;
    padding-bottom: 20px;
  }

  .linkdiv:hover {
    color:@purple;
  }
  .content-container {
    margin: 15px 70px 5px 70px;
    white-space: break-spaces;
  }

  .no-article {
    text-align: center;
    font-size: 16px;
  }

  .article-animate-enter-active {
    animation: fadeIn 1s;
  }

  .slotWrapper {
    padding-top: 10px;
    border-top: 1px solid #C4C4C4;
  }

  .comment-submit-textarea {
    border-radius: 3px 3px 0 0;
    width: 100%;
    min-height: 90px;
    height: 90px;
    padding: 10px;
    overflow: hidden;
    resize: none;
    outline: none;
    display: block;
    border-color: #C4C4C4;
    border-bottom-width: 0;
  }
  .comment-section {
    margin-top: 20px;
    padding: 0 25px 15px;
  }
  .comment-list-box {
    margin-top : 10px;
    margin-bottom : 10px;
    border-bottom: 1px solid #f2f2f2;
  }

  #comment_submit_btn {
    margin: -1px -1px -1px auto;
    border-radius: 0 0 3px 0;
    font-size: 1.3em;
    color: @white;
    background-color: @purple;
    border: none;
    &:focus {
      outline: none !important;
      -webkit-box-shadow: none;
      box-shadow: none;
    }
    * > &:focus {
      outline: none !important;
      -webkit-box-shadow: none;
      box-shadow: none;
    }
    * > &:hover {
      color: @white;
      background-color: @light-purple;
      border-color: @light-purple;
    }
    * {
      border: none;
    }
  }

  #problem-id-container {
    line-height: 40px;
    #problem-id-btn {
      padding: 0;
      border-radius: 0;
      font-size: 100%;
      border-color: transparent;
      color: @black;
      background-color: transparent;
      &:hover {
        outline: none;
        box-shadow: none;
        background-color: transparent;
        color: @purple;
      }
      &:focus {
        outline: none;
        box-shadow: none;
        background-color: transparent;
      }
    }
  }

  .comment-submit-area {
    border-radius: 0 0 3px 3px;
    border: 1px solid #C4C4C4;
    margin-bottom: 20px;
    display: flex;
    justify-content: flex-end;
  }

  .like_button {
    &:focus {
      outline: none !important;
      -webkit-box-shadow: none;
      box-shadow: none;
    }
    * > &:focus {
      outline: none !important;
      -webkit-box-shadow: none;
      box-shadow: none;
    }
  }

  pre {
    font-family: 'Manrope', sans-serif;
    margin: 10px 25px 10px 65px;
    white-space: break-spaces;
  }

  .modify-button, .delete-button {
    background-color: transparent;
    padding: 5px 10px;
    border-color: transparent;
    font-size: 120%;
  }

  .modify-button {
    color: @purple;
    &:hover, &:focus {
      color: @light-purple;
      border-color: transparent;
      background-color: transparent;
      box-shadow: 0 0 0 transparent;
    }
  }

  .delete-button {
    color: @red;
    &:hover, &:focus {
      color: #ed856e;
      border-color: transparent;
      background-color: transparent;
      box-shadow: 0 0 0 transparent;
    }
  }

  .smaller {
    font-size: 90%;
  }

</style>
