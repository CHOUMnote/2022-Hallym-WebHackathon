from django.db import models

class EmailAuthentication(models.Model):
    """
    이메일 인증을 위한 임시 객체 모델
    """
    email = models.TextField(null=True)   # 인증 할 이메일
    verify_email_token = models.TextField(null=True)  # 이메일 토큰
    verify_email_token_expire_time = models.DateTimeField(null=True)  # 이메일 인증 제한 시간
    class Meta:
        db_table = "emailauthentication"