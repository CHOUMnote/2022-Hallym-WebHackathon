<template>
  <div style="margin: 0px 0px 15px 0px;">
    <div class="header">
      <div class="options">
        <div>
          <div class="status" v-if="statusVisible">
            <template v-if="!this.contestID || (this.contestID && OIContestRealTimePermission)">
              <!-- <span>{{$t('m.Status')}}</span> -->
              <Tag class="result" :color="submissionStatus.color" @click.native="handleRoute('/status/'+submissionId)">
                {{$t('m.' + submissionStatus.text.replace(/ /g, "_"))}}
              </Tag>
            </template>
            <template v-else-if="contestID && !OIContestRealTimePermission">
              <Alert type="success" show-icon>{{$t('m.Submitted_successfully')}}</Alert>
            </template>
          </div>
          <div v-else-if="my_status === 0">
            <Alert type="success" show-icon>{{$t('m.You_have_solved_the_problem')}}</Alert>
          </div>
          <div v-else-if="contestID && !OIContestRealTimePermission && submissionExists">
            <Alert type="success" show-icon>{{$t('m.You_have_submitted_a_solution')}}</Alert>
          </div>
          <div v-if="contestEnded">
            <Alert type="warning" show-icon>{{$t('m.Contest_has_ended')}}</Alert>
          </div>
        </div>
        <div>
          <Tooltip :content="this.$i18n.t('m.Reset_to_default_code_definition')" placement="bottom" style="margin-left: 10px">
              <Button icon="md-refresh" @click="onResetClick" class="reset-btn"></Button>
            </Tooltip>
          <Select :value="theme" @on-change="onThemeChange" class="adjust">
            <Option v-for="item in themes" :key="item.label" :value="item.value">{{item.label}}
            </Option>
          </Select>
          <Select :value="language" 
          @on-change="onLangChange" class="adjust">
            <Option v-for="item in languages" :key="item" :value="item">{{item}}
            </Option>
          </Select>
        </div>
        <!-- <span>{{$t('m.Language')}}:</span> -->
        <!-- 
        <Tooltip :content="this.$i18n.t('m.Upload_file')" placement="top" style="margin-left: 10px">
          <Button icon="ios-cloud-upload-outline" @click="onUploadFile"></Button>
        </Tooltip> -->

        <!-- <input type="file" id="file-uploader" style="display: none" @change="onUploadFileDone"> -->

          <!-- <span>{{$t('m.Theme')}}:</span> -->
      </div>
      <div>
        <codemirror v-model.lazy="value" :options="options" @change="onEditorCodeChange" ref="myEditor">
        </codemirror>
      </div>
    </div>
  </div>
</template>
<script>
  import utils from '@/utils/utils'
  import { codemirror } from 'vue-codemirror-lite'

  // theme
  import 'codemirror/theme/monokai.css'
  import 'codemirror/theme/base16-light.css'
  import 'codemirror/theme/material.css'

  // mode
  import 'codemirror/mode/clike/clike.js'
  import 'codemirror/mode/python/python.js'
  import 'codemirror/mode/go/go.js'
  import 'codemirror/mode/javascript/javascript.js'

  // active-line.js
  import 'codemirror/addon/selection/active-line.js'

  // foldGutter
  import 'codemirror/addon/fold/foldgutter.css'
  import 'codemirror/addon/fold/foldgutter.js'
  import 'codemirror/addon/fold/brace-fold.js'
  import 'codemirror/addon/fold/indent-fold.js'

  import 'codemirror/addon/scroll/simplescrollbars.js'
  import 'codemirror/addon/scroll/simplescrollbars.css'

  export default {
    name: 'SubmitCodeMirror',
    components: {
      codemirror
    },
    props: {
      value: {
        type: String,
        default: ''
      },
      languages: {
        type: Array,
        default: () => {
          return ['C', 'C++', 'Java', 'Python2']
        }
      },
      language: {
        type: String,
        default: 'C++'
      },
      theme: {
        type: String,
        default: 'base16-light'
      },
      my_status: [Number, String],
      statusVisible: Boolean,
      contestID: [Number, String],
      OIContestRealTimePermission: Boolean,
      submissionStatus: [Function, Object],
      submissionId: [Number, String],
      submissionExists: Boolean,
      contestEnded: Boolean
    },
    data () {
      return {
        options: {
          // codemirror options
          tabSize: 2,
          mode: 'text/x-csrc',
          theme: 'base16-light',
          lineNumbers: true,
          line: true,
          // 코드 접기
          foldGutter: true,
          gutters: ['CodeMirror-linenumbers', 'CodeMirror-foldgutter'],
          // 선택한 텍스트가 자동으로 강조 표시되고 강조 표시됩니다.
          styleSelectedText: true,
          lineWrapping: true,
          highlightSelectionMatches: {showToken: /\w/, annotateScrollbar: true},
          scrollbarStyle: 'overlay'
        },
        mode: {
          'C++': 'text/x-csrc'
        },
        themes: [
          {label: this.$i18n.t('m.Monokai'), value: 'monokai'},
          {label: this.$i18n.t('m.Eclipse'), value: 'base16-light'},
          {label: this.$i18n.t('m.Material'), value: 'material'}
        ]
      }
    },
    mounted () {
      utils.getLanguages().then(languages => {
        let mode = {}
        languages.forEach(lang => {
          mode[lang.name] = lang.content_type
        })
        this.mode = mode
        this.editor.setOption('mode', this.mode[this.language])
        this.editor.setSize('100%', '76vh')
      })
      this.editor.focus()
    },
    methods: {
      setHeight (height) {
        this.editor.setSize('100%', height)
      },
      onEditorCodeChange (newCode) {
        this.$emit('update:value', newCode)
      },
      onLangChange (newVal) {
        this.editor.setOption('mode', this.mode[newVal])
        this.$emit('changeLang', newVal)
      },
      onThemeChange (newTheme) {
        this.editor.setOption('theme', newTheme)
        this.$emit('changeTheme', newTheme)
      },
      onResetClick () {
        this.$emit('resetCode')
      },
      onUploadFile () {
        document.getElementById('file-uploader').click()
      },
      onUploadFileDone () {
        let f = document.getElementById('file-uploader').files[0]
        let fileReader = new window.FileReader()
        let self = this
        fileReader.onload = function (e) {
          var text = e.target.result
          self.editor.setValue(text)
          document.getElementById('file-uploader').value = ''
        }
        fileReader.readAsText(f, 'UTF-8')
      },
      handleRoute (route) {
        this.$router.push(route).catch(() => {})
      }
    },
    computed: {
      editor () {
        // get current editor object
        return this.$refs.myEditor.editor
      }
    },
    watch: {
      'theme' (newVal, oldVal) {
        this.editor.setOption('theme', newVal)
      }
    }
  }
</script>

<style lang="less" scoped>
  @import "../../../styles/common.less";
  .header {
    padding: 15px;
    .options {
      display: flex;
      justify-content: space-between;
      margin-bottom: 15px;
    }
    .adjust {
      width: 100px;
      margin-left: 10px;
    }
  }

  .reset-btn {
    background-color: @light-purple;
    color: @white;
    border-color: transparent;
    &:hover, &:focus {
      background-color: @purple;
      transition: background-color .3s ease-in-out;
      box-shadow: none;
    }
  }

  .result {
    -webkit-text-stroke: .3px; 
    font-size: 15px;
    border-width: 2px;
  }
</style>

<style lang="less" scoped>
  @import '../../../styles/common.less';
  /* @media screen and (max-width: 1200px) {
    .CodeMirror-scroll {
      max-height: 67vh;
    }
  } */

  /* @media screen and (min-width: 1200px) {
    .CodeMirror-scroll {
      max-height: 67vh;
    }
  } */

  .CodeMirror-scroll {
    max-height: 1000px;
    /* min-height: 67vh; */
    /* max-height: 67vh; */
  }
</style>
