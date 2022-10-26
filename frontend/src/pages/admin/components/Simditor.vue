<template>
  <textarea ref="editor"></textarea>
</template>

<script>
  import Simditor from 'tar-simditor'
  import 'tar-simditor/styles/simditor.css'
  import 'tar-simditor-markdown'
  import 'tar-simditor-markdown/styles/simditor-markdown.css'
  import './simditor-file-upload'
  
  export default {
    name: 'Simditor',
    props: {
      toolbar: {
        type: Array,
        default: () => ['title', 'bold', 'italic', 'underline', 'color', 'ol', 'ul', 'blockquote', 'code', 'link', 'table', 'image', 'uploadfile', 'hr', 'indent', 'outdent', 'alignment', 'markdown']
      },
      value: {
        type: String,
        default: ''
      }
    },
    data () {
      return {
        editor: null,
        currentValue: this.value
      }
    },
    mounted () {
      Simditor.i18n = {
        'ko-KR': {
          blockquote: '인용구',
          bold: '볼드체',
          code: '코드 블록',
          color: '글꼴 색',
          coloredText: '색상',
          hr: '수평선',
          image: '이미지 삽입',
          externalImage: '외부 이미지 삽입',
          uploadImage: '이미지 업로드',
          uploadFailed: '업로드 실패',
          uploadError: '업로드 중 오류가 발생하였습니다',
          imageUrl: 'URL',
          imageSize: '크기',
          imageAlt: 'Alt',
          restoreImageSize: '원본 사이즈',
          uploading: 'Uploading',
          indent: '들여쓰기',
          outdent: '내어쓰기',
          italic: 'Italic',
          link: '링크 삽입',
          linkText: '대체 글',
          linkUrl: 'URL',
          linkTarget: '페이지보기',
          openLinkInCurrentWindow: '현재 페이지에서 열기',
          openLinkInNewWindow: '새 창에서 열기',
          removeLink: '링크 삭제',
          ol: '숫자 목록',
          ul: '일반 목록',
          strikethrough: '취소선',
          table: '표',
          deleteRow: '행 삭제',
          insertRowAbove: '위에 행 삽입',
          insertRowBelow: '아래에 행 삽입',
          deleteColumn: '열 삭제',
          insertColumnLeft: '왼쪽 열 삽입',
          insertColumnRight: '오른쪽 열 삽입',
          deleteTable: '표 삭제',
          title: '제목',
          normalText: '내용',
          underline: '밑줄',
          alignment: '정렬',
          alignCenter: '가운데 정렬',
          alignLeft: '왼쪽 정렬',
          alignRight: '오른쪽 정렬',
          selectLanguage: '언어 선택',
          fontScale: '글꼴 크기',
          fontScaleXLarge: 'X Large Size',
          fontScaleLarge: 'Large Size',
          fontScaleNormal: 'Normal Size',
          fontScaleSmall: 'Small Size',
          fontScaleXSmall: 'X Small Size'
        }
      }
      Simditor.locale = 'ko-KR'
      this.editor = new Simditor({
        textarea: this.$refs.editor,
        toolbar: this.toolbar,
        pasteImage: true,
        upload: {
          url: '/api/admin/upload_image/',
          params: null,
          fileKey: 'image',
          connectionCount: 3,
          leaveConfirm: this.$i18n.t('m.Uploading_is_in_progress')
        },
        allowedStyles: {
          span: ['color']
        },
        placeholder: '내용',
        imageButton: ['upload']
      })

      this.editor.on('valuechanged', (e, src) => {
        this.currentValue = this.editor.getValue()
      })
      this.editor.on('decorate', (e, src) => {
        this.currentValue = this.editor.getValue()
      })

      this.editor.setValue(this.value)
    },
    watch: {
      'value' (val) {
        if (this.currentValue !== val) {
          this.currentValue = val
          this.editor.setValue(val)
        }
      },
      'currentValue' (newVal, oldVal) {
        if (newVal !== oldVal) {
          this.$emit('change', newVal)
          this.$emit('input', newVal)
        }
      }
    }
  }
</script>

<style lang="less" scoped>
</style>
<style>
[class ~= simditor-body] img {
  max-width: 100% !important;
  max-height: 100% !important;
  width: auto !important;
  height: auto !important;
}
</style>
