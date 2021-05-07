from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import User, Topic, Post


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username')


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = ('id', 'name')


class PostSerializer(ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'created', 'user', 'topics')






