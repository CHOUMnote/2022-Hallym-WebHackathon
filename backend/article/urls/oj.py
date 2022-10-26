from django.conf.urls import url

from ..views.oj import (ArticleListAPI, ArticleCreateAPI, ArticleAPI, ArticleDeleteAPI, 
                        ArticleModifyAPI, CommentCreateAPI, CommentDeleteAPI, ArticleLikeAPI, CommentModifyAPI,
                        NotificationListAPI, NotificationCheckAPI, NotificationDeleteAPI, ReadNotificationAPI,
                        CommentArticleListAPI, LikeArticleListAPI)

urlpatterns = [
    url(r"^article_list/?$", ArticleListAPI.as_view(), name="article_list"),
    url(r"^create_article/?$", ArticleCreateAPI.as_view(), name="create_article"),
    url(r"^article/?$", ArticleAPI.as_view(), name="article"),
    url(r"^delete_article/?$", ArticleDeleteAPI.as_view(), name="delete_article"),
    url(r"^modify_article/?$", ArticleModifyAPI.as_view(), name="modify_article"),
    url(r"^create_comment/?$", CommentCreateAPI.as_view(), name="create_comment"),
    url(r"^delete_comment/?$", CommentDeleteAPI.as_view(), name="delete_comment"),
    url(r"^like_article/?$", ArticleLikeAPI.as_view(), name="like_article"),
    url(r"^modify_comment/?$", CommentModifyAPI.as_view(), name="modify_comment"),
    url(r"^notification_list/?$", NotificationListAPI.as_view(), name="notification_list"),
    url(r"^delete_notification/?$", NotificationDeleteAPI.as_view(), name="delete_notification"),
    url(r"^check_notification/?$", NotificationCheckAPI.as_view(), name="check_notification"),
    url(r"^read_notification/?$", ReadNotificationAPI.as_view(), name="read_notification"),
    url(r"^comment_article_list/?$", CommentArticleListAPI.as_view(), name="comment_article_list"),
    url(r"^like_article_list/?$", LikeArticleListAPI.as_view(), name="like_article_list"),
]
