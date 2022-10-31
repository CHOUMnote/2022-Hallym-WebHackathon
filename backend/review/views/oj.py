import random
from django.db.models import Q, Count
from account.decorators import login_required
from utils.api import APIView, validate_serializer
from ..models import ReadCount, Review, User, PageInfo
from ..serializers import ReviewListSerializer, ReadCountSerializer, PageInfoSerializer

class CreateReviewAPI(APIView):
    """
    리뷰 작성 함수
    """
    @login_required
    def get(self, request):
        data = request.data
        content = data["content"] # 작성할 댓글 내용
        articleid = data["articleid"] # 리뷰을 작성할 게시글 ID
        score = data["star"]#평점 정보
        
        if content:
            user = User.objects.get(username=request.user.username)
            avatar = user.userprofile.avatar
            Review.objects.create(articleid=articleid,
                                   avatar=avatar,
                                   username=request.user.username,
                                   content=content,
                                   star=score)
            
            page = PageInfo.objects.get(articleid=articleid)
            page.starCount += 1
            page.sumStar += int(score)
            page.avgStar = int(page.sumStar)/page.starCount
            page.save()
            
            return self.success("리뷰 작성 성공")
            
        else:
            return self.error("내용이 비어있습니다")
        
class DeleteReviewAPI(APIView):
    """
    리뷰 삭제 함수
    """
    def get(self, request):
        review_id = request.GET.get("id") # 삭제할 리뷰의 ID
        if review_id:
            comment = Review.objects.get(id=review_id)
            #article = Article.objects.get(id=comment.articleid)
            #article.comment_count -= 1
            #article.save()
            comment.delete() # 댓글 삭제
            return self.success()
        else:
            return self.error("해당 리뷰가 존재하지 않습니다")
        
class ReviewModifyAPI(APIView):
    """
    리뷰 수정 함수
    """
    @login_required
    def get(self, request):
        data = request.data
        id = data["id"] 
        content = data["content"] 
        if id:
            comment = Review.objects.get(id=id)
            comment.content = content
            comment.save() # 저장
            return self.success()
        else:
            return self.error("해당 리뷰가 존재하지 않습니다")
        
class ReviewAPI(APIView):
    def get(self, request):
        article_id = request.GET.get("article_id")
        
        reviews = Review.objects.filter(articleid=article_id).order_by('id') # 댓글을 가져옴
        result = ReviewListSerializer(reviews,many=True).data
        return self.success(result)
            
class Pageinfo(APIView):
    def get(self, request):
        article_id = request.GET.get("article_id")
        page = PageInfo.objects.get(articleid=article_id)
        result = PageInfoSerializer(page).data
        return self.success(result)

# class ReviewCountAPI(APIView):
#     def get(self, request):
#         qr = Review.objects.all()
#         count = qr.count()
#         return self.success()

class ReadCountAPI(APIView):
    def get(self, request):
        data = request.data
        aid = data["id"] 
        try:
            obj = ReadCount.objects.get(articleid=aid)
        except:
            obj = ReadCount.objects.create(articleid=aid)
        return self.success(ReadCountSerializer(obj).data)

class VisiteAPI(APIView):
    def get(self, request):
        data = request.data
        aid = data["id"] 
        try:
            obj = ReadCount.objects.get(articleid=aid)
        except:
            return self.error()
        obj.count += 1
        obj.save()
        return self.success(ReadCountSerializer(obj).data)