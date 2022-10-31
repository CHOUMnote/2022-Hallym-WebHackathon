from django.conf.urls import url
from ..views.oj import CreateReviewAPI,DeleteReviewAPI,ReviewModifyAPI,ReviewAPI,Pageinfo

urlpatterns = [
    url(r"^create_review/?$", CreateReviewAPI.as_view(), name="create_review"),
    url(r"^delete_review/?$", DeleteReviewAPI.as_view(), name="delete_review"),
    url(r"^modify_review/?$", ReviewModifyAPI.as_view(), name="modify_review"),
    url(r"^review_list/?$", ReviewAPI.as_view(), name="review_list"),
    url(r"^review_list/?$", ReviewAPI.as_view(), name="review_list"),
    
    url(r"^page_info/?$", Pageinfo.as_view(), name="page_info"),
    
]
