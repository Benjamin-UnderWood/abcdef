from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions


class MyAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        username = request.META.get('HTTP_MYUSERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('没有这个用户！')
        return (user, None)   # (request.user, request.auth)
