import json
import os
from datetime import timedelta
from importlib import import_module
import smtplib
from utils.shortcuts import send_email
import qrcode
from django.conf import settings
from django.contrib import auth
from django.template.loader import render_to_string
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from otpauth import OtpAuth

from account.models import User
from problem.models import Problem
from utils.constants import ContestRuleType
from options.options import SysOptions
from utils.api import APIView, validate_serializer, CSRFExemptAPIView
from utils.captcha import Captcha
from utils.shortcuts import rand_str, img2base64, datetime2str
from ..decorators import login_required, verify_required
from ..models import User, UserProfile, AdminType
from ..serializers import (ApplyResetPasswordSerializer, ResetPasswordSerializer,
                           UserChangePasswordSerializer, UserDeleteSerializer, UserLoginSerializer,
                           UserRegisterSerializer, UsernameOrEmailCheckSerializer,
                           RankInfoSerializer, UserChangeEmailSerializer, SSOSerializer)
from ..serializers import (TwoFactorAuthCodeSerializer, UserProfileSerializer,
                           EditUserProfileSerializer, ImageUploadForm, ApplyVerifyEmailSerializer, VerifyEmailSerializer,
                           UserGrassDataSerializer, UserLastActivitySerializer)
from ..tasks import send_email_async

class LastActivityAPI(APIView):
    @validate_serializer(UserLastActivitySerializer)
    def get(self, request):
        # 비로그인시 pass
        user = request.user
        if not user.is_authenticated:
            return self.success()
        # 세션 갱신 때마다 시간 저장
        now_time = now()
        if not user.last_activity: 
            user.last_activity = now_time
            user.save()
            return self.success(json.dumps(0, default=str))

        inactive_time =  now_time - user.last_activity
        user.last_activity = now_time
        user.save()
        return self.success(json.dumps(inactive_time.total_seconds(), default=str))

# JG 02.15
class UserDeleteAPI(APIView):
    @validate_serializer(UserDeleteSerializer)
    @login_required
    def post(self, request):
        
        data = request.data
        data["username"] = data["username"].lower()
        if request.user.username != data["username"]:
            return self.error("Not your account username!")
        data["password"] = data["password"].lower()
        captcha = Captcha(request)
        if not captcha.check(data["captcha"]):
            return self.error("captcha가 올바르지 않습니다")
        
        
        user = auth.authenticate(username=data["username"], password=data["password"])
        if user:
            if user.two_factor_auth:
                if "tfa_code" not in data:
                    return self.error("tfa_required")
                if not OtpAuth(user.tfa_token).valid_totp(data["tfa_code"]):
                    return self.error("Invalid two factor verification code")
            request.user.delete()
            auth.logout(request)
            return self.success("성공하였습니다")
        else:
            return self.error("Invalid Password")


# DG 02.13
class ApplyVerifyEmailAPI(APIView):
    @login_required
    @validate_serializer(ApplyVerifyEmailSerializer)
    def post(self, request):
        if not request.user.is_authenticated:
            return self.error("잘못 된 접근입니다.")
        if not SysOptions.smtp_config:
            return self.error("SMTP 설정이 되어있지 않습니다")
        data = request.data
        try:
            user = User.objects.get(email__iexact=data["email"])
        except User.DoesNotExist:
            return self.error("사용자를 찾을 수 없습니다.")
        if user != request.user:
            return self.error("이메일이 일치하지 않습니다.")
        if user.verify_email_token_expire_time and 0 < int(
                (user.verify_email_token_expire_time - now()).total_seconds()) < 60:
            return self.error("재전송은 1분마다 가능합니다.")
        user.verify_email_token = rand_str(length=8)
        user.verify_email_token_expire_time = now() + timedelta(minutes=15)
        user.save()
        render_data = {
                "website_name": SysOptions.website_name,
                "token": user.verify_email_token
        }
        try:
            email_html = render_to_string("auth_token_email.html", render_data)
            send_email(smtp_config=SysOptions.smtp_config,
                       from_name=SysOptions.website_name_shortcut,
                       to_name=request.user.username,
                       to_email=request.data["email"],
                       subject="[" + SysOptions.website_name_shortcut + "] 이메일 인증 코드",
                       content=email_html)
        except smtplib.SMTPResponseException as e:
            # guess error message encoding
            msg = "이메일 전송이 실패했습니다"
            try:
                msg = e.smtp_error
                # qq mail
                msg = msg.decode("gbk")
            except Exception:
                msg = msg.decode("utf-8", "ignore")
            return self.error(msg)
        except Exception as e:
            msg = str(e)
            return self.error(msg)
       
        return self.success("성공하였습니다")

# DG 02.13
class VerifyEmailAPI(APIView):
    @login_required
    @validate_serializer(VerifyEmailSerializer)
    def post(self, request):
        data = request.data
        try:
            user = User.objects.get(verify_email_token=data["token"])
        except User.DoesNotExist:
            return self.error("유효하지 않은 코드입니다")
        if request.user.username != user.username:
            return self.error("유효하지 않은 코드입니다")
        if user.verify_email_token_expire_time < now():
            return self.error("만료된 코드입니다.")
        user.verify_email_token = None
        user.is_email_verify = True
        user.save()
        return self.success("성공하였습니다")

#temp
class GrassAPI(APIView):
    @login_required
    def get(self, request):
        username = request.user.username
        """
        if data is None:
            return self.error("invalid Query")
        """
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return self.error("존재하지 않는 유저입니다")
        return self.success(UserGrassDataSerializer(user).data)

    
class UserProfileAPI(APIView):
    @method_decorator(ensure_csrf_cookie)
    def get(self, request, **kwargs):
        """
        로그인 여부 결정, 로그인한 경우 사용자 정보 반환
        """
        user = request.user
        if not user.is_authenticated:
            return self.success()
        show_real_name = False
        username = request.GET.get("username")
        try:
            if username:
                user = User.objects.get(username=username, is_disabled=False)
            else:
                user = request.user
                # api는 자체 정보를 반환함. real_name을 반환 할 수도 있음
                show_real_name = True
        except User.DoesNotExist:
            return self.error("존재하지 않는 유저입니다")
        return self.success(UserProfileSerializer(user.userprofile, show_real_name=show_real_name).data)

    @validate_serializer(EditUserProfileSerializer)
    @login_required
    @verify_required
    def put(self, request):
        data = request.data
        user_profile = request.user.userprofile
        for k, v in data.items():
            setattr(user_profile, k, v)
        user_profile.save()
        return self.success(UserProfileSerializer(user_profile, show_real_name=True).data)


class AvatarUploadAPI(APIView):
    request_parsers = ()

    @login_required
    @verify_required
    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            avatar = form.cleaned_data["image"]
        else:
            return self.error("Invalid file content")
        if avatar.size > 2 * 1024 * 1024:
            return self.error("Picture is too large")
        suffix = os.path.splitext(avatar.name)[-1].lower()
        if suffix not in [".gif", ".jpg", ".jpeg", ".bmp", ".png"]:
            return self.error("Unsupported file format")

        name = rand_str(10) + suffix
        with open(os.path.join(settings.AVATAR_UPLOAD_DIR, name), "wb") as img:
            for chunk in avatar:
                img.write(chunk)
        user_profile = request.user.userprofile

        user_profile.avatar = f"{settings.AVATAR_URI_PREFIX}/{name}"
        user_profile.save()
        return self.success("성공하였습니다")


class TwoFactorAuthAPI(APIView):
    @login_required
    def get(self, request):
        """
        Get QR code
        """
        user = request.user
        if user.two_factor_auth:
            return self.error("2FA is already turned on")
        token = rand_str()
        user.tfa_token = token
        user.save()

        label = f"{SysOptions.website_name_shortcut}:{user.username}"
        image = qrcode.make(OtpAuth(token).to_uri("totp", label, SysOptions.website_name.replace(" ", "")))
        return self.success(img2base64(image))

    @login_required
    @validate_serializer(TwoFactorAuthCodeSerializer)
    def post(self, request):
        """
        Open 2FA
        """
        code = request.data["code"]
        user = request.user
        if OtpAuth(user.tfa_token).valid_totp(code):
            user.two_factor_auth = True
            user.save()
            return self.success("성공하였습니다")
        else:
            return self.error("Invalid code")

    @login_required
    @validate_serializer(TwoFactorAuthCodeSerializer)
    def put(self, request):
        code = request.data["code"]
        user = request.user
        if not user.two_factor_auth:
            return self.error("2FA is already turned off")
        if OtpAuth(user.tfa_token).valid_totp(code):
            user.two_factor_auth = False
            user.save()
            return self.success("성공하였습니다")
        else:
            return self.error("Invalid code")


class CheckTFARequiredAPI(APIView):
    @validate_serializer(UsernameOrEmailCheckSerializer)
    def post(self, request):
        """
        Check TFA is required
        """
        data = request.data
        result = False
        if data.get("username"):
            try:
                user = User.objects.get(username=data["username"])
                result = user.two_factor_auth
            except User.DoesNotExist:
                pass
        return self.success({"result": result})


class UserLoginAPI(APIView):
    @validate_serializer(UserLoginSerializer)
    def post(self, request):
        print("login")
        """
        User login api
        """
        data = request.data
        user = auth.authenticate(username=data["username"], password=data["password"])
        # None is returned if username or password is wrong
        if user:
            if user.is_disabled:
                return self.error("사용할 수 없는 계정입니다")
            if not user.two_factor_auth:
                auth.login(request, user)
                return self.success("성공하였습니다")

            # `tfa_code` not in post data
            if user.two_factor_auth and "tfa_code" not in data:
                return self.error("tfa_required")

            if OtpAuth(user.tfa_token).valid_totp(data["tfa_code"]):
                auth.login(request, user)
                return self.success("성공하였습니다")
            else:
                return self.error("two factor verification code가 올바르지 않습니다")
        else:
            return self.error("아이디 혹은 비밀번호가 올바르지 않습니다")


class UserLogoutAPI(APIView):
    def get(self, request):
        auth.logout(request)
        return self.success()


class UsernameOrEmailCheck(APIView):
    @validate_serializer(UsernameOrEmailCheckSerializer)
    def post(self, request):
        """
        check username or email is duplicate
        """
        data = request.data
        # True means already exist.
        result = {
            "username": False,
            "email": False
        }
        if data.get("username"):
            result["username"] = User.objects.filter(username=data["username"].lower()).exists()
        if data.get("email"):
            result["email"] = User.objects.filter(email=data["email"].lower()).exists()
        return self.success(result)


class UserRegisterAPI(APIView):
    @validate_serializer(UserRegisterSerializer)
    def post(self, request):
        """
        User register api
        """
        if not SysOptions.allow_register:
            return self.error("관리자에 의해 가입 기능이 제한되어있습니다")

        data = request.data
        data["username"] = data["username"].lower()
        data["email"] = data["email"].lower()
        captcha = Captcha(request)
        if not captcha.check(data["captcha"]):
            return self.error("captcha가 올바르지 않습니다")
        if User.objects.filter(username=data["username"]).exists():
            return self.error("Username already exists")
        if User.objects.filter(email=data["email"]).exists():
            return self.error("Email already exists")
        user = User.objects.create(username=data["username"], email=data["email"], is_email_verify=True)
        user.set_password(data["password"])

        user.save()
        UserProfile.objects.create(user=user)
        return self.success("성공하였습니다")


class UserChangeEmailAPI(APIView):
    @validate_serializer(UserChangeEmailSerializer)
    @login_required
    def post(self, request):
        data = request.data
        user = auth.authenticate(username=request.user.username, password=data["password"])
        if user:
            if user.two_factor_auth:
                if "tfa_code" not in data:
                    return self.error("tfa_required")
                if not OtpAuth(user.tfa_token).valid_totp(data["tfa_code"]):
                    return self.error("two factor verification code가 올바르지 않습니다")
            data["new_email"] = data["new_email"].lower()
            if User.objects.filter(email=data["new_email"]).exists():
                return self.error("이미 사용되고 있는 이메일입니다.")
            user.email = data["new_email"]
            user.is_email_verify = False
            user.save()
            return self.success("성공하였습니다")
        else:
            return self.error("비밀번호가 올바르지 않습니다")


class UserChangePasswordAPI(APIView):
    @validate_serializer(UserChangePasswordSerializer)
    @login_required
    def post(self, request):
        """
        User change password api
        """
        data = request.data
        username = request.user.username
        user = auth.authenticate(username=username, password=data["old_password"])
        if user:
            if user.two_factor_auth:
                if "tfa_code" not in data:
                    return self.error("tfa_required")
                if not OtpAuth(user.tfa_token).valid_totp(data["tfa_code"]):
                    return self.error("two factor verification code가 올바르지 않습니다")
            user.set_password(data["new_password"])
            user.save()
            return self.success("성공하였습니다")
        else:
            return self.error("비밀번호가 일치하지 않습니다")


class ApplyResetPasswordAPI(APIView):
    @validate_serializer(ApplyResetPasswordSerializer)
    def post(self, request):
        if request.user.is_authenticated:
            return self.error("이미 로그인 상태입니다.")
        data = request.data
        captcha = Captcha(request)
        if not captcha.check(data["captcha"]):
            return self.error("captcha가 올바르지 않습니다")
        try:
            user = User.objects.get(email__iexact=data["email"])
        except User.DoesNotExist:
            return self.error("존재하지 않는 유저입니다")
        # if user.reset_password_token_expire_time and 0 < int(
        #         (user.reset_password_token_expire_time - now()).total_seconds()) < 20 * 60:
        #     return self.error("You can only reset password once per 20 minutes")
        user.reset_password_token = rand_str()
        user.reset_password_token_expire_time = now() + timedelta(minutes=20)
        user.save()
        render_data = {
            "username": user.username,
            "website_name": SysOptions.website_name,
            "link": f"{SysOptions.website_base_url}/reset-password/{user.reset_password_token}"
        }
        email_html = render_to_string("reset_password_email.html", render_data)
        if not SysOptions.smtp_config:
            return self.error("SMTP 설정이 되어있지 않습니다")
        try:
            email_html = render_to_string("reset_password_email.html", render_data)
            send_email(smtp_config=SysOptions.smtp_config,
                       from_name=SysOptions.website_name_shortcut,
                       to_name=request.user.username,
                       to_email=request.data["email"],
                       subject="Reset Your Password",
                       content=email_html)
        except smtplib.SMTPResponseException as e:
            # guess error message encoding
            msg = b"Failed to send email"
            try:
                msg = e.smtp_error
                # qq mail
                msg = msg.decode("gbk")
            except Exception:
                msg = msg.decode("utf-8", "ignore")
            return self.error(msg)
        except Exception as e:
            msg = str(e)
            return self.error(msg)

        return self.success("성공하였습니다")


class ResetPasswordAPI(APIView):
    @validate_serializer(ResetPasswordSerializer)
    def post(self, request):
        data = request.data
        captcha = Captcha(request)
        if not captcha.check(data["captcha"]):
            return self.error("captcha가 올바르지 않습니다")
        try:
            user = User.objects.get(reset_password_token=data["token"])
        except User.DoesNotExist:
            return self.error("토큰이 올바르지 않습니다")
        if user.reset_password_token_expire_time < now():
            return self.error("토큰이 유효하지 않습니다")
        user.reset_password_token = None
        user.two_factor_auth = False
        user.set_password(data["password"])
        user.save()
        return self.success("성공하였습니다")


class SessionManagementAPI(APIView):
    @login_required
    def get(self, request):
        engine = import_module(settings.SESSION_ENGINE)
        session_store = engine.SessionStore
        current_session = request.session.session_key
        session_keys = request.user.session_keys
        result = []
        modified = False
        for key in session_keys[:]:
            session = session_store(key)
            # session does not exist or is expiry
            if not session._session:
                session_keys.remove(key)
                modified = True
                continue

            s = {}
            if current_session == key:
                s["current_session"] = True
            s["ip"] = session["ip"]
            s["user_agent"] = session["user_agent"]
            s["last_activity"] = datetime2str(session["last_activity"])
            s["session_key"] = key
            result.append(s)
        if modified:
            request.user.save()
        return self.success(result)

    @login_required
    def delete(self, request):
        session_key = request.GET.get("session_key")
        if not session_key:
            return self.error("Parameter Error")
        request.session.delete(session_key)
        if session_key in request.user.session_keys:
            request.user.session_keys.remove(session_key)
            request.user.save()
            return self.success("성공하였습니다")
        else:
            return self.error("session_key 가 올바르지 않습니다")


class UserRankAPI(APIView):
    def get(self, request):
        rule_type = request.GET.get("rule")
        if rule_type not in ContestRuleType.choices():
            rule_type = ContestRuleType.ACM
        profiles = UserProfile.objects.filter(user__admin_type=AdminType.REGULAR_USER, user__is_disabled=False) \
            .select_related("user")
        if rule_type == ContestRuleType.ACM:
            profiles = profiles.filter(submission_number__gt=0).order_by("-accepted_number", "submission_number")
        else:
            profiles = profiles.filter(total_score__gt=0).order_by("-total_score")
        return self.success(self.paginate_data(request, profiles, RankInfoSerializer))


class ProfileProblemDisplayIDRefreshAPI(APIView):
    @login_required
    def get(self, request):
        profile = request.user.userprofile
        acm_problems = profile.acm_problems_status.get("problems", {})
        oi_problems = profile.oi_problems_status.get("problems", {})
        ids = list(acm_problems.keys()) + list(oi_problems.keys())
        if not ids:
            return self.success()
        display_ids = Problem.objects.filter(id__in=ids, visible=True).values_list("_id", flat=True)
        id_map = dict(zip(ids, display_ids))
        for k, v in acm_problems.items():
            v["_id"] = id_map[k]
        for k, v in oi_problems.items():
            v["_id"] = id_map[k]
        profile.save(update_fields=["acm_problems_status", "oi_problems_status"])
        return self.success()


class OpenAPIAppkeyAPI(APIView):
    @login_required
    def post(self, request):
        user = request.user
        if not user.open_api:
            return self.error("OpenAPI 권한이 없습니다")
        api_appkey = rand_str()
        user.open_api_appkey = api_appkey
        user.save()
        return self.success({"appkey": api_appkey})


class SSOAPI(CSRFExemptAPIView):
    @login_required
    def get(self, request):
        token = rand_str()
        request.user.auth_token = token
        request.user.save()
        return self.success({"token": token})

    @method_decorator(csrf_exempt)
    @validate_serializer(SSOSerializer)
    def post(self, request):
        try:
            user = User.objects.get(auth_token=request.data["token"])
        except User.DoesNotExist:
            return self.error("존재하지 않는 유저입니다")
        return self.success({"username": user.username, "avatar": user.userprofile.avatar, "admin_type": user.admin_type})
        
