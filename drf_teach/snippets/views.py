from django.shortcuts import render

# Create your views here.


from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from rest_framework import permissions, renderers

from snippets.models import Snippet
from snippets.serializers import SnippetModelSerializer, UserHyperlinkSerializer, SnippetHyperlinkSerializer


# 根视图
# 1. 列出所有代码片段
# 2. 创建一个新的snippet

@csrf_exempt
def snippet_list(request):
    if request.method == 'GET':
        snippets = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippets, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = SnippetModelSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)  # 只有通过验证serializer 保存成功后就可以得到data
        return JsonResponse(serializer.errors, status=400)  # 400 json参数认证错误


@csrf_exempt
def snippet_detail(request, pk):  # 针对某一个代码片段的更新删除
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:  # 不存在这个对象
        return HttpResponse(status=404)  # 404 找不到资源

    if request.method == 'GET':
        serializer = SnippetModelSerializer(snippet)
        return JsonResponse(serializer.data)

    if request.method == 'PUT':
        data = JSONParser().parse(request)
        # 在更新实例的时候必须要知道我们要更新哪一个实例
        serializer = SnippetModelSerializer(snippet, data=data)

        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.data, status=400)  # 400 json 参数认证错误

    if request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=204)  # 204 删除成功




###################################################################################
################################### DRF函数视图编写 ##################################
###################################################################################


from rest_framework import status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response


from snippets.models import Snippet
from snippets.serializers import SnippetModelSerializer


@api_view(['GET', 'POST'])
def drf_snippet_list(request, format=None):  # drf 对request 做了进一步封装
    if request.method == 'GET':
        snippet = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippet, many=True)
        print('------------', type(serializer.data)) # RunDict
        return Response(serializer.data)

    if request.method == 'POST':
        # 我们不需要再自己去解析数据了
        print('+++++++++++++++', type(request.data))
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)



@api_view(['GET', 'PUT', 'DELETE'])
def drf_snippet_detail(request, pk, format=None):  # 针对某一个代码片段的更新删除
    try:
        snippet = Snippet.objects.get(pk=pk)
    except Snippet.DoesNotExist:  # 不存在这个对象
        return Response(status=status.HTTP_404_NOT_FOUND)  # 404 找不到资源

    if request.method == 'GET':
        serializer = SnippetModelSerializer(snippet)
        return Response(serializer.data)

    if request.method == 'PUT':
        # 在更新实例的时候必须要知道我们要更新哪一个实例
        serializer = SnippetModelSerializer(snippet, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)  # 400 json 参数认证错误

    if request.method == 'DELETE':
        snippet.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)  # 204 删除成功

###################################################################################
################################### DRF函数视图编写 ##################################
###################################################################################







###################################################################################
################################### DRF类视图编写 ##################################
###################################################################################

from django.http import Http404
from rest_framework.views import APIView



class SnippetList(APIView):

    def get(self, request, format=None):
        snippets = Snippet.objects.all()
        serializer = SnippetModelSerializer(snippets, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = SnippetModelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)


class SnippetDetail(APIView):

    def get_object(self, pk):
        try:
            snippet = Snippet.objects.get(pk=pk)
            return snippet
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk,  format=None):
        snippet = self.get_object(pk)
        serializer = SnippetModelSerializer(snippet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request,pk,  format=None):

        snippet = self.get_object(pk)
        serializer = SnippetModelSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_422_UNPROCESSABLE_ENTITY)

    def delete(self, request, pk,  format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)





###################################################################################
################################### DRF类视图编写 ##################################
###################################################################################



###################################################################################
################################### DRFmixin编写 ##################################
###################################################################################

from rest_framework import mixins
from rest_framework import generics


class SnippetMixinList(mixins.ListModelMixin,
                       mixins.CreateModelMixin,
                       generics.GenericAPIView):

    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):  # 样板
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class SnippetMixinDetail(mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin,
                         generics.GenericAPIView):

    queryset = Snippet.objects.all()
    serializer_class = SnippetModelSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


###################################################################################
################################### DRFmixin编写 ##################################
###################################################################################



#==================================================================================#
################################### DRF generic封装view 编写 ########################
#==================================================================================#



class SnippetListZuhe(generics.ListCreateAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetHyperlinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)  # 这个视图当前应该遵守的权限

    def perform_create(self, serializer):  # 针对哪一个序列化器的对象我要执行,创建的方法
        """创建 对象时如何提供用户信息"""
        serializer.save(owner=self.request.user)


from snippets.permissions import IsOwnerOrReadOnly


class SnippetDetailZuhe(generics.RetrieveUpdateDestroyAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetHyperlinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)  # 这个视图当前应该遵守的权限
    


#==================================================================================#
################################### DRF generic封装view 编写 ########################
#==================================================================================#



###################################################################################
################################### DRF user 关联编写 ###############################
###################################################################################

from django.contrib.auth.models import User
from snippets.serializers import UserModelSerializer


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    # serializer_class = UserModelSerializer
    serializer_class = UserHyperlinkSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    # serializer_class = UserModelSerializer
    serializer_class = UserHyperlinkSerializer




###################################################################################
################################### 根视图 ###############################
###################################################################################

from rest_framework.reverse import reverse

@api_view(['GET'])
def api_root(request, format=None):
    return Response(
        {
            'users': reverse('user-list', request=request, format=format),
            "snippets": reverse('snippet-list', request=request, format=format),
        }
    )
###################################################################################
################################### 根视图 ###############################
###################################################################################

#==================================================================================#
###################################  代码高亮  #######################################
#==================================================================================#


class SnipperHighlight(generics.GenericAPIView):
    queryset = Snippet.objects.all()
    # serializer_class = SnippetModelSerializer
    renderer_classes = (renderers.StaticHTMLRenderer, )  # 为这个类视图指定渲染的类, 把我们内容渲染成html 返回给前端

    def get(self, request, *args, **kwargs):
        snippet = self.get_object()  # GenericAPIView 提供的. 返回视图要渲染的对象. 通过ORM获得 snippet模型的实例对象
        return Response(snippet.highlighted)  # 这个对象可以调用highlighted 高亮文本. 响应的时候会选择,你选择的渲染器渲染

#==================================================================================#
###################################  代码高亮  #######################################
#==================================================================================#


###################################################################################
################################### drf viewset 编写 ###############################
###################################################################################

from rest_framework import viewsets


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserHyperlinkSerializer


class SnippetViewSet(viewsets.ModelViewSet):
    queryset = Snippet.objects.all()
    serializer_class = SnippetHyperlinkSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)

    def perform_create(self, serializer):
        """创建 对象时如何提供用户信息"""
        serializer.save(owner=self.request.user)

    #  detail=True  实现 @detail_route装饰器 让 action 执行
    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])  # 指定渲染器
    def highlight(self, request, *args, **kwargs):  # 自定义高亮方法
        snippet = self.get_object()
        return Response(snippet.highlighted)

    def list(self, request, *args, **kwargs): # 为了查看request对象内容

        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)

        res = Response(serializer.data)
        print(res.data)
        print(res.status_code)
        print(res.template_name)
        print('aaa', res.cookies)
        return res

        # print('request.data------', request.data)
        # print('request.query_params------', request.query_params)
        # print('request.parsers------', request.parsers)
        # print('request.authenticators------', request.authenticators)
        # print('request.user------', request.user)
        # print('request.auth------', request.auth)
        # return super(SnippetViewSet, self).list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):  # 为了查看request对象内容
        print('request.data------', request.data)
        print('request.query_params------', request.query_params)
        print('request.parsers------', request.parsers)
        print('request.authenticators------', request.authenticators)
        print('request.user------', request.user)
        print('request.auth------', request.auth)
        return super(SnippetViewSet, self).create(request, *args, **kwargs)



###################################################################################
################################### drf viewset 编写 ###############################
###################################################################################



#==================================================================================#
###################################  request使用 #######################################
#==================================================================================#


