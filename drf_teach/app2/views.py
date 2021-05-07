from app2.models import Topic, User, Post

from app2.serializers import PostSerializer, TopicSerializer, UserSerializer, PostBSerializer, PostHyperlinkedSerializer

from rest_framework.viewsets import ModelViewSet


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer


class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostHyperlinkedSerializer
