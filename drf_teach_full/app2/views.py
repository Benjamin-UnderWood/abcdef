from .models import User, Topic, Post
from .serializers import PostSerializer, UserSerializer, TopicSerializer, PostSerializer2
from rest_framework.viewsets import ModelViewSet
from rest_framework.authentication import TokenAuthentication, BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, IsAuthenticatedOrReadOnly
from app2.auth import MyAuthentication
from rest_framework import generics
from rest_framework import views
from rest_framework import throttling
from rest_framework import filters, status



from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TopicViewSet(ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer



from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework import pagination
from app2 import paginators
from rest_framework import versioning
from rest_framework import negotiation
from rest_framework import metadata


class PostViewSet(ModelViewSet):
    """
    list:
        显示所有的文章对象
    create:
        创建一篇文章
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter)
    filterset_fields = ('title', 'content')
    search_fields = ('=title', '^user__username')
    ordering_fields = ('title', 'user')  # 可以用来排序的字段
    ordering = ('title', 'content')  # 默认初始排序的结果
    metadata_class = metadata.SimpleMetadata


    # def get_serializer_class(self):
    #     if self.request.version == 'v1':
    #         return PostSerializer
    #     else:
    #         return PostSerializer2

# @api_view(('GET',))
# def foo(request, format=None):
#     pass
#
# class Foo(APIView):
#
#     def get(self,request, format=None):
#         pass

# from rest_framework.reverse import reverse


# path('/posts/<int:pk>/', views.Foo.as_view(), name='post-detail')

# class Foo(views.APIView):
#     def get(self,request):
#         post_id = 12
#
#         current_post_url = reverse('post-detail', arg=[post_id], request=request)  # 在Python的代码中解析或生成url
#         return Respone(current_post_url)

# from rest_framework.views import exception_handler
#
# def my_exception_handler(exc, context):
#
#     response = exception_handler(exc, context)  # 把默认的DRF帮我们做的异常处理工作，先干了
#     if response is not None:
#         response.data['status_code'] = response.status_code
#
#     return response

from rest_framework.settings import api_settings