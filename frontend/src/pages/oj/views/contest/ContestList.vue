<template>
  <div style="display:flex; justify-content:space-between;" id="contest-container">
    <div id="contest-card">
      <div style="display: block;">
        <div class="title">
          {{ query.rule_type === "" ? "" : query.rule_type }}
          {{ $t("m.Contests") }}
        </div>
        <div>
          <ul class="filter">
            <li class="list">
              <Select
                id="rule"
                @on-change="onRuleChange"
                :placeholder="$t('m.Rule')"
              >
                <!-- <span>{{query.rule_type === '' ? this.$i18n.t('m.Rule') : this.$i18n.t('m.' + query.rule_type)}}
                  <Icon type="md-arrow-dropdown" />
                </span> -->
                <Option value="All">{{ $t("m.All") }}</Option>
                <Option value="OI">{{ $t("m.OI") }}</Option>
                <Option value="ACM">{{ $t("m.ACM") }}</Option>
              </Select>
            </li>
            <li class="list">
              <Select
                id="status"
                @on-change="onStatusChange"
                :placeholder="$t('m.Status')"
              >
                <!-- <span>{{query.status === '' ? this.$i18n.t('m.Status') : this.$i18n.t('m.' + CONTEST_STATUS_REVERSE[query.status].name.replace(/ /g,"_"))}}
                  <Icon type="md-arrow-dropdown" />
                </span> -->
                <Option value="All">모든 대회</Option>
                <Option value="0">진행 중인 대회</Option>
                <Option value="1">개최 예정인 대회</Option>
                <Option value="-1">종료 된 대회</Option>
              </Select>
            </li>
            <li>
              <Input
                id="keyword"
                @on-search="changeRoute"
                v-model="query.keyword"
                search
                placeholder="검색어를 입력하세요."
              ></Input>
            </li>
          </ul>
        </div>
      </div>
      <p id="no-contest" v-if="contests.length == 0">
        {{ $t("m.No_contest") }}
      </p>
      <ol id="contest-list">
        <li class="entry" v-for="contest in contests" :key="contest.title">
          <div>
            <div style="display:flex;">
              <div class="trophy">
                <img :src="contest.contest_title_img" />
              </div>
              <div
                class="contest-main"
                style="display: flex; flex-direction: column; justify-content:space-between;"
              >
                <p>
                  <a class="contest-title" @click.stop="goContest(contest)">
                    {{ contest.title }}
                  </a>
                  <template v-if="contest.contest_type != 'Public'">
                    <Icon type="ios-locked-outline" size="20"></Icon>
                  </template>
                </p>
                <div class="description" v-html="contest.description"></div>
                <ul class="detail" style="display:flex;">
                  <li>
                    <Tag type="border" :checked="true">{{
                      contest.start_time | localtime("YYYY-M-D HH:mm")
                    }}</Tag>
                  </li>
                  <!-- <li>
                  <Icon type="android-time" color="#3091f2"></Icon>
                  {{getDuration(contest.start_time, contest.end_time)}}
                </li> -->
                  <li>
                    <!-- <Button size="small" shape="circle" @click="onRuleChange(contest.rule_type)">
                    {{contest.rule_type}}
                  </Button> -->
                    <Tag
                      type="border"
                      :checkable="checkRule(contest.rule_type)"
                      @on-change="onRuleChange(contest.rule_type)"
                    >
                      {{ contest.rule_type }}</Tag
                    >
                  </li>
                  <li>
                    <Tag
                      type="border"
                      :color="CONTEST_STATUS_REVERSE[contest.status].color"
                      >{{
                        $t(
                          "m." +
                            CONTEST_STATUS_REVERSE[contest.status].name.replace(
                              / /g,
                              "_"
                            )
                        )
                      }}</Tag
                    >
                  </li>
                </ul>
              </div>
            </div>
          </div>
        </li>
      </ol>
      <Pagination
        style="float:none; text-align: center;"
        :total="total"
        :page-size.sync="limit"
        @on-change="changeRoute"
        :current.sync="page"
        :show-sizer="true"
        @on-page-size-change="changeRoute"
      ></Pagination>
    </div>
    <div id="user-ranking">
      <div class="main">
        <div class="ranking-container">
          <table class="ranking-list">
            <!-- 내용 -->
            <tbody
              v-for="(data, index) in dataRank"
              @click="goUser(data.user)"
              :key="index"
            >
              <tr class="ranking-entry" v-if="index == 0">
                <td class="image">
                  <img
                    class="rankings-img"
                    src="../../../../assets/gold crown.png"
                  />
                  <span class="top">1</span>
                </td>
                <div class="user-info ranker">
                  <td class="name">{{ data.user.username }}</td>
                  <td class="score">{{ data.accepted_number }}</td>
                </div>
              </tr>
              <tr class="ranking-entry" v-else-if="index == 1">
                <td class="image">
                  <img
                    class="rankings-img"
                    src="../../../../assets/silver crown.png"
                  />
                  <span class="top">2</span>
                </td>
                <div class="user-info ranker">
                  <td class="name">{{ data.user.username }}</td>
                  <td class="score">{{ data.accepted_number }}</td>
                </div>
              </tr>

              <tr class="ranking-entry" v-else-if="index == 2">
                <td class="image">
                  <img
                    class="rankings-img"
                    src="../../../../assets/bronse crown.png"
                  />
                  <span class="top third" style="color: white">3</span>
                </td>
                <div class="user-info ranker">
                  <td class="name">{{ data.user.username }}</td>
                  <td class="score">{{ data.accepted_number }}</td>
                </div>
              </tr>
              <tr class="ranking-entry" v-else-if="index > 2">
                <td class="no">{{ index + 1 }}</td>
                <div class="user-info">
                  <td class="name">{{ data.user.username }}</td>
                  <td class="score">{{ data.accepted_number }}</td>
                </div>
              </tr>
            </tbody>
          </table>
          <!-- <Pagination :total="total" :page-size.sync="limit" :current.sync="page"
                      @on-change="getRankData" show-sizer
                      @on-page-size-change="getRankData(1)"
                      style="margin: 20px 0 10px; display: flex; justify-content:center; float: none;"></Pagination> -->
        </div>
      </div>
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import api from "@oj/api";
import { mapGetters } from "vuex";
import utils from "@/utils/utils";
import Pagination from "@/pages/oj/components/Pagination";
import time from "@/utils/time";
import {
  CONTEST_STATUS_REVERSE,
  CONTEST_TYPE,
  RULE_TYPE
} from "@/utils/constants";

const limit = 10;

export default {
  name: "contest-list",
  components: {
    Pagination
  },
  data() {
    return {
      page: 1,
      query: {
        status: "",
        keyword: "",
        rule_type: ""
      },
      limit: limit,
      total: 0,
      rows: "",
      contests: [],
      loadingTable: false,
      dataRank: [],
      CONTEST_STATUS_REVERSE: CONTEST_STATUS_REVERSE,
      //      for password modal use
      cur_contest_id: ""
    };
  },
  beforeRouteEnter(to, from, next) {
    api.getContestList(0, limit).then(
      res => {
        next(vm => {
          vm.contests = res.data.data.results;
          vm.total = res.data.data.total;
        });
      },
      res => {
        next();
      }
    );
  },
  mounted() {
    this.init();
  },
  methods: {
    init() {
      let route = this.$route.query;
      this.query.status = route.status || "";
      this.query.rule_type = route.rule_type || "";
      this.query.keyword = route.keyword || "";
      this.page = parseInt(route.page) || 1;
      this.limit = parseInt(route.limit) || 10;
      this.getContestList(this.page);
      this.getRankData(this.page);
    },
    getContestList(page = 1) {
      let offset = (page - 1) * this.limit;
      api.getContestList(offset, this.limit, this.query).then(res => {
        this.contests = res.data.data.results;
        this.total = res.data.data.total;
      });
    },
    getRankData(page = 1) {
      let offset = (page - 1) * this.limit;
      api.getUserRank(offset, 10, RULE_TYPE.ACM).then(res => {
        this.dataRank = res.data.data.results;
      });
    },
    changeRoute() {
      let query = Object.assign({}, this.query);
      query.page = this.page;
      query.limit = this.limit;

      this.$router
        .push({
          name: "contest-list",
          query: utils.filterEmptyValue(query)
        })
        .catch(() => {});
    },
    onRuleChange(rule) {
      if (rule === "All") {
        this.query.rule_type = "";
      } else {
        this.query.rule_type = rule;
      }
      this.page = 1;
      this.changeRoute();
    },
    onStatusChange(status) {
      if (status === "All") {
        this.query.status = "";
      } else {
        this.query.status = status;
      }
      this.page = 1;
      this.changeRoute();
    },
    goContest(contest) {
      this.cur_contest_id = contest.id;
      if (
        contest.contest_type !== CONTEST_TYPE.PUBLIC &&
        !this.isAuthenticated
      ) {
        this.$error(this.$i18n.t("m.Please_login_first"));
        this.$store.dispatch("changeModalStatus", { visible: true });
      } else {
        this.$router
          .push({ name: "contest-details", params: { contestID: contest.id } })
          .catch(() => {});
      }
    },
    checkRule(rule) {
      if (this.query.rule_type !== rule) {
        return true;
      } else {
        return false;
      }
    },
    getDuration(startTime, endTime) {
      return time.duration(startTime, endTime);
    },
    goUser(user) {
      this.$router
        .push({
          name: "user-home",
          query: { username: user.username }
        })
        .catch(() => {});
    }
  },
  computed: {
    ...mapGetters(["isAuthenticated", "user"])
  },
  watch: {
    $route(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.init();
      }
    }
  }
};
</script>
<style lang="less" scoped>
@import "../../../../styles/common.less";
#contest-card {
  //min-width: 800px;
  width: 70%;
  background-color: @white;
  border-radius: 5px;
  box-shadow: 0 0 5px #cac6c6;
  margin: 20px 0 20px 200px;
  padding: 20px;

  #no-contest {
    margin: 0 20px;
    font-size: @font-regular;
    -webkit-text-stroke: 0.1px;
    text-align: center;
  }
  .title {
    color: @black;
    font-size: @font-medium;
    margin-left: 20px;
    margin-bottom: 20px;
    -webkit-text-stroke: 1px;
  }

  .filter {
    list-style: none;
    display: flex;
    margin-left: 20px;
    .list:not(:first-of-type) {
      margin-left: 15px;
    }
    margin-bottom: 30px;
    #rule {
      width: 100px;
    }
    #status {
      width: 150px;
    }
    #keyword {
      min-width: 180px;
      width: 20vw;
      margin-left: 15px;
      margin-right: 20px;
    }
  }

  #contest-list {
    list-style: none;
      ul {
        list-style:none;
      }
      .entry {
        margin: 15px 20px;
        border: 1px solid @dark-white;
        padding: 15px;
        .trophy {
          width: 100px;
          height: 100px;
          img {
            width: 100%;
            height: 100%;
          }
          min-width: 100px;
          min-height: 100px;
          background-color: @light-purple;
          margin-right: 10px;
          margin-top: 5px;
      }

      .contest-title {
        font-size: @font-regular;
        margin-left: 10px;
        color: @default-font-color;
        -webkit-text-stroke: 0.5px;
        &:hover {
          color: @orange;
          transition: color 0.3s ease-in-out;
        }
      }
      .detail {
        margin: 0 10px;
      }
      .description {
        margin-left: 10px;
        overflow: hidden;
        text-overflow: ellipsis;
        display: -webkit-box;
        -webkit-line-clamp: 3;
        -webkit-box-orient: vertical;
      }
    }
  }
}

#user-ranking {
  min-width: 180px;
  max-width: 300px;
  background-color: @white;
  border-radius: 5px;
  box-shadow: 0 0 5px #cac6c6;
  margin: 20px 200px 20px 30px;
  padding: 20px 30px;
}

.ranking-container {
  // width: 75vw;
  margin: auto;
}
.ranking-list {
  -webkit-text-stroke: 0.5px;
  border-collapse: collapse;
  table-layout: fixed;
  text-align: center;
  padding: 8px;
  margin: auto;

  .ranking-entry {
    display: flex;
    margin-bottom: 25px;
  }

  .user-info {
    display: flex;
    flex-direction: column;
    padding-bottom: 10px;
    text-align: left;
  }
  .ranker {
    justify-content: flex-end;
  }
  tbody {
    color: @black;
    -webkit-text-stroke: 0.3px;
    height: 60px;
    font-size: @font-micro;
    .name {
      cursor: pointer;
      &:hover {
        color: @orange;
        transition: color 0.3s ease-in-out;
      }
    }

    .score {
      color: @gray;
      font-size: 80%;
    }

    .no {
      font-size: 150%;
      line-height: 50px;
      width: 40px;
      margin-right: 15px;
    }

    .image {
      position: relative;
      margin-right: 15px;
      img {
        width: 40px;
      }
      .top {
        position: absolute;
        transform: translate(-50%, -50%);
        top: 60%;
        left: 50%;
        color: @black;
        -webkit-text-stroke: 0.5px;
      }
      .third {
        color: @white;
      }
    }
  }
}
@media screen and (max-width : 900px) {
  #contest-container {
    flex-direction: column;
    max-width: 100vw;
    align-items: center;
    #contest-card {
      margin: 20px 0;
      min-width: 90vw;
      .title {
        margin: 0 0 20px;
      }
      .filter {
        display: block;
        margin: 0 0 20px;
        .list {
          display: inline-block;
        }
        #keyword {
          display: block;
          margin: 10px 0 0;
          width: 100%;
        }
      }
      #contest-list {
        .entry {
          margin: 15px 0;
          padding: 10px;
        }
      }
    }
    #user-ranking {
      margin: 0 auto;
      min-width: 90vw;
    }
  }
}
</style>
