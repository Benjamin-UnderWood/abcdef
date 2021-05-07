from django.urls import path
from app1 import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('poststpl/', views.PostTemplateList.as_view()),
    path('postsstatic/', views.PostStaticList.as_view()),
    path('postsadmin/', views.PostAdminList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('posts/<int:pk>/<str:title>/', views.RetrievePostView.as_view()),
    path('upload/', views.FileUploadView.as_view()),
    path('upload/<str:filename>/', views.FileUploadParserView.as_view()),
    path('plain/<str:filename>/', views.FileUploadPlainView.as_view()),
]
from rest_framework import serializers