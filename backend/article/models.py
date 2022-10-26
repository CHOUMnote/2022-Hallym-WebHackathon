from django.db import models

from account.models import User
from django.conf import settings

class BoardType(object):
    """
    게시글 타입 객체 - 추후 추가 예정
    """
    FREE_BOARD = "FREE"
    QUESTION_BOARD = "QUESTION"
    REQUEST_BOARD = "REQUEST"


class Article(models.Model):
    """
    게시글 객체
    """
    id = models.IntegerField(primary_key=True, db_index=True) # 게시글 고유 ID
    writer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    username = models.TextField(null=False)
    boardtype = models.TextField(null=False) # 게시글 타입

    title = models.CharField(max_length=20, null=True)
    content = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now=True) # 수정 예정

    like = models.ManyToManyField(User, related_name='likes', blank=True)
    like_count = models.PositiveIntegerField(default=0)

    comment_count = models.PositiveIntegerField(default=0)

    problemtype = models.TextField(null=True, blank=True) # 질문 게시글의 질문 관련 언어
    problemid = models.TextField(null=True, blank=True) # 질문 게시글의 질문 관련 문제 ID
    
    class Meta:
        db_table = "article"
        ordering = ("-create_time",)


class Comment(models.Model):
    """
    게시글 댓글 객체
    """
    articleid = models.IntegerField() # 해당 댓글 객체가 작성된 게시글 ID
    username = models.TextField(null=False)
    avatar = models.TextField(default=f"{settings.AVATAR_URI_PREFIX}/default.png")
    content = models.TextField(null=False)
    create_time = models.DateTimeField(auto_now_add=True)
    is_comment_writer = models.NullBooleanField()

class NotificationType(object):
    """
    알림 타입 객체
    """
    LIKE = "LIKE"
    COMMENT = "COMMENT"

class Notification(models.Model):
    """
    알림 객체
    """
    #id = models.IntegerField(primary_key=True, db_index=True) # 알림 고유 ID
    create_time = models.DateTimeField(auto_now_add=True) # 알림 생성 시각
    read_time = models.DateTimeField(null=True) # 알림 읽은 시각
    is_read = models.BooleanField(default=False) # 알림 읽기 여부
    url = models.TextField(null=False) # 알림이 발생한 경로
    target_username = models.TextField(null=False) # 알림을 받는 회원 이름
    action_username = models.TextField(null=False) # 알림을 생성한 회원 이름
    notificationtype = models.TextField(null=False) # 알림 타입 - 댓글 / 좋아요
    content = models.TextField(null=False) # 알림 내용
    comment_content = models.TextField(null=True) # Comment일 경우 content를 담아둠