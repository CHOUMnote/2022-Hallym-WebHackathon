from utils.api import serializers
from .models import Article, Comment, Notification


class ArticleListSerializer(serializers.ModelSerializer):
    """
    게시글 목록 전송용
    """
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

    class Meta:
        model = Article
        exclude = ("last_update_time", "content", "writer")

class ArticleSerializer(serializers.ModelSerializer):
    """
    게시글 detail용
    """
    class Meta:
        model = Article
        exclude = ("id", "writer", "last_update_time")

class ArticleCreateSerializer(serializers.Serializer):
    """
    게시글 생성용
    """
    title = serializers.CharField()
    content = serializers.CharField()
    boardtype = serializers.CharField()
    problemtype = serializers.CharField(allow_blank=True)
    problemid = serializers.CharField(allow_blank=True)

class ArticleModifySerializer(serializers.Serializer):
    """
    게시글 수정용
    """
    title = serializers.CharField()
    content = serializers.CharField()
    id = serializers.IntegerField()

class CommentListSerializer(serializers.ModelSerializer):
    """
    댓글 출력용
    """
    class Meta:
        model = Comment
        fields = '__all__'

class CommentCreateSerializer(serializers.Serializer):
    content = serializers.CharField()
    articleid = serializers.IntegerField()

class CommentModifySerializer(serializers.Serializer):
    content = serializers.CharField()
    id = serializers.IntegerField()

class NotificationListSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Notification
        fields = '__all__'