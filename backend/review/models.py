from django.db import models
from account.models import User
from django.conf import settings

class Review(models.Model):
    """
    리뷰 객체
    """
    articleid = models.IntegerField() # 해당 댓글 객체가 작성된 게시글 ID
    username = models.TextField(null=False)
    avatar = models.TextField(default=f"{settings.AVATAR_URI_PREFIX}/default.png")
    content = models.TextField(null=False)
    star = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    #is_comment_writer = models.NullBooleanField()
    
class ReadCount(models.Model):
  articleid = models.IntegerField()
  count = models.IntegerField(default=0)

class PageInfo(models.Model):
  articleid = models.IntegerField()
  starCount = models.IntegerField(default=0)
  sumStar = models.IntegerField(default=0)
  avgStar = models.TextField(default=0)
  visitorCount = models.IntegerField(default=0)
  