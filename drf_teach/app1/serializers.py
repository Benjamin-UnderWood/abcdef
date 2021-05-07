from rest_framework import serializers

from app1.models import Post
from rest_framework.serializers import ModelSerializer

class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created')

    def validate_title(self, value):  # value 初始值

        if 'drf' not in value.lower():
            raise serializers.ValidationError("Post 必须和DRF相关")
        return value


def multiple_of_ten(value):
    if value % 10 != 0:
        raise serializers.ValidationError('Not a multiple of ten')

class GameRecord(serializers.Serializer):
    score = serializers.IntegerField(validators=[multiple_of_ten])



class PostBSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'content')

