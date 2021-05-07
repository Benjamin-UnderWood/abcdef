

from django.urls import path, include
from snippets import views

from rest_framework.urlpatterns import format_suffix_patterns

from snippets.views import SnippetViewSet, UserViewSet
from rest_framework import renderers

# 第一种路由
snippet_list = SnippetViewSet.as_view({
    'get': 'list',
    'post': 'create',
})
snippet_detail = SnippetViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',  # 局部更新
    'delete': 'destroy'
})

snippet_highlight = SnippetViewSet.as_view({
    'get': 'highlight',

}, renderer_classes=[renderers.StaticHTMLRenderer])

user_list = UserViewSet.as_view({
    'get': 'list'
})

user_detail = UserViewSet.as_view({
    'get': 'retrieve'
})

# 第二种路由
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'vs2/ddd', views.SnippetViewSet)
router.register(r'vs2/users', views.UserViewSet)

urlpatterns = [

    path('snippets/', views.snippet_list),
    path('snippets/<int:pk>/', views.snippet_detail),

    # api_view装饰器
    path('snippets-drf/', views.drf_snippet_list),
    path('snippets-drf/<int:pk>/', views.drf_snippet_detail),

    # apiview视图
    path('snippets-view/', views.SnippetList.as_view()),
    path('snippets-view/<int:pk>/', views.SnippetDetail.as_view()),

    # 使用mixin
    path('snippets-mixin/', views.SnippetMixinList.as_view()),
    path('snippets-mixin/<int:pk>/', views.SnippetMixinDetail.as_view()),

    # 使用组合类
    path('snippets-zuhe/', views.SnippetListZuhe.as_view(), name='snippet-list'),
    path('snippets-zuhe/<int:pk>/', views.SnippetDetailZuhe.as_view(), name='snippet-detail'),

    # user展示
    path('snippets-users/', views.UserList.as_view(), name='user-list'),
    path('snippets-users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),

    # 根路由
    path('abc/', views.api_root),

    # 代码高亮
    path('snippets/<int:pk>/hl/', views.SnipperHighlight.as_view(), name='snippet-highlight'),


    # router 第一种
    path('vs1/snippets/', snippet_list, name='snippet-list'),
    path('vs1/snippets/<int:pk>/', snippet_detail, name='snippet-detail'),
    path('vs1/snippets/<int:pk>/hl', snippet_highlight, name='snippet-highlight'),

    path('vs1/users/', user_list, name='user-list'),
    path('vs1/users/<int:pk>/', user_detail, name='user-detail'),

    path('', include(router.urls))
]

# urlpatterns = format_suffix_patterns(urlpatterns)  #  加后缀 让他支持带.json, .html方式