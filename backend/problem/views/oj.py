import random
from django.db.models import Q, Count
from utils.api import APIView
from account.decorators import check_contest_permission
from ..models import ProblemTag, Problem, ProblemRuleType, ProblemCategory, User
from ..serializers import ProblemSerializer, TagSerializer, ProblemSafeSerializer, ProblemCategorySerializer, CategoryListSerializer
from contest.models import ContestRuleType

class CategoryProblemPercentAPI(APIView):
    def get(self, request):
        id = request.GET.get("category_id")
        category = ProblemCategory.objects.get(id=id)
        problem_id_list = category.problems
        problems = Problem.objects.filter(id__in=problem_id_list)
        total = problems.count()
        no_accepted = problems.filter(accepted_number = 0).count()
        return self.success(int((total - no_accepted) / total * 100))


class CategoryListAPI(APIView):
    def get(self, request):
        categories = ProblemCategory.objects.all()
        # categories_data = ProblemCategorySerializer(categories, many=True).data
        categories_data = categories
                # category 검색 로직
        search = request.GET.get("search")
        searchtype = request.GET.get("searchtype")
        if search:
            if (searchtype == "0"): # 전체 검색
                categories_data = categories_data.filter(Q(title__contains=search) | Q(description__contains =search))
            elif (searchtype == "1"): # 제목 검색
                categories_data = categories_data.filter(title__contains=search)
            elif (searchtype == "2"): # 내용 검색
                categories_data = categories_data.filter(description__contains=search)
        # return self.success(list(categories_data))   
        # categories_data = list(categories_data)     
        data = self.paginate_data(request, categories_data) # 페이징
        categories = data["results"]
        categories_data = ProblemCategorySerializer(categories, many=True).data

        isNotloggedIn = False # 로그인 사용자의 경우
        try:
            username = request.user.username
            user = User.objects.get(username=username, is_disabled=False)
            profile = user.userprofile
            acm_problems = profile.acm_problems_status.get("problems", {}) #JSON Field Type
            #         example :
            #         "1": {
            #             "status": JudgeStatus.ACCEPTED,
            #             "_id": "1000"
            #         }
            ids = [] # accepted key list

            # accept 된 submission만 추출하기 위함
            for acm_problem_key in list(acm_problems.keys()):
                if acm_problems[acm_problem_key]["status"] == 0 or acm_problems[acm_problem_key]["status"] == "0":
                    ids.append(acm_problem_key)
            ids = list(ids)
        except User.DoesNotExist:
            isNotloggedIn = True
        # 비로그인 사용자의 경우 혹은 accept 된 submission이 없을 경우
        if isNotloggedIn or not ids:
            idx = 0
            for category in categories:
                problem_id_list = category.problems
                problems = Problem.objects.filter(id__in=problem_id_list)
                total = problems.count()
                categories_data[idx]['percent'] = int(0)
                idx = idx + 1
        else:
            # accept 된 key list를 통해 problem의 _id 값들을 모두 filtering
            idslist = Problem.objects.filter(id__in=ids).values_list("_id", flat=True)
            idslist = list(map(int, idslist)) # 정수로 변환

            idx = 0
            for category in categories:
                problem_ids_in_category_list = category.problems
                problems = Problem.objects.filter(id__in=problem_ids_in_category_list)
                problems_id_set = problems.values_list("_id", flat=True)
                problems_id_set = list(map(int, problems_id_set))
                total = problems.count()
                # 카테고리의 문제 set가 없을 경우
                if not problems_id_set:
                    categories_data[idx]['percent'] = 0
                else:
                    # 통과한 제출과 카테고리 문제리스트의 교집합
                    result = list(map(int,list(set(problems_id_set).intersection(idslist))))
                    # 교집합이 없을경우 : 0 percent
                    if not result:
                        categories_data[idx]['percent'] = 0
                    else:
                        categories_data[idx]['percent'] = int(len(result) / total * 100)
                idx = idx + 1
        res = {'result' : categories_data, 'total': data["total"] }
        return self.success(res)


class ProblemTagAPI(APIView):
    def get(self, request):
        qs = ProblemTag.objects
        keyword = request.GET.get("keyword")
        if keyword:
            qs = ProblemTag.objects.filter(name__icontains=keyword)
        else:
            qs = ProblemTag.objects.all()
        #tags = qs.annotate(problem_count=Count("problem")).filter(problem_count__gt=0)
        
        if request.GET.get("limit"):
            return self.success(self.paginate_data(request, qs, TagSerializer))
        else:
            return self.success(TagSerializer(qs, many=True).data)


class PickOneAPI(APIView):
    def get(self, request):
        problems = Problem.objects.filter(contest_id__isnull=True, visible=True)
        count = problems.count()
        if count == 0:
            return self.error("No problem to pick")
        return self.success(problems[random.randint(0, count - 1)]._id)


class ProblemAPI(APIView):
    @staticmethod
    def _add_problem_status(request, queryset_values):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            acm_problems_status = profile.acm_problems_status.get("problems", {})
            oi_problems_status = profile.oi_problems_status.get("problems", {})
            # paginate data
            results = queryset_values.get("results")
            if results is not None:
                problems = results
            else:
                problems = [queryset_values, ]
            for problem in problems:
                if problem["rule_type"] == ProblemRuleType.ACM:
                    problem["my_status"] = acm_problems_status.get(str(problem["id"]), {}).get("status")
                else:
                    problem["my_status"] = oi_problems_status.get(str(problem["id"]), {}).get("status")

    def get(self, request):
        # 문제 세부정보 페이지
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = Problem.objects.select_related("created_by") \
                    .get(_id=problem_id, contest_id__isnull=True, visible=True)
                problem_data = ProblemSerializer(problem).data
                self._add_problem_status(request, problem_data)
                return self.success(problem_data)
            except Problem.DoesNotExist:
                return self.error("문제가 존재하지 않습니다")

        limit = request.GET.get("limit")
        if not limit:
            return self.error("Limit is needed")

        problems = Problem.objects.select_related("created_by").filter(contest_id__isnull=True, visible=True)
        # 태그로 필터링
        tag_text = request.GET.get("tag")
        if tag_text:
            problems = problems.filter(tags__name=tag_text)

        # 검색 케이스
        keyword = request.GET.get("keyword", "").strip()
        if keyword:
            problems = problems.filter(Q(title__icontains=keyword) | Q(_id__icontains=keyword))

        # 난이도
        difficulty = request.GET.get("difficulty")
        if difficulty:
            problems = problems.filter(difficulty=difficulty)

        
        categoryid = request.GET.get("category")
        if categoryid:
            category = ProblemCategory.objects.get(id=categoryid)
            problem_id_list = category.problems
            problems = Problem.objects.filter(id__in=problem_id_list)
        
        # 프로필에 따라 완료한 문제에 태그 추가
        data = self.paginate_data(request, problems, ProblemSerializer)
        self._add_problem_status(request, data)
        return self.success(data)


class ContestProblemAPI(APIView):
    def _add_problem_status(self, request, queryset_values):
        if request.user.is_authenticated:
            profile = request.user.userprofile
            if self.contest.rule_type == ContestRuleType.ACM:
                problems_status = profile.acm_problems_status.get("contest_problems", {})
            else:
                problems_status = profile.oi_problems_status.get("contest_problems", {})
            for problem in queryset_values:
                problem["my_status"] = problems_status.get(str(problem["id"]), {}).get("status")

    @check_contest_permission(check_type="problems")
    def get(self, request):
        problem_id = request.GET.get("problem_id")
        if problem_id:
            try:
                problem = Problem.objects.select_related("created_by").get(_id=problem_id,
                                                                           contest=self.contest,
                                                                           visible=True)
            except Problem.DoesNotExist:
                return self.error("문제가 존재하지 않습니다")
            if self.contest.problem_details_permission(request.user):
                problem_data = ProblemSerializer(problem).data
                self._add_problem_status(request, [problem_data, ])
            else:
                problem_data = ProblemSafeSerializer(problem).data
            return self.success(problem_data)

        contest_problems = Problem.objects.select_related("created_by").filter(contest=self.contest, visible=True)
        if self.contest.problem_details_permission(request.user):
            data = ProblemSerializer(contest_problems, many=True).data
            self._add_problem_status(request, data)
        else:
            data = ProblemSafeSerializer(contest_problems, many=True).data
        return self.success(data)
