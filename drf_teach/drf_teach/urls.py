"""drf_teach URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.renderers import CoreJSONRenderer, CoreAPIJSONOpenAPIRenderer, JSONOpenAPIRenderer

from app1 import views

from django.contrib.auth.models import User
from rest_framework import routers, serializers, viewsets, renderers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', "email", 'is_staff')


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


router = routers.DefaultRouter()
router.register(r'admin/users', UserViewSet)  # 把url 映射到某个视图上面去

from rest_framework.schemas import get_schema_view

# =========返回yaml格式, 尝试返回json失败============
# class JSONOpenAPIRenderer(renderers.OpenAPIRenderer):
#     media_type = 'application/json'
#
#
# schemas_view = get_schema_view(title='qwer', renderer_classes=[JSONOpenAPIRenderer])  # 保存一个视图
# =========返回yaml格式, 尝试返回json失败============

# schemas_view = get_schema_view(title='qwer', renderer_classes=[CoreJSONRenderer])  # 保存一个视图
schemas_view = get_schema_view(title='qwer')  # 保存一个视图

# 查看几个drf 的核心文件
import rest_framework.fields  # 1800
import rest_framework.serializers  # 1600
import rest_framework.permissions  # 300

urlpatterns = [
    path('admin/', admin.site.urls),
    # FBV
    path('users/', views.userList),
    # CBV
    path('users_cbv/', views.UserList.as_view()),

    # drf urls
    path('api-auth/', include('rest_framework.urls')),

    # 简单例子 注册router
    # path('', include(router.urls)),  # 访问的路径  127.0.0.1:8000/admin/users

    # api视图
    path('schema/', schemas_view),


    #########################################
    ################# 入门实例 ##################
    #########################################

    path('', include('snippets.urls')),

    ####### GenericView 源码分析 ########
    path('app1/', include('app1.urls')),


    ####### 关系字段序列化 ########
    path('app2/', include('app2.urls')),
]
