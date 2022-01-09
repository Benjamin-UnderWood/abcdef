from django.urls import path

from celerydemo.views import TestView

urlpatterns = [
    path("abc/", TestView.as_view()),
]