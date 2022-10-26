
<template>
  <div class="header">
    <div class="title">언어별 도움말</div>
    <!-- General -->
    <Card :padding="50">
      <div class="content markdown-body">
        <ul>
          <li><b>공통</b>
            <p>입력과 출력은 모두 Standard IO를 통해 읽고 출력하게 됩니다. C언어를 예로들어 입력에서 Standard Input 으로 <code>stdin</code>을 통해 입력 받게 되며, 대표적으로 <code>scanf</code>가 있습니다.
              마찬가지로 출력 Standard Output으로는 <code>stdout</code>을 통해 출력을 하게 되며, 대표적으로 <code>printf</code>가 있습니다. 언어별 예제는 아래 예제 코드를 참고하시기를 바랍니다.
            </p>
          </li>
        </ul>
      </div>
      <div class="exampletext">{{exampleProblem}}</div>
                   <BlockedCursorCodeMirror
                :value="examplesource[0].source"
                :language="langopt[1]"
                :theme="theme"></BlockedCursorCodeMirror>
    </Card>
    <!-- C -->
    <Card :padding="50">
      <div class="content markdown-body">
        <ul>
          <li><b>{{examplesource[0].lang}}</b>
          </li>
        </ul>
      </div>
      <div class="exampletext">{{exampleProblem}}</div>
                   <BlockedCursorCodeMirror
                :value="examplesource[0].source"
                :language="langopt[1]"
                :theme="theme"></BlockedCursorCodeMirror>
    </Card>
    <!-- C++ -->
    <Card :padding="50">
      <div class="content markdown-body">
        <ul>
          <li><b>{{examplesource[1].lang}}</b>
          </li>
        </ul>
      </div>
      <div class="exampletext">{{exampleProblem}}</div>
                   <BlockedCursorCodeMirror
                :value="examplesource[1].source"
                :language="langopt[1]"
                :theme="theme"></BlockedCursorCodeMirror>
    </Card>
    <!-- Go -->
    <Card :padding="50">
      <div class="content markdown-body">
        <ul>
          <li><b>{{examplesource[2].lang}}</b>
          </li>
        </ul>
      </div>
      <div class="exampletext">{{exampleProblem}}</div>
                   <BlockedCursorCodeMirror
                :value="examplesource[2].source"
                :language="langopt[1]"
                :theme="theme"></BlockedCursorCodeMirror>
    </Card>
    <!-- Java -->
    <Card :padding="50">
      <div class="content markdown-body">
        <ul>
          <li><b>{{examplesource[3].lang}}</b>
          </li>
        </ul>
      </div>
      <div class="exampletext">{{exampleProblem}}</div>
                   <BlockedCursorCodeMirror
                :value="examplesource[3].source"
                :language="langopt[2]"
                :theme="theme"></BlockedCursorCodeMirror>
    </Card>
    <!-- JavaScript -->
        <Card :padding="50">
      <div class="content markdown-body">
        <ul>
          <li><b>{{examplesource[4].lang}}</b>
          </li>
        </ul>
      </div>
      <div class="exampletext">{{exampleProblem}}</div>
                   <BlockedCursorCodeMirror
                :value="examplesource[4].source"
                :language="langopt[2]"
                :theme="theme"></BlockedCursorCodeMirror>
    </Card>
    <!-- Python2 -->
        <Card :padding="50">
      <div class="content markdown-body">
        <ul>
          <li><b>{{examplesource[5].lang}}</b>
          </li>
        </ul>
      </div>
      <div class="exampletext">{{exampleProblem}}</div>
                   <BlockedCursorCodeMirror
                :value="examplesource[5].source"
                :language="langopt[2]"
                :theme="theme"></BlockedCursorCodeMirror>
    </Card>
    <!-- Python3 -->
        <Card :padding="50">
      <div class="content markdown-body">
        <ul>
          <li><b>{{examplesource[6].lang}}</b>
          </li>
        </ul>
      </div>
      <div class="exampletext">{{exampleProblem}}</div>
                   <BlockedCursorCodeMirror
                :value="examplesource[6].source"
                :language="langopt[2]"
                :theme="theme"></BlockedCursorCodeMirror>
    </Card>
  </div>
</template>

<script>
  import utils from '@/utils/utils'
  import BlockedCursorCodeMirror from '@oj/components/BlockedCursorCodeMirror.vue'
  export default {
    name: 'Languages',
    components: {
      BlockedCursorCodeMirror
    },
    data () {
      return {
        theme: 'solarized',
        langopt: ['C', 'C++', 'Java', 'Python2'],
        languages: [],
        examplesource: [
          {
            lang: 'C',
            source: '#include <stdio.h>\n\n' +
                    'int main() {\n' +
                    '  int a, b;\n' +
                    '  scanf("%d %d",&a,&b);\n' +
                    '  printf("%d\\n",a+b);\n' +
                    '  return 0;\n' +
                    '}'
          },
          {
            lang: 'C++',
            source: '#include <iostream>\n\n' +
                    'using namespace std;\n\n' +
                    'int main() {\n' +
                    '  int a, b;\n' +
                    '  cin >> a >> b;\n' +
                    '  cout << a+b << endl;\n' +
                    '  return 0;\n' +
                    '}'
          },
          {
            lang: 'Go',
            source: 'package main\n\n' +
                    'import "fmt"\n\n' +
                    'func main() {\n' +
                    '    var a int\n' +
                    '    fmt.Scanf("%d", &a)\n' +
                    '    fmt.Printf("%d", a)\n' +
                    '}'
          },
          {
            lang: 'Java',
            source: 'import java.util.*;\n\n' +
                    'public class Main {\n' +
                    '  public static void main(String[] args) {\n' +
                    '    Scanner scan = new Scanner(System.in);\n' +
                    '    int a, b;\n' +
                    '    a = scan.nextInt();\n' +
                    '    b = scan.nextInt();\n' +
                    '    System.out.println(a + b);\n' +
                    '  }\n' +
                    '}'
          },
          {
            lang: 'JavaScript',
            source: 'var fs = require(\'fs\');\n' +
                    'var input = fs.readFileSync(\'/dev/stdin\').toString().split(\' \');\n' +
                    'var a = parseInt(input[0]);\n' +
                    'var b = parseInt(input[1]);\n' +
                    'console.log(a+b)\n'
          },
          {
            lang: 'Python2',
            source: 'a, b = map(int, raw_input().split())\n' +
                    'print a+b'
          },
          {
            lang: 'Python3',
            source: 'a, b = map(int, input().split())\n' +
                    'print a+b'
          }
        ],
        readable: 'nocursor',
        BlinkRate: 0,
        exampleProblem: 'xxx번 예제 코드'
      }
    },
    beforeRouteEnter (to, from, next) {
      utils.getLanguages().then(languages => {
        next(vm => {
          vm.languages = languages
        })
      })
    }
  }
</script>

<style scoped lang="less">
  .container1 {
    margin-bottom: 20px;
    height: 150px;
    .content {
      font-size: 16px;
      margin: 50px 50px 50px 50px;
      > ul {
        list-style: disc;
        li {
          line-height: 2;
          .title {
            font-weight: 500;
          }
        }
      }
    }
  }
  .header {
    width: calc(100% - 100px);
    margin: 0 auto;
  }
  .title {
    padding-top: 50px;
    margin: 0 50px 50px 50px;
    font-size: 30px;
    font-weight: 700;
  }
  .exampletext {
    margin-bottom: 20px;
  }
  .container {
    margin-bottom: 20px;
    
    .content {
      font-size: 16px;
      margin: 0 50px 20px 50px;
      > ul {
        list-style: disc;
        li {
          line-height: 2;
          .title {
            font-weight: 500;
          }
        }
      }
    }
  }

</style>
