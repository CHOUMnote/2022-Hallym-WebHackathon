<template>
  <div class="join">
    <div class="form">
      <Form ref="formRegister" :model="formRegister" :rules="ruleRegister">
        <!-- 회원가입 박스 title-->
        <div class="join_title"><p @click="goHome">COU</p></div>
                
        <div class = "join_edge">
          <FormItem prop="username">
            <p class="form_title">아이디</p>
            <Input class ="login_input" type="text" v-model="formRegister.username" placeholder="아이디를 입력해주세요" size="large" @on-enter="handleRegister">
            </Input>
          </FormItem>
          <FormItem prop="password">
            <p class="form_title">비밀번호 
              <Poptip trigger="hover" content="영문 + 숫자 + 특수문자(@$!%*#?& 중 1개이상)로 구성되어야 합니다" :transfer="true" placement="right-start">
                <i class="mdi mdi-help-circle-outline"></i>
              </Poptip>
              <span style="float:right">
              <Checkbox v-model="showpassword">비밀번호 보기</Checkbox>
              </span>
            </p>
            <Input v-if="showpassword" class ="login_input" type="text" v-model="formRegister.password" placeholder="비밀번호를 입력해주세요" size="large" @on-enter="handleRegister">
            </Input>
            <Input v-else class ="login_input" type="password" v-model="formRegister.password" placeholder="비밀번호를 입력해주세요" size="large" @on-enter="handleRegister"></Input>
          </FormItem>
          <FormItem prop="passwordAgain">
            <p class="form_title">비밀번호 확인</p>
            <Input class ="login_input" type="password" v-model="formRegister.passwordAgain" placeholder="비밀번호를 다시 한 번 입력해주세요" size="large" @on-enter="handleRegister">
            </Input>
          </FormItem>
          <!-- <FormItem prop="email">
            <p class="form_title">이메일</p>
            <Input v-if="!authModal && !isAuthed" class ="login_input" type="email" v-model="formRegister.email" placeholder="이메일을 입력해주세요" size="large" @on-enter="handleRegister">
            </Input>
            <Input v-else class ="login_input" type="email" v-model="formRegister.email" placeholder="이메일을 입력해주세요" size="large" disabled>
            </Input>
            <div v-if="!authModal">
              <Button v-if="isAuthed" type="primary" class="auth_email_btn" @click="editEmail">이메일 재입력</Button>
              <Button v-else-if="authButton" type="primary" class="auth_email_btn" @click="callAuthEmail" :loading="authButtonLoading">
                <span v-if="!authButtonLoading">인증코드발송</span>
                <span v-else="authButtonLoading">Loading...</span>
              </Button>
              <Button v-else type="primary" class="auth_email_btn" :loading="authButtonLoading" disabled>
              인증코드발송
              </Button>
            </div>
            <div v-else>
              <Button type="primary" class="auth_email_btn" @click="editEmail">이메일 재입력</Button>
            </div>
          </FormItem>
          <transition name="slide-fade" mode="out-in">
            <div v-if="authModal" class="auth_form">
              <div class="input">
                <Input type="text" v-model="authCode" placeholder="인증 코드" size="large" @on-enter="handleRegister">
                </Input>
              </div>
              <Button class="auth-btn" type="primary" @click="authEmail">인증확인</Button>
            </div>
          </transition> -->
          <FormItem prop="captcha">
            <p class="form_title">Captcha</p>
            <div class="oj-captcha">
              <div class="oj-captcha-code">
                <Input v-model="formRegister.captcha" :placeholder="$t('m.Captcha')" size="large" @on-enter="handleRegister">
                </Input>
              </div>
              <div class="oj-captcha-img">
                <Tooltip content="Click to refresh" placement="top">
                  <img :src="captchaSrc" @click="getCaptchaSrc"/>
                </Tooltip>
              </div>
            </div>
          </FormItem>
          <FormItem>
            <div class="login_btn">
              <Button 
                type="primary"
                @click="handleRegister"
                class="primary btn register_btn" v-if="website.allow_register" long
                :loading="btnRegisterLoading">
                회원가입
              </Button>
            </div>
          </FormItem>
        </div>
      </Form>
      <div class="join_foot" @click="goLogin"> &#60; 로그인 페이지</div>
    </div>
  </div>
</template>

<script>
  import { mapGetters, mapActions } from 'vuex'
  import api from '@oj/api'
  import { FormMixin } from '@oj/components/mixins'
  import InfoCard from '@admin/components/infoCard.vue'
  export default {
    mixins: [FormMixin],
    components: {
      InfoCard
    },
    mounted () {
      this.getCaptchaSrc()
    },
    data () {
      const regExp = /(?=^.{3,20}$)^[a-z]+[a-z0-9]$/
      const blockAdminRegExp = /^(admin|user|root|gm|unknownuser|help)/i
      const passregex = /^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$/
      const CheckUsernameNotExist = (rule, value, callback) => {
        if (regExp.test(value)) {
          callback(new Error('4 ~ 20자리 소문자 + 숫자 조합만 가능합니다'))
        } else if (blockAdminRegExp.test(value)) {
          callback(new Error('생성할 수 없는 이름입니다'))
        } else {
          api.checkUsernameOrEmail(value, undefined).then(res => {
            if (res.data.data.username === true) {
              callback(new Error('이미 존재하는 아이디입니다'))
            } else {
              callback()
            }
          }, _ => callback())
          callback()
        }
      }
      // const CheckEmailNotExist = (rule, value, callback) => {
      //   api.checkUsernameOrEmail(undefined, value).then(res => {
      //     callback()
      //     // if (rfalse) {
      //     //   callback(new Error(this.$i18n.t('m.The_email_already_exists')))
      //     // } else {
      //     //   callback()
      //     // }
      //   }, _ => callback())
      // }
      const CheckPassword = (rule, value, callback) => {
        if (this.formRegister.password !== '') {
          console.log(value)
          console.log(passregex.test(value))
          console.log(passregex.test(value))
          if (passregex.test(value) === false) {
            callback(new Error('영문 + 숫자 + 특수문자(@$!%*#?& 중 1개이상)로 구성되어야 합니다'))
          } else {
            // 두 번째 비밀번호 상자를 다시 확인
            this.$refs.formRegister.validateField('passwordAgain')
          }
        }
        callback()
      }

      const CheckAgainPassword = (rule, value, callback) => {
        if (value !== this.formRegister.password) {
          callback(new Error(this.$i18n.t('m.password_does_not_match')))
        }
        callback()
      }

      return {
        btnRegisterLoading: false,
        authCode: '',
        authButton: false,
        authButtonLoading: false,
        authModal: false,
        isAuthed: true,
        showpassword: false,
        formRegister: {
          username: '',
          password: '',
          passwordAgain: '',
          email: Math.floor((Math.random() * 1000)) + '@nav.com',
          captcha: ''
        },
        ruleRegister: {
          username: [
            {required: true, trigger: 'blur', message: '아이디를 입력해주세요'},
            {validator: CheckUsernameNotExist, trigger: 'blur'}
          ],
          email: [
            {required: false, type: 'email', trigger: 'blur', message: '이메일을 입력해주세요'},
            {validator: true, trigger: 'blur', message: '이미 사용 된 이메일입니다'}
          ],
          password: [
            {required: true, trigger: 'blur', message: '8~20자 사이로 입력해주세요', min: 8, max: 20},
            {validator: CheckPassword, trigger: 'blur'}
          ],
          passwordAgain: [
            {required: true, validator: CheckAgainPassword, message: '비밀번호가 일치하지 않습니다', trigger: 'change'}
          ],
          captcha: [
            {required: true, trigger: 'blur', message: '일치하지 않습니다', min: 1, max: 10}
          ]
        }
      }
    },
    methods: {
      ...mapActions(['getProfile']),
      showpasswordBtn () {
        if (this.showpassword) {
          return 'text'
        } else {
          return 'password'
        }
      },
      handleRegister () {
        if (!this.isAuthed) {
          console.log('이메일 인증')
        } else {
          this.validateForm('formRegister').then(valid => {
            let formData = Object.assign({}, this.formRegister)
            delete formData['passwordAgain']
            this.btnRegisterLoading = true
            api.register(formData).then(res => {
              this.$success(this.$i18n.t('m.Thanks_for_registering'))
              this.btnRegisterLoading = false
              this.$router.push({path: '/login'}).catch(() => {})
            }, _ => {
              this.getCaptchaSrc()
              this.formRegister.captcha = ''
              this.btnRegisterLoading = false
            })
          })
        }
      },
      callAuthEmail () {
        setTimeout(() => this.convertStatusAuthButtonLoading(), 0)
        setTimeout(() => this.authPass(), 1000)
      },
      convertStatusAuthButtonLoading () {
        this.authButtonLoading = true
      },
      deconvertStatusAuthButtonLoading () {
        this.authButtonLoading = false
      },
      authPass () {
        let formData = Object.assign({}, this.formRegister)
        delete formData['passwordAgain']
        delete formData['password']
        delete formData['username']
        delete formData['captcha']
        api.callAuthEmail(formData).then(res => {
          this.$success('성공적으로 이메일이 전송되었습니다.')
          this.authModal = true
          setTimeout(() => this.deconvertStatusAuthButtonLoading(), 500)
        }, err => {
          console.log(err)
          this.$error('이메일 전송이 실패하였습니다.')
          setTimeout(() => this.deconvertStatusAuthButtonLoading(), 500)
        })
      },
      authEmail () {
        api.authEmail(this.formRegister.email, this.authCode).then(res => {
          this.isAuthed = true
          this.authModal = false
          this.$success('인증 성공')
        }, _ => {
        })
      },
      editEmail () {
        this.isAuthed = false
        this.authModal = false
      },
      goHome () {
        this.$router.push({path: '/'}).catch(() => {})
      },
      goLogin () {
        this.$router.push({path: '/login'}).catch(() => {})
      }
    },
    computed: {
      ...mapGetters(['website'])
    },
    watch: {
      'formRegister.email' (newVal) {
        this.formRegister.email = newVal
        this.$refs.formRegister.validateField('email', valid => {
          if (valid) {
            this.authButton = false
          } else {
            this.authButton = true
          }
        }, _ => {
          this.authButton = false
        })
      }
    }
  }
</script>
<style lang="less">
.ivu-form-item {
  margin-bottom: 15px;
}
.auth_form {
  display: -webkit-box; /* ios 6이하, 사파리 3.1 */
  display: -moz-box; /* 파이어폭스 19 이하 */
  display: -ms-flexbox; /* IE 10 */
  display: -webkit-flex; /* 웹킷 구 버전*/
  display: flex;
  flex-wrap: nowrap;
  -webkit-box-pack: justify;
  -ms-flex-pack: justify;
  justify-content: space-between;
  width: 100%;
  height: 36px;

  &.input {
    -webkit-box-flex: 1;
    -ms-flex: auto;
    flex: auto;
  }
  .auth-btn {
    margin-left: 10px !important;
    padding: 3px !important;
    -webkit-box-flex: initial;
    -ms-flex: initial;
    flex: initial;
    font-weight: bold;
  }
}
</style>
<style scoped lang="less">
@import '../../../../styles/common.less';

.fade-enter {
  opacity: 0;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.5s ease-out;
}

.fade-leave-to {
  opacity: 0;
}

.slide-fade-enter {
  transform: translateY(-10px);
  opacity: 0;
}

.slide-fade-enter-active,
.slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}
.join {
  display: -webkit-box; /* ios 6이하, 사파리 3.1 */
  display: -moz-box; /* 파이어폭스 19 이하 */
  display: -ms-flexbox; /* IE 10 */
  display: -webkit-flex; /* 웹킷 구 버전*/
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 800px;
  height: calc(~"100vh - 80px");

}


@media screen and (max-width: 1200px) {
  .join {
    margin: 0px -50px -100px -50px;
    position: relative;
  }
}

@media screen and (max-height: 900px) {
  .join {
    margin: 60px -50px -100px -50px;
    position: relative;
    .form {
      .join_edge {
        padding: 0px 14px 30px;
      }
    }
  }
}

@media screen and (min-width: 1200px) {
  .join {
    margin: 0px -50px -100px -50px;
  }
}

.nav {
  top: -80px;
  position: absolute;
}
.image{
  display: block;
  left: -20px;
  top: 0px;
  width: 100%;
  height: 60vh;
  background-color: rgb(39, 39, 39);
  color: white;
  font-size: 36px;
  font-weight: bold;
}
.form {
  display: inline-block;
  background-color: @white;
  box-shadow: 2px 5px 20px 2px rgba(90, 82, 128, 0.31);
  border-radius: @size-border-radius;
  padding: 20px;
  width: 40vw;
  height: 700px;  // 소수점으로 떨어지는 높이를 730px로 고정
  max-width: 500px;
  min-width: 350px; // width가 강제적으로 줄어드는걸 방지
  margin-top: 60px;
  margin-bottom: 60px;
  overflow: auto;
  .btn {
    margin: 0 0 0 0;
    &:last-child {
      margin: 30px 0 30px 0;
    }
  }
  .auth_email_btn {
    margin-top: 5px;
    border: none;
    background: @purple;
    font-weight: bold;
    float:right;
    color: white
  }
}

/* 회원가입 박스의 Coding Platform Dev title css */
.join_title{
  width: 100%;
  height: 13%;
  margin: 30px 0;
  background: @white;
  padding: 0px;
  text-align: center;
  font-size: @font-large;
  font-weight: @weight-bold;
  line-height: 50px;
  color: @purple;
  p {
    display:inline-block;
    cursor: pointer;
    margin: 0 auto;
  }
}

/* 회원가입 입력 박스 css */
.join_edge{
  // margin-top: 10px;
  padding: 0px 50px 30px;
  background-color: @white;
  .form_title {
    font-size: @font-micro;
    font-weight: bold;
    color: @purple;
  }
}


/* 로그인 입력 textbox css */
.login_input {
  text-justify: center;
  font-size: 18px;
}

/* 로그인 상태 유지 checkbox css */
.login_check{
  text-align: left;
}

.register_btn {
  margin-top: 20px;
}

.btn {
  border: none;
  border-radius: @size-border-radius;
  text-justify: center;
  padding: 12px 0;
  color: white;
  font-size: @font-small;
  font-weight: bold;
  &.primary {
    background: @purple;
  }
  &.second {
    background: @light-gray;
    color: @gray;
  }
}

/* 로그인 회원가입하기 & 아이디/비밀번호 찾기 */
.join_foot {
  color: @gray;
  font-weight: @weight-bold;
  &:hover {
    cursor: pointer;
  }
}

.footer {
    background-color: @black;
    position: relative;
    left: 0;
    bottom: 0;
    width: 100%;
    height: 10vh;
    text-align: center;
    font-size: small;
  }

</style>
