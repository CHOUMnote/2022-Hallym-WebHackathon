from ..models import EmailAuthentication
from utils.api import APIView, validate_serializer
from ..serializers import EmailAuthenticationSerializer, MakeEmailAuthenticationTokenSerializer
from django.utils.timezone import now
from datetime import timedelta
from options.options import SysOptions
from utils.shortcuts import rand_str
from django.template.loader import render_to_string
from utils.shortcuts import send_email
import smtplib

class EmailAuthenticationAPI(APIView):
    @validate_serializer(EmailAuthenticationSerializer)
    def post(self, request):
      data = request.data
      try:
          user = EmailAuthentication.objects.get(email__iexact=data["email"])
      except EmailAuthentication.DoesNotExist:
          return self.error("이메일을 가져올 수 없습니다.")
      if user.verify_email_token_expire_time < now():
          return self.error("유효하지 않은 코드입니다.")
      if user.verify_email_token != data["token"]:
          return self.error("유효하지 않은 코드입니다.")
      user.delete()
      return self.success("인증되었습니다.")


class MakeEmailAuthenticationTokenAPI(APIView):
    @validate_serializer(MakeEmailAuthenticationTokenSerializer)
    def post(self, request):
        """
        SMTP 설정 여부
        """
        if not SysOptions.smtp_config:
            return self.error("SMTP 설정이 되어있지 않습니다")
        data = request.data
        email = data["email"].lower()
        if email:
            
            auth_token = rand_str(length=8)
            """
            이메일이 존재하는 경우
            """
            if EmailAuthentication.objects.filter(email__iexact=email).exists():
                exist_email = EmailAuthentication.objects.filter(email__iexact=email).first()
                print(exist_email)
                # 이메일 인증 과정 중 DDoS 를 막기 위한 제한시간(60초) 설정
                if exist_email.verify_email_token_expire_time and 0 < int(
                      (exist_email.verify_email_token_expire_time - now()).total_seconds()) < 60:
                    return self.error("재전송은 1분마다 가능합니다.")
                else:
                    exist_email.verify_email_token = auth_token
                    exist_email.verify_email_token_expire_time = now() + timedelta(minutes=15)
                    exist_email.save()
            
            #이메일이 존재하지 않는 경우
            else:
                expire_time = now() + timedelta(minutes=15)
                new_email = EmailAuthentication.objects.create(email=email, verify_email_token=auth_token, verify_email_token_expire_time=expire_time)
                new_email.save()
            render_data = {
                "website_name": SysOptions.website_name,
                "token": auth_token
            }
            try:
                email_html = render_to_string("auth_token_email.html", render_data)
                send_email(smtp_config=SysOptions.smtp_config,
                           from_name=SysOptions.website_name_shortcut,
                           to_name="email 인증",
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
        else:
            return self.error("올바르지 않은 email 형식입니다")
