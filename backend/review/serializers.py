from utils.api import serializers
from .models import Review, ReadCount, PageInfo

class ReviewListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class ReadCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadCount
        fields = '__all__'
        
class PageInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageInfo
        fields = '__all__'
