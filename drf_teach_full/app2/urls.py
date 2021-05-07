from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'topics', views.TopicViewSet, basename='topic')
router.register(r'posts', views.PostViewSet, basename='post')


urlpatterns = router.urls


# urlpatterns += [
#     path('posts/<str:username>/v2/', views.PostList.as_view())
# ]

# from rest_framework.urlpatterns import format_suffix_patterns
#
# urlpatterns= [...]
#
#
# urlpatterns = format_suffix_patterns(urlpatterns)