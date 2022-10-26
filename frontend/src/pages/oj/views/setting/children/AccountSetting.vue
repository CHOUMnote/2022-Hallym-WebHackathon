<template>
  <div class="setting-main">
    <div class="title-setting">계정 설정</div>
      <div class="left">
        <p class="section-title">{{$t('m.ChangePassword')}}</p>
        <Form class="setting-content" ref="formPassword" :model="formPassword" :rules="rulePassword">
          <div class="field">
            <div class="text-field">현재 비밀번호</div>
            <FormItem class="edit-field" prop="old_password">
              <Input v-model="formPassword.old_password" type="password"></Input>
            </FormItem>
          </div>
          <div class="field">
            <div class="text-field">새 비밀번호</div>
            <FormItem class="edit-field" prop="new_password">
              <Input v-model="formPassword.new_password" type="password"></Input>
            </FormItem>
          </div>
          <div class="field">
            <div class="text-field">새 비밀번호 확인</div>
            <FormItem class="edit-field" prop="again_password">
              <Input v-model="formPassword.again_password" type="password"></Input>
            </FormItem>
          </div>
          <FormItem v-if="visible.tfaRequired" label="Two Factor Auth" prop="tfa_code">
            <Input v-model="formPassword.tfa_code"/>
          </FormItem>
          <FormItem v-if="visible.passwordAlert">
            <Alert type="success">You will need to login again after 5 seconds..</Alert>
          </FormItem>
          <Button class="purple-button" @click="changePassword">{{$t('m.Update_Password')}}</Button>
        </Form>
      </div>

      <!-- <div class="middle separator"></div> -->

      <div class="left">
        <p class="section-title">{{$t('m.ChangeEmail')}}</p>
        <Form class="setting-content" ref="formEmail" :model="formEmail" :rules="ruleEmail">
          <div class="field">
            <div class="text-field">현재 비밀번호</div>
            <FormItem class="edit-field" prop="password">
              <Input v-model="formEmail.password" type="password"></Input>
            </FormItem>
          </div>
          <div class="field">
            <div class="text-field" style="line-height: 100px;">현재 이메일</div>
            <FormItem prob="old_email" class="email-label-container edit-field">
              <label v-if="getStatusEmailAuth" class="verify-label"><Icon type="md-checkmark" />  (인증된 이메일)</label>
              <label v-else="getStatusEmailAuth" class="warning-label"><Icon type="md-information" class="rotate-icon" />  (인증되지 않은 이메일)</label>
              <Input type="text" v-model="getTokenToCheck" disabled></Input>
            </FormItem>
          </div>
          <div class="field">
            <div class="text-field">새 이메일</div>
            <FormItem prop="new_email" class="new-email-container edit-field">
              <Input type="text" v-model="formEmail.new_email"></Input>
            </FormItem>
          </div>
          <FormItem v-if="visible.tfaRequired" label="Two Factor Auth" prop="tfa_code">
            <Input type="text" v-model="formEmail.tfa_code"></Input>
          </FormItem>
          <Button class="purple-button" @click="changeEmail">{{$t('m.ChangeEmail')}}</Button>
          <span>
            <Button v-if="getStatusEmailAuth" type="primary" disabled>인증 된 이메일</Button>
            <Button v-else type="primary" @click="callAuthEmail" :loading="authButtonLoading">
                <span v-if="!authButtonLoading">이메일 인증하기</span>
                <span v-else="authButtonLoading">발송중...</span>
            </Button>
          </span>
          <div class="trans-container">
            <transition name="slide-fade" mode="out-in">
              <div v-if="authModal" class="auth_form">
                <div class="input">
                  <Input type="text" v-model="authCode" placeholder="인증 코드" size="large">
                  </Input>
                </div>
                <Button class="auth-btn" type="primary" @click="authEmail">인증확인</Button>
              </div>
            </transition>
          </div>
        </Form>
      </div>

    
    <div class="setting-delete">
      <div class="left">
        <p class="section-title red-title">{{$t('m.Delete_Account')}}</p>
        <Form class="setting-content" ref="formDelete" :model="formDelete" :rules="ruleDelete">
          <div class="field">
            <div class="text-field red-title">현재 닉네임</div>
            <FormItem class="edit-field" prop="username">
              <Input v-model="formDelete.username" type="text"></Input>
            </FormItem>
          </div>
          <div class="field">
            <div class="text-field red-title">현재 비밀번호</div>
            <FormItem class="edit-field" prop="password">
              <Input v-model="formDelete.password" type="password"></Input>
            </FormItem>
          </div>
          <div class="field">
            <div class="text-field red-title">Captcha</div>
            <FormItem class="edit-field" prop="captcha" style="margin-bottom:30px">
              <div class="oj-captcha">
                <div class="oj-captcha-code">
                  <Input type="text" v-model="formDelete.captcha" size="large" @on-enter="deleteAccount"></Input>
                </div>
                <div class="oj-captcha-img">
                  <Tooltip content="Click to refresh" placement="top">
                    <img :src="captchaSrc" @click="getCaptchaSrc"/>
                  </Tooltip>
                </div>
              </div>
            </FormItem>
          </div>
          <FormItem v-if="visible.tfaRequired" label="Two Factor Auth" prop="tfa_code">
            <Input type="text" v-model="formDelete.tfa_code"/>
          </FormItem>
          <FormItem v-if="visible.accountDelete">
            <Alert type="success">5초후에 자동 로그아웃 됩니다</Alert>
          </FormItem>
          <Button type="primary" class="red-button" @click="deleteAccount">{{$t('m.Delete_Account')}}</Button>
        </Form>
      </div>
    </div>
  </div>
</template>

<script>
  import api from '@oj/api'
  import { FormMixin } from '@oj/components/mixins'
  import {types} from '@/store'
  export default {
    mixins: [FormMixin],
    data () {
      const oldPasswordCheck = [{required: true, trigger: 'blur', min: 6, max: 20}]
      const tfaCheck = [{required: true, trigger: 'change'}]
      const CheckAgainPassword = (rule, value, callback) => {
        if (value !== this.formPassword.new_password) {
          callback(new Error('password does not match'))
        }
        callback()
      }
      const CheckNewPassword = (rule, value, callback) => {
        if (this.formPassword.old_password !== '') {
          if (this.formPassword.old_password === this.formPassword.new_password) {
            callback(new Error('The new password doesn\'t change'))
          } else {
            this.$refs.formPassword.validateField('again_password')
          }
        }
        callback()
      }
      return {
        authCode: '',
        authModal: false,
        authButtonLoading: false,
        loading: {
          btnPassword: false,
          btnEmail: false
        },
        visible: {
          passwordAlert: false,
          emailAlert: false,
          tfaRequired: false,
          accountDelete: false
        },
        formPassword: {
          tfa_code: '',
          old_password: '',
          new_password: '',
          again_password: ''
        },
        formEmail: {
          tfa_code: '',
          password: '',
          old_email: '',
          new_email: ''
        },
        formDelete: {
          username: '',
          tfa_code: '',
          password: '',
          captcha: ''
        },
        rulePassword: {
          old_password: oldPasswordCheck,
          new_password: [
            {required: true, trigger: 'blur', min: 6, max: 20},
            {validator: CheckNewPassword, message: '다른 비밀번호로 변경하세요', trigger: 'blur'}
          ],
          again_password: [
            {required: true, validator: CheckAgainPassword, message: '비밀번호가 일치하지 않습니다', trigger: 'change'}
          ],
          tfa_code: tfaCheck
        },
        ruleEmail: {
          password: oldPasswordCheck,
          new_email: [{required: true, type: 'email', message: '일치하지 않습니다', trigger: 'change'}],
          tfa_code: tfaCheck
        },
        ruleDelete: {
          username: [
            {required: true, trigger: 'blur', message: '아이디를 입력해주세요'}
          ],
          password: oldPasswordCheck,
          captcha: [
            {required: true, trigger: 'blur', message: '일치하지 않습니다', min: 1, max: 10}
          ],
          tfa_code: tfaCheck
        }
      }
    },
    mounted () {
      this.formEmail.old_email = this.$store.getters.user.email || ''
      this.getCaptchaSrc()
    },
    methods: {
      callAuthEmail () {
        setTimeout(() => this.convertStatusAuthButtonLoading(), 0)
        setTimeout(() => this.authPass(), 1000)
      },
      convertStatusAuthButtonLoading () {
        this.authButtonLoading = true
        this.authModal = true
      },
      deconvertStatusAuthButtonLoading () {
        this.authButtonLoading = false
      },
      authPass () {
        let temp = {
          email: this.getTokenToCheck
        }
        let formData = Object.assign({}, temp)
        api.applyVerifyEmail(formData).then(res => {
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
        let temp = {
          token: this.authCode
        }
        let formData = Object.assign({}, temp)
        api.verifyEmail(formData).then(res => {
          this.authModal = false
          this.$success('인증 성공')
          setTimeout(() => {
            api.getUserInfo(this.$store.state.user.username).then(res => {
              setTimeout(() => {
                this.$store.commit(types.CHANGE_PROFILE, {profile: res.data.data})
              }, 100)
            })
          }, 100)
        }, _ => {
        })
      },
      changePassword () {
        this.validateForm('formPassword').then(valid => {
          this.loading.btnPassword = true
          let data = Object.assign({}, this.formPassword)
          delete data.again_password
          if (!this.visible.tfaRequired) {
            delete data.tfa_code
          }
          api.changePassword(data).then(res => {
            this.loading.btnPassword = false
            this.visible.passwordAlert = true
            this.$success('비밀번호가 변경되었습니다')
            setTimeout(() => {
              this.visible.passwordAlert = false
              this.$router.push({name: 'logout'}).catch(() => {})
            }, 5000)
          }, res => {
            if (res.data.data === 'tfa_required') {
              this.visible.tfaRequired = true
            }
            this.loading.btnPassword = false
          })
        })
      },
      changeEmail () {
        this.validateForm('formEmail').then(valid => {
          this.loading.btnEmail = true
          let data = Object.assign({}, this.formEmail)
          if (!this.visible.tfaRequired) {
            delete data.tfa_code
          }
          api.changeEmail(data).then(res => {
            this.loading.btnEmail = false
            this.visible.emailAlert = true
            this.$success('변경되었습니다')
            this.$refs.formEmail.resetFields()
            setTimeout(() => {
              api.getUserInfo(this.$store.state.user.username).then(res => {
                setTimeout(() => {
                  this.$refs.formEmail.old_email = res.data.data.user.email
                  this.$store.commit(types.CHANGE_PROFILE, {profile: res.data.data})
                }, 100)
              })
            }, 100)
          }, res => {
            if (res.data.data === 'tfa_required') {
              this.visible.tfaRequired = true
            }
          })
        })
      },
      deleteAccount () {
        this.validateForm('formDelete').then(valid => {
          this.loading.btnPassword = true
          let data = Object.assign({}, this.formDelete)
          if (!this.visible.tfaRequired) {
            delete data.tfa_code
          }
          api.deleteAccount(data).then(res => {
            this.loading.btnPassword = false
            this.visible.accountDelete = true
            this.$success('탈퇴가 완료되었습니다')
            this.$refs.formDelete.resetFields()
            setTimeout(() => {
              this.visible.accountDelete = false
              this.$router.push({name: 'delete-account'}).catch(() => {})
              this.$router.push({name: 'logout'}).catch(() => {})
            }, 5000)
          }, res => {
            if (res.data.data === 'tfa_required') {
              this.visible.tfaRequired = true
            }
          })
        })
      }
    },
    computed: {
      getTokenToCheck () {
        return this.$store.getters.user.email
      },
      getStatusEmailAuth () {
        return this.$store.getters.user.is_email_verify
      },
      getCurrentEmailAuth () {
        if (this.$store.getters.user.is_email_verify) {
          return 'Current Email'
        } else {
          return 'Current Email (인증되지 않은 이메일)'
        }
      }
    }
  }
</script>
<style lang="less">
  @import '../../../../../styles/common.less';
.new-email-container {
  margin-bottom: 20px;
}
.email-label-container {
  .rotate-icon {
    -webkit-transform: rotate(180deg);
    -moz-transform: rotate(180deg);
    -ms-transform: rotate(180deg);
    -o-transform: rotate(180deg);
    transform: rotate(180deg);
  }
  .ivu-icon {
    margin-right: 5px;
    padding-bottom: 2px;
  }
  .ivu-form-item-label {
    padding-right: 5px;
  }
  .warning-label {
    color: #ff3300;
    .ivu-icon {
      font-size: 20px;
      width: 12px;
      margin-bottom: 2px;
      padding-bottom: 0px;
    }
  }
  .verify-label {
    color: #029302
  }
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
  justify-content: flex-start;
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

  .trans-container {
    margin-top: 10px
  }
  .title-setting {
    font-size: 200%;
    font-weight: 500;
    -webkit-text-stroke: 1px;
    color: @purple;
  }
  .section-title {
    color: @purple;
    font-size: 150%;
    font-weight: 400;
    -webkit-text-stroke: .8px;
    padding-bottom: 3px;
    border-bottom: 1.5px solid @purple;
    margin-bottom: 15px;
  }
  .red-title {
    color: #E1262A;
    border-bottom: 1.5px solid #E1262A;
  }
  .left {
    margin-bottom: 40px;
    .setting-content {
      margin: 0;
      .field {
        display: flex;
        border-bottom: 1px solid @light-gray;
        margin-bottom: 15px;
        .text-field {
          min-width: 150px;
          line-height: 30px;
          font-size: 120%;
          color: @purple;
          font-weight: 500;
          -webkit-text-stroke: .5px;
        }
        .red-title {
          color: #E1262A;
          border: none;
        }
        .edit-field {
          width: 250px;
        }
      }
      .red-button {
        background-color: #E1262A;
        border: none;
        &:focus {
          color: @white;
          box-shadow: none;
          background-color: #af1d1f;
        }
      }
      .purple-button {
        border: 1px solid @purple;
        color: @purple;
        margin-right: 5px;
      }
    }
  }
</style>
