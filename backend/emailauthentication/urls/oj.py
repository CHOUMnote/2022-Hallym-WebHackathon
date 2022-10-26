from django.conf.urls import url

from ..views.oj import (EmailAuthenticationAPI, MakeEmailAuthenticationTokenAPI)

urlpatterns = [
    url(r"^auth_email_call/?$", MakeEmailAuthenticationTokenAPI.as_view(), name="make_email_authentication_token"),
    url(r"^authed_email/?$", EmailAuthenticationAPI.as_view(), name="email_authentication")
]
