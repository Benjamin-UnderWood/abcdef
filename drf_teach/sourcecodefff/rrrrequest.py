# import io
# import sys
# from contextlib import contextmanager
#
# from django.conf import settings
# from django.http import HttpRequest, QueryDict
# from django.http.multipartparser import parse_header
# from django.http.request import RawPostDataException
# from django.utils.datastructures import MultiValueDict
#
# from rest_framework import HTTP_HEADER_ENCODING, exceptions
# from rest_framework.settings import api_settings
#
#
# def is_form_media_type(media_type):
#     """
#     Return True if the media type is a valid form media type.
#     """
#     base_media_type, params = parse_header(media_type.encode(HTTP_HEADER_ENCODING))
#     return (base_media_type == 'application/x-www-form-urlencoded' or
#             base_media_type == 'multipart/form-data')
#
#
# class Empty:
#     """
#     未设置属性的占位符。
#     不能使用`None`，因为那可能是一个有效的值。
#     """
#     pass
#
#
# class ForcedAuthentication:
#     """
#     This authentication class is used if the test client or request factory
#     forcibly authenticated the request.
#     如果测试客户端或请求工厂对请求进行强行认证，则使用该认证类。
#     """
#
#     def __init__(self, force_user, force_token):
#         self.force_user = force_user
#         self.force_token = force_token
#
#     def authenticate(self, request):
#         return (self.force_user, self.force_token)
#
#
# class Request:
#     """
#     Wrapper allowing to enhance a standard `HttpRequest` instance.
#
#     Kwargs:
#         - request(HttpRequest). The original request instance.
#         - parsers(list/tuple). The parsers to use for parsing the
#           request content.
#         - authenticators(list/tuple). The authenticators used to try
#           authenticating the request's user.
#     """
#
#     def __init__(self, request, parsers=None, authenticators=None,
#                  negotiator=None, parser_context=None):
#
#         # 判断请求 是不是django HttpRequest类型
#         assert isinstance(request, HttpRequest), (
#             'The `request` argument must be an instance of '
#             '`django.http.HttpRequest`, not `{}.{}`.'
#             .format(request.__class__.__module__, request.__class__.__name__)
#         )
#
#         self._request = request  # 备份原生django request
#         self.parsers = parsers or ()  # 是否有解析器
#         self.authenticators = authenticators or ()  # 认证器
#         self.negotiator = negotiator or self._default_negotiator()  # 协商器
#         self.parser_context = parser_context  # 解析器上下文
#
#         # 设置如下变量, 在很多时候None是非法的值.
#         self._data = Empty
#         self._files = Empty
#         self._full_data = Empty
#         self._content_type = Empty
#         self._stream = Empty
#
#         if self.parser_context is None:  # 解析器上下文判定
#             self.parser_context = {}
#         self.parser_context['request'] = self
#         self.parser_context['encoding'] = request.encoding or settings.DEFAULT_CHARSET
#
#         # 用户和token 的判定
#         force_user = getattr(request, '_force_auth_user', None)
#         force_token = getattr(request, '_force_auth_token', None)
#         if force_user is not None or force_token is not None:
#             forced_auth = ForcedAuthentication(force_user, force_token)
#             self.authenticators = (forced_auth,)
#
#     def _default_negotiator(self):
#         return api_settings.DEFAULT_CONTENT_NEGOTIATION_CLASS()
#
#     @property
#     def content_type(self):
#         meta = self._request.META
#         return meta.get('CONTENT_TYPE', meta.get('HTTP_CONTENT_TYPE', ''))
#
#     @property
#     def stream(self):
#         """
#         Returns an object that may be used to stream the request content.
#         """
#         if not _hasattr(self, '_stream'):
#             self._load_stream()
#         return self._stream
#
#     @property
#     def query_params(self):  # 查询参数, 返回 原生request 的GET
#         """
#         More semantically correct name for request.GET.
#         """
#         return self._request.GET
#
#     @property
#     def data(self):             #
#         if not _hasattr(self, '_full_data'):  # 如果当前request里没有这个属性
#             self._load_data_and_files()  # 我就去加载数据和文件
#         return self._full_data          #如果有直接返回
#
#     @property
#     def user(self):  # 属性方法
#         """
#         Returns the user associated with the current request, as authenticated
#         by the authentication classes provided to the request.
#         """
#         if not hasattr(self, '_user'):
#             with wrap_attributeerrors():
#                 self._authenticate()
#         return self._user
#
#     @user.setter
#     def user(self, value):
#         """
#         Sets the user on the current request. This is necessary to maintain
#         compatibility with django.contrib.auth where the user property is
#         set in the login and logout functions.
#
#         Note that we also set the user on Django's underlying `HttpRequest`
#         instance, ensuring that it is available to any middleware in the stack.
#         """
#         self._user = value
#         self._request.user = value
#
#     @property
#     def auth(self):
#         """
#         Returns any non-user authentication information associated with the
#         request, such as an authentication token.
#         """
#         if not hasattr(self, '_auth'):
#             with wrap_attributeerrors():
#                 self._authenticate()
#         return self._auth
#
#     @auth.setter
#     def auth(self, value):
#         """
#         Sets any non-user authentication information associated with the
#         request, such as an authentication token.
#         """
#         self._auth = value
#         self._request.auth = value
#
#
#     def _load_data_and_files(self):  # 把原生的request 数据转填到现在的request 中
#         """
#         Parses the request content into `self.data`.
#         """
#         if not _hasattr(self, '_data'):
#             self._data, self._files = self._parse()
#             if self._files:
#                 self._full_data = self._data.copy()
#                 self._full_data.update(self._files)
#             else:
#                 self._full_data = self._data
#
#             # if a form media type, copy data & files refs to the underlying
#             # http request so that closable objects are handled appropriately.
#             if is_form_media_type(self.content_type):
#                 self._request._post = self.POST
#                 self._request._files = self.FILES
#
#     def _parse(self):
#         """
#         Parse the request content, returning a two-tuple of (data, files)
#
#         May raise an `UnsupportedMediaType`, or `ParseError` exception.
#         """
#         media_type = self.content_type
#         try:
#             stream = self.stream
#         except RawPostDataException:
#             if not hasattr(self._request, '_post'):
#                 raise
#             # If request.POST has been accessed in middleware, and a method='POST'
#             # request was made with 'multipart/form-data', then the request stream
#             # will already have been exhausted.
#             if self._supports_form_parsing():
#                 return (self._request.POST, self._request.FILES)
#             stream = None
#
#         if stream is None or media_type is None:
#             if media_type and is_form_media_type(media_type):
#                 empty_data = QueryDict('', encoding=self._request._encoding)
#             else:
#                 empty_data = {}
#             empty_files = MultiValueDict()
#             return (empty_data, empty_files)
#
#         parser = self.negotiator.select_parser(self, self.parsers)
#
#         if not parser:
#             raise exceptions.UnsupportedMediaType(media_type)
#
#         try:
#             parsed = parser.parse(stream, media_type, self.parser_context)
#         except Exception:
#             # If we get an exception during parsing, fill in empty data and
#             # re-raise.  Ensures we don't simply repeat the error when
#             # attempting to render the browsable renderer response, or when
#             # logging the request or similar.
#             self._data = QueryDict('', encoding=self._request._encoding)
#             self._files = MultiValueDict()
#             self._full_data = self._data
#             raise
#
#         # Parser classes may return the raw data, or a
#         # DataAndFiles object.  Unpack the result as required.
#         try:
#             return (parsed.data, parsed.files)
#         except AttributeError:
#             empty_files = MultiValueDict()
#             return (parsed, empty_files)