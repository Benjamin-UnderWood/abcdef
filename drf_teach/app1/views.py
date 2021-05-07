from time import time

from django.shortcuts import render, HttpResponse, get_object_or_404
import json

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

# ======================================== #
# =================FBV==================== #
# ======================================== #
from rest_framework.parsers import FileUploadParser, BaseParser
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer, StaticHTMLRenderer, AdminRenderer

from app1.models import Post

user_dict = {
    'username': 'tom',
    'sex': '男',
    'age': 18
}



@csrf_exempt
def userList(request):

    # return HttpResponse(user_dict)
    # 不序列化直接返回的是什么?
    # 返回值 usernamesexage
    # 因为返回的不是json 数据格式

    if request.method == 'GET':
        # return HttpResponse(json.dumps(user_dict), content_type='application/json')
        return JsonResponse(user_dict, content_type='application/json')

    if request.method == 'POST':

        print("---------", request.body)
        print('******', request.body.decode('utf8'))
        body = json.loads(request.body)
        print("++++++++", body)
        # return HttpResponse(json.dumps(body), content_type='application/json')
        return JsonResponse(body, content_type='application/json')

# ======================================== #
# =================FBV==================== #
# ======================================== #



# ======================================== #
# =================CBV==================== #
# ======================================== #

from django.utils.decorators import method_decorator


@method_decorator(csrf_exempt, name='dispatch')
class UserList(View):

    def get(self, request):
        return JsonResponse(user_dict, content_type='application/json')

    def post(self, request):
        body = json.loads(request.body)
        print('----', body)
        return JsonResponse(body, content_type='application/json')



# ======================================== #
# =================查看GenericView 的钩子==================== #
# ======================================== #


from app1.serializers import PostSerializer, PostBSerializer
from rest_framework import generics, views
from rest_framework.response import Response

class PostList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # renderer_classes = (JSONRenderer, )

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        serializer = serializer(queryset, many=True)
        return Response(serializer.data)

    def get_serializer_class(self):
        if self.request.user.is_staff:
            return PostSerializer
        return PostBSerializer


from rest_framework import mixins


class PostDetail(mixins.RetrieveModelMixin,
                 mixins.UpdateModelMixin,
                 mixins.DestroyModelMixin,
                 generics.GenericAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class MultipleFieldLookupMixin:
    def get_object(self):
        """
        要覆盖genericAPIView中自带的 get_object() 方法
        之重写一部分
        :return:
        """

        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        filter = {}
        for field in self.lookup_fields:
            if self.kwargs[field]:
                filter[field] = self.kwargs[field]

        obj = get_object_wor_404(queryset, **filter)
        self.check_object_permissions(self.request, obj)
        return obj


class RetrievePostView(MultipleFieldLookupMixin, generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_fields = ('pk', 'title',)





class FileUploadView(views.APIView):
    def post(self, request):
        print("当前时间: ", time())
        print('request.body ++++++', request.body)
        print('request.data ++++++', request.data)
        with open(r'uploads/2.jpg', 'wb') as f:
            f.write(request.body)

        return Response("200, ok")


class FileUploadParserView(views.APIView):
    parser_classes = (FileUploadParser,)

    def post(self, request, filename):
        print("当前时间: ", time())
        print('request.body ++++++', request.body)
        print('request.data ++++++', request.data)

        fileobj = request.data['file']
        return Response(status=204)



class PlainTextParser(BaseParser):
    media_type = 'text/plain'

    def parse(self, stream, media_type=None, parser_context=None):
        return stream.read()


class FileUploadPlainView(views.APIView):
    parser_classes = (PlainTextParser,)

    def post(self, request, filename):
        print("当前时间: ", time())
        print('request.body ++++++', request.body)
        print('request.data ++++++', request.data)


        # with open(f'uploads/3.txt', 'wb') as f:
        #     f.write(request.data)
        return Response(status=204)



class PostTemplateList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # renderer_classes = (JSONRenderer, )
    renderer_classes = (TemplateHTMLRenderer, )

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer_class()
        serializer = serializer(queryset, many=True)
        return Response({'post': serializer.data}, template_name='posts.html')

class PostStaticList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = (StaticHTMLRenderer, )

    def get(self, request, *args, **kwargs):
        data = "<html><body><h1>hello world</h1></body></html>"
        return Response(data)


class PostAdminList(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    renderer_classes = (AdminRenderer, )