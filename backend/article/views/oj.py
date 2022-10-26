from datetime import timezone
from ..models import Article, BoardType, Comment, NotificationType, Notification, User
from utils.api import APIView, validate_serializer
from ..serializers import ArticleListSerializer, ArticleSerializer, ArticleCreateSerializer, ArticleModifySerializer, CommentListSerializer, CommentCreateSerializer, CommentModifySerializer, NotificationListSerializer
from account.decorators import login_required
from django.db.models import Q

class ArticleListAPI(APIView):
    """
    게시글 목록 출력 함수
    """
    def get(self, request):
        myself = request.GET.get("myself") # 자기 자신의 게시글만 확인하기 위한 데이터
        boardtype = request.GET.get("boardtype") # 게시판 타입 데이터
        sort = request.GET.get("sort") # 게시글 정렬 데이터
        search = request.GET.get("search") # 검색 데이터
        searchtype = request.GET.get("searchtype") # 검색 카테고리
        language = request.GET.get("language") # 검색 프로그래밍 언어
        
        # 게시판 타입 분류 시
        if (boardtype == "1"): # 1 = 자유 게시판인 경우
            articles = Article.objects.filter(boardtype = BoardType.FREE_BOARD)
        elif (boardtype == "2"): # 2 = 질문 게시판인 경우
            articles = Article.objects.filter(boardtype = BoardType.QUESTION_BOARD)
        elif (boardtype == "3"): # 3 = 요청 게시판인 경우
            articles = Article.objects.filter(boardtype = BoardType.REQUEST_BOARD)
        else: # 전체
            articles = Article.objects.all()

        # 자기 자신의 게시글 / 전체 게시글 분류 시
        if (myself and myself == "1"): # 1 - 자기 자신의 게시글만
            articles = articles.filter(username=request.user.username)

        # 게시글 정렬 시
        if (sort == "1"): # 좋아요 순 정렬인 경우
            articles = articles.order_by('-like_count', '-create_time')
        elif (sort == "2"): # 댓글 순 정렬인 경우
            articles = articles.order_by('-comment_count', '-create_time')

        # 게시글 검색 시
        if search:
            if (searchtype == "0"): # 전체 검색
                articles = articles.filter(Q (title__contains=search) | Q (content__contains=search) | Q (username__contains=search)).distinct()
            elif (searchtype == "1"): # 제목에서 검색
                articles = articles.filter(title__contains=search)
            elif (searchtype == "2"): # 내용에서 검색
                articles = articles.filter(content__contains=search)
            elif (searchtype == "3"): # 작성자명에서 검색
                articles = articles.filter(username__contains=search)

        # 질문 게시판의 경우 원하는 언어의 게시글만 출력
        if language:
            articles = articles.filter(problemtype=language)

        data = self.paginate_data(request, articles) # 페이징
        data["results"] = ArticleListSerializer(data["results"], many=True, user=request.user).data
        return self.success(data)


class ArticleCreateAPI(APIView):
    @login_required
    @validate_serializer(ArticleCreateSerializer)
    def post(self, request):
        data = request.data
        title = data["title"]
        content = data["content"]
        username = request.user.username
        boardtype = data["boardtype"]
        
        if (boardtype == "1"): # 자유 게시판인 경우
            boardtype = BoardType.FREE_BOARD
        elif (boardtype == "2"): # 질문 게시판인 경우
            boardtype = BoardType.QUESTION_BOARD
            problemtype = data["problemtype"]
            problemid = data["problemid"]
        elif (boardtype == "3"): # 요청 게시판인 경우
            boardtype = BoardType.REQUEST_BOARD
        else: # 선택을 안한 경우
            return self.error("게시판 타입을 선택하지 않았습니다")
            
        if Article.objects.exists(): # 게시글이 존재하는 경우
            latest_id = Article.objects.order_by('-id')[0].id + 1 # 생성 게시글 ID = 현재 존재하는 가장 높은 ID + 1
        else: # 아무 게시글도 없는 경우
            latest_id = 1 # 생성 게시글 ID = 1
        
        article = Article.objects.create(id = latest_id,
                                         writer = request.user,
                                         username = username,
                                         boardtype = boardtype,
                                         title = title,
                                         content = content)
        
        if (boardtype == BoardType.QUESTION_BOARD): # 질문 게시판의 경우
            article.problemtype = problemtype # 게시글에 언어 타입 작성 / Java, C, C++, Python
            article.problemid = problemid
        
        article.save() # 게시글 생성
        return self.success()
             

class ArticleAPI(APIView):
    """
    게시글 details 출력 함수
    """
    def get(self, request):
        article_id = request.GET.get("article_id") # 파라미터로 전송된 ID값을 통해 게시글 출력
        
        if article_id:
            article = Article.objects.get(id=article_id) # 해당 ID를 가진 게시글 가져옴
            article_data = ArticleSerializer(article).data
            # 현재 접속한 유저가 해당 게시글의 작성자 여부
            article_data["is_writer"] = (request.user.username == article.username)
            
            if article.like.filter(id = request.user.id).exists(): # 현재 접속한 유저가 해당 게시글의 좋아요를 이미 한 경우
                article_data["is_liked"] = True
            else:
                article_data["is_liked"] = False

            try: # 해당 ID를 가진 게시글에 달린 댓글 데이터
                comments = Comment.objects.filter(articleid=article_id).order_by('id') # 댓글을 가져옴
                for comment in comments:
                    comment.is_comment_writer = (request.user.username == comment.username) # 현재 접속한 유저가 해당 게시글에 달린 댓글의 작성자인지 확인하기 위한 데이터
                    try:
                      user = User.objects.get(username=comment.username)
                      comment.avatar = user.userprofile.avatar
                    except User.DoesNotExist:
                      comment.username = 'UnknownUser' #가입할 수 없는 아이디로 해당 아이디로 반환하여 특정함
                article_data["comments"] = CommentListSerializer(comments, many=True).data
            except Comment.DoesNotExist: # 해당 ID를 가진 댓글이 하나도 없는 경우
                article_data["comments"] = []
            return self.success(article_data) # username, title, content, create_time, is_writer, comments 데이터 전송
            
        else:
            return self.error("게시글이 존재하지 않습니다")
        

class ArticleDeleteAPI(APIView):
    """
    게시글 삭제 함수
    """
    def get(self, request):
        article_id = request.GET.get("article_id")
        if article_id:
            article = Article.objects.get(id=article_id) # 전송된 ID를 통해 게시글을 가져옴
            if request.user.username == article.username: # 해당 게시글 작성자와 현재 접속한 작성자가 같은 경우
                comments = Comment.objects.filter(articleid=article_id) # 해당 게시글의 작성된 댓글
                comments.delete() # 댓글 삭제
                article.delete() # 게시글 삭제
                return self.success()
            else: # 게시글 작성자가 아닌 경우
                return self.error("권한이 없습니다")
        else:
            return self.error("게시글이 존재하지 않습니다")

class ArticleModifyAPI(APIView):
    """
    게시글 수정 함수
    """
    @login_required
    @validate_serializer(ArticleModifySerializer)
    def post(self, request):
        data = request.data
        title = data["title"]
        content = data["content"]
        article_id = data["id"] # 수정과 달리 이미 존재하는 게시글의 ID를 전송 받음
        
        if article_id:
            article = Article.objects.get(id=article_id) # 전송받은 ID를 가진 게시글을 수정함 / 신규 생성 X
            article.title = title
            article.content = content
            article.save()
            return self.success()
        else:
            return self.error("게시글이 존재하지 않습니다")


class CommentCreateAPI(APIView):
    """
    댓글 작성 함수
    """
    @login_required
    @validate_serializer(CommentCreateSerializer)
    def post(self, request):
        data = request.data
        content = data["content"] # 작성할 댓글 내용
        articleid = data["articleid"] # 댓글을 작성할 게시글 ID
        if content:
            article = Article.objects.get(id=articleid)
            article.comment_count += 1 # 댓글을 작성할 게시글의 댓글 수 1 증가
            article.save() # 저장
            user = User.objects.get(username=request.user.username)
            avatar = user.userprofile.avatar
            Comment.objects.create(articleid=articleid,
                                   avatar=avatar,
                                   username=request.user.username,
                                   content=content)
            
            url = "/article/" + str(articleid)
            short_content = "[" + article.title + "]글에 댓글이 달렸습니다."
            if article.username != request.user.username:
                Notification.objects.create(target_username=article.username,
                                    action_username=request.user.username,
                                    notificationtype=NotificationType.COMMENT,
                                    content=short_content,
                                    comment_content = content,
                                    url=url)
            return self.success()
            
        else:
            return self.error("내용이 비어있습니다")

class CommentDeleteAPI(APIView):
    """
    댓글 삭제 함수
    """
    def get(self, request):
        comment_id = request.GET.get("id") # 삭제할 댓글의 ID
        if comment_id:
            comment = Comment.objects.get(id=comment_id) # 전송된 ID를 통해 댓글을 가져옴
            article = Article.objects.get(id=comment.articleid) # 해당 댓글이 작성된 게시글을 가져옴
            article.comment_count -= 1 # 게시글의 댓글 수 1 감소
            article.save() # 저장
            comment.delete() # 댓글 삭제
            return self.success()
        else:
            return self.error("해당 댓글이 존재하지 않습니다")

class CommentModifyAPI(APIView):
    """
    댓글 수정 함수
    """
    @login_required
    @validate_serializer(CommentModifySerializer)
    def post(self, request):
        data = request.data
        id = data["id"] # 수정할 댓글의 ID
        content = data["content"] # 수정할 댓글의 내용
        if id:
            comment = Comment.objects.get(id=id)
            comment.content = content # 댓글 내용 수정
            comment.save() # 저장
            return self.success()
        else:
            return self.error("해당 댓글이 존재하지 않습니다")

class ArticleLikeAPI(APIView):
    """
    좋아요 함수
    """
    @login_required
    def get(self, request):
        article_id = request.GET.get("article_id") # 좋아요할 게시글의 ID
        if article_id:
            article = Article.objects.get(id=article_id) # 전송된 ID를 통해 게시글을 가져옴
            if article.like.filter(id = request.user.id).exists(): # 현재 접속한 유저가 해당 게시글의 좋아요를 이미 한 경우
                article.like.remove(request.user) # 좋아요 삭제
                article.like_count -= 1 # 좋아요 수 1 감소
                article.save()
                
                url = "/article/" + str(article.id)
                Notification.objects.filter(Q (target_username=article.username) & Q (action_username=request.user.username) & Q (url=url) & Q (notificationtype=NotificationType.LIKE)).delete()

                return self.success()
            else: # 현재 접속한 유저가 해당 게시글의 좋아요를 아직 안 한 경우
                article.like.add(request.user) # 좋아요 추가
                article.like_count += 1 # 좋아요 수 1 증가
                article.save()

                url = "/article/" + str(article.id)
                content = "[" + article.title + "]글에 좋아요를 받았습니다."
                if article.username != request.user.username:
                    Notification.objects.create(target_username=article.username,
                                    action_username=request.user.username,
                                    notificationtype=NotificationType.LIKE,
                                    content=content,
                                    url=url)

                return self.success()
        else:
            return self.error("해당 게시글이 존재하지 않습니다")

class NotificationListAPI(APIView):
    """
    알림 출력 함수
    """
    def get(self, request):
        notifications = Notification.objects.filter(target_username = request.user.username).order_by('-create_time')
        notifications = NotificationListSerializer(notifications, many=True).data
        return self.success(notifications)

class NotificationDeleteAPI(APIView):
    """
    알림 삭제 함수
    """
    def get(self, request):
        notification_id = request.GET.get("notification_id")
        if notification_id:
            notification = Notification.objects.get(id=int(notification_id))
            notification.delete()
            return self.success()
        else:
            return self.error("해당 알림이 존재하지 않습니다")

class NotificationCheckAPI(APIView):
    """
    알림 확인 함수
    """
    def get(self, request):
        notification_id = request.GET.get("notification_id")
        if notification_id:
            notification = Notification.objects.get(id=int(notification_id))
            notification.is_read = True
            #notification.read_time = timezone.now()
            notification.save()
            return self.success()
        else:
            return self.error("해당 알림이 존재하지 않습니다")

class ReadNotificationAPI(APIView):
    def get(self, request):
        notifications = Notification.objects.filter(Q (target_username = request.user.username) & Q (is_read = False)).order_by('-create_time')
        notifications = NotificationListSerializer(notifications, many=True).data
        return self.success(notifications)
        # read_notification_num = notifications.count()
        # return self.success(read_notification_num)

class CommentArticleListAPI(APIView):
    def get(self, request):
        username = request.user.username
        
        comments = Comment.objects.filter(username = username)

        comment_ids  = []

        for comment in comments:
            comment_ids.append(comment.articleid)

        articles = Article.objects.filter(id__in = comment_ids)
        data = self.paginate_data(request, articles) # 페이징
        data["results"] = ArticleListSerializer(data["results"], many=True, user=request.user).data
        return self.success(data)

class LikeArticleListAPI(APIView):
    def get(self, request):
        articles = request.user.likes.all()
        data = self.paginate_data(request, articles) # 페이징
        data["results"] = ArticleListSerializer(data["results"], many=True, user=request.user).data
        return self.success(data)
