from utils.api import serializers

class EmailAuthenticationSerializer(serializers.Serializer):
    """
    email 인증용
    """
    email = serializers.EmailField()  # 인증 할 이메일
    token = serializers.CharField() # 입력 할 token

class MakeEmailAuthenticationTokenSerializer(serializers.Serializer):
    """
    email 인증에 필요한 token발급기
    """
    email = serializers.EmailField()  # token발급할 이메일
