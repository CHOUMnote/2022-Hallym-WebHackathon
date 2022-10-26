"""
import os
from ..decorators import super_admin_required
from board.models import Board
from board.serializers import BoardSerializer, CreateBoardSerializer 

class BoardAdminAPI(APIView):
    @validate_serializer(CreateBoardSerializer)
    @super_admin_required
    def post(self, request):

        data = request.data
        board = Board.objects.create(title=data["title"], content=data["board_type"])
        return self.success(BoardSerializer(board).data)
    
    @super_admin_required
    def get(self, request):

        board_title = request.GET.get("title")
        if board_title:
            try:
                board = Board.objects.get(id=board_title)
                return self.success(BoardSerializer(board).data)
            except Board.DoesNotExist:
                return self.error("Board does not exist")
        board = Board.objects.all().order_by("-title")
        return self.success(self.paginate_data(request, board, BoardSerializer))

    @super_admin_required
    def delete(self, request):
        if request.GET.get("title"):
            Board.objects.filter(title=request.GET["title"]).delete()
        return self.success()
"""