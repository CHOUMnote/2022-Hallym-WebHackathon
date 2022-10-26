<template>
  <div>
    <panel :padding="15" class="container">
      <div slot="title">{{$t('m.Compiler')}} & {{$t('m.Judger')}}</div>
      <div class="content markdown-body">
        <ul>
          <li v-for="lang in languages">{{lang.name}} ( {{lang.description}} )
            <p>컴파일 : <b>{{lang.config.compile.compile_command.substring(9)}}</b></p>
          </li>
        </ul>
      </div>
    </panel>
    <panel :padding="15" class="container">
      <div slot="title">{{$t('m.Result_Explanation')}}</div>
      <div class="content markdown-body">
        <ul>
          <li><b>{{$t('m.Pending')}}</b> : 채점 대기중인 상태입니다. 기다리시면 결과를 받아보실 수 있습니다.</li>
          <li><b>{{$t('m.Judging')}}</b> : 채점 중인 상태입니다.</li>
          <li><b>{{$t('m.Accepted')}}</b> :	제출한 코드가 서버 내의 테스트 케이스들에 대하여 모두 통과했을 경우에 받게 됩니다.</li>
          <li><b>{{$t('m.Wrong_Answer')}}</b> :	출력 결과가 다른 경우에 받게 됩니다.</li>
          <li><b>{{$t('m.Compile_Error')}}</b> :	제출한 코드가 컴파일에 실패한 경우입니다. 이 결과는 (경고)Warnning을 포함하지 않습니다.</li>
          <li><b>{{$t('m.Runtime_Error')}}</b> :	프로그램이 비정상적으로 종료되었을 경우에 받게 됩니다.</li>
          <li><b>{{$t('m.Time_Limit_Exceeded')}}</b> : 채점 과정 중 문제에서 주어진 시간보다 초과했을 경우에 받게 됩니다.</li>
          <li><b>{{$t('m.Memory_Limit_Exceeded')}}</b> : 채점 과정 중 문제에서 주어진 메모리 허용량보다 초과하게 될 경우에 받게 됩니다.</li>
          <li><b>{{$t('m.System_Error')}}</b> :	현재 체점 서버에 문제가 있거나 어떠한 이유로 중단되는 경우입니다. 이 경우 관리자에게 문의를 주시기를 바랍니다.</li>
        </ul>
      </div>
    </panel>
    <panel :padding="15" class="container">
      <div slot="title">자주 묻는 질문</div>
      <div class="content markdown-body">
        <ul>
          <li><b>입출력 방식</b>
            <p>입력과 출력은 모두 Standard IO를 통해 읽고 출력하게 됩니다. C언어를 예로들어 입력에서 Standard Input 으로 <code>stdin</code>을 통해 입력 받게 되며, 대표적으로 <code>scanf</code>이 있습니다.
              마찬가지로 출력 Standard Output으로는 <code>stdout</code>을 통해 출력을 하게 되며, 대표적으로 <code>printf</code>가 있습니다. 언어별 예제는 위 언어별 채점 방식을 참고하시기를 바랍니다.
            </p>
          </li>
          <li><b><span>틀렸습니다</span>를 받았을 경우</b>
          <p>작성한 코드에 대해 입력값에 대한 출력 값이 정확하게 일치하지 않으면 <span>틀렸습니다</span>를 받게 됩니다.
          데이터가 잘못 된 경우는 거의 없으며, 주어진 예제 입력이 맞는다고 다른 테스트케이스들 까지 모두 맞는 것은 아닙니다. 주어진 데이터의 범위 혹은 극단적인 케이스들까지 모두 고려하여 올바른 정답인지를 다시 확인해보세요.
          </p>
          </li>
          <li><b><span>시간 초과</span>를 받았을 경우</b>
            <p><span>시간 초과</span>는 말 그대로 문제에서 제한하는 시간 내에 통과하지 못할 경우 받게 됩니다. <span>통과</span> 혹은 <span>틀렸습니다</span>가 아닙니다.
            제한 시간을 초과하게 될 경우에 프로그램이 종료되기 때문에 맞았는지 틀렸는지 알 수 없습니다.</p>
          </li>
          <li><b><span>메모리 초과</span>를 받았을 경우</b>
            <p><span>메모리 초과</span>는 말 그대로 문제에서 제한 된 메모리를 초과하여 할당 할 경우 받게 됩니다. 단, 컴파일러의 최적화에 의해 임의로 초과시키더라도 반드시 <span>메모리 초과</span>가 나는 것은 아니며, <span>런타임 에러</span> 등
            다른 에러 결과를 받을 수도 있습니다.
            </p>
          </li>
          <li><b><span>컴파일 에러</span>를 받았을 경우</b>
            <p><span>컴파일 에러</span>의 경우 컴파일에 실패한 메세지를 자신이 제출했던 결과를 클릭하면 볼 수 있습니다.</p>
           </li>
          <li><b><span>런타임 에러</span>를 받았을 경우</b>
            <p><span>런타임 에러</span>의 경우에는 별도의 원인을 알려주진 않습니다.</p>
          </li>
        </ul>
      </div>
    </panel>
  </div>
</template>

<script>
  import utils from '@/utils/utils'

  export default {
    data () {
      return {
        languages: []
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
@import '../../../../styles/common.less';
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

    span {
      color: @purple;
    }
  }
</style>
