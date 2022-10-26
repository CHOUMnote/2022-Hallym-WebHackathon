import functools
import hashlib
import time

from problem.models import Problem
from contest.models import Contest, ContestType, ContestStatus, ContestRuleType
from utils.api import JSONResponse, APIError
from utils.constants import CONTEST_PASSWORD_SESSION_KEY
from .models import ProblemPermission


class BasePermissionDecorator(object):
    def __init__(self, func):
        self.func = func

    def __get__(self, obj, obj_type):
        return functools.partial(self.__call__, obj)

    def error(self, data):
        return JSONResponse.response({"error": "permission-denied", "data": data})

    def __call__(self, *args, **kwargs):
        self.request = args[1]

        if self.check_permission():
            if self.request.user.is_disabled:
                return self.error("Your account is disabled")
            return self.func(*args, **kwargs)
        else:
            return self.error("Please login first")

    def check_permission(self):
        raise NotImplementedError()


class login_required(BasePermissionDecorator):
    def check_permission(self):
        return self.request.user.is_authenticated

class verify_required(BasePermissionDecorator):
    def check_permission(self):
        user = self.request.user
        return user.is_email_verify or user.is_admin_role()
    
    def __call__(self, *args, **kwargs):
        self.request = args[1]
        if self.check_permission():
            return self.func(*args, **kwargs)
        else:
            return self.error("Please verify your account first") 

    

class super_admin_required(BasePermissionDecorator):
    def check_permission(self):
        user = self.request.user
        return user.is_authenticated and user.is_super_admin()


class admin_role_required(BasePermissionDecorator):
    def check_permission(self):
        user = self.request.user
        return user.is_authenticated and user.is_admin_role()


class problem_permission_required(admin_role_required):
    def check_permission(self):
        if not super(problem_permission_required, self).check_permission():
            return False
        if self.request.user.problem_permission == ProblemPermission.NONE:
            return False
        return True


def check_contest_password(password, contest_password):
    if not (password and contest_password):
        return False
    if password == contest_password:
        return True
    else:
        # sig = sha256(contest_password + timestamp)[:8]
        if "#" in password:
            s = password.split("#")
            if len(s) != 2:
                return False
            sig, ts = s[0], s[1]

            if sig == hashlib.sha256((contest_password + ts).encode("utf-8")).hexdigest()[:8]:
                try:
                    ts = int(ts)
                except Exception:
                    return False
                return int(time.time()) < ts
            else:
                return False
        else:
            return False


def check_contest_permission(check_type="details"):
    """
    클래스 기반 보기 전용의 경우 사용자에게 콘테스트에 참가할 수 있는 권한이 있는지 확인하고 check_type 선택적 세부 정보, 문제, 순위, 제출
    검증을 통과하면 뷰의 self.contest를 통해 테스트를 받을 수 있습니다.
    """

    def decorator(func):
        def _check_permission(*args, **kwargs):
            self = args[0]
            request = args[1]
            user = request.user
            if request.data.get("contest_id"):
                contest_id = request.data["contest_id"]
            else:
                contest_id = request.GET.get("contest_id")
            if not contest_id:
                return self.error("Parameter error, contest_id is required")

            try:
                # use self.contest to avoid query contest again in view.
                self.contest = Contest.objects.select_related("created_by").get(id=contest_id, visible=True)
            except Contest.DoesNotExist:
                return self.error("Contest %s doesn't exist" % contest_id)

            # Anonymous
            if not user.is_authenticated:
                return self.error("Please login first.")

            # creator or owner
            if user.is_contest_admin(self.contest):
                return func(*args, **kwargs)

            if self.contest.contest_type == ContestType.PASSWORD_PROTECTED_CONTEST:
                # password error
                if not check_contest_password(request.session.get(CONTEST_PASSWORD_SESSION_KEY, {}).get(self.contest.id), self.contest.password):
                    return self.error("Wrong password or password expired")

            # regular user get contest problems, ranks etc. before contest started
            if self.contest.status == ContestStatus.CONTEST_NOT_START and check_type != "details":
                return self.error("Contest has not started yet.")

            # check does user have permission to get ranks, submissions in OI Contest
            if self.contest.status == ContestStatus.CONTEST_UNDERWAY and self.contest.rule_type == ContestRuleType.OI:
                if not self.contest.real_time_rank and (check_type == "ranks" or check_type == "submissions"):
                    return self.error(f"No permission to get {check_type}")

            return func(*args, **kwargs)
        return _check_permission
    return decorator


def ensure_created_by(obj, user):
    e = APIError(msg=f"{obj.__class__.__name__} does not exist")
    if not user.is_admin_role():
        raise e
    if user.is_super_admin():
        return
    if isinstance(obj, Problem):
        if not user.can_mgmt_all_problem() and obj.created_by != user:
            raise e
    elif obj.created_by != user:
        raise e
