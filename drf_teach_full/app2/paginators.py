from rest_framework import pagination


class MyPagination1(pagination.PageNumberPagination):
    page_size = 2           # 每页显示的默认对象的个数
    page_query_param = 'page'     #页号，第几页的参数
    page_size_query_param = 'page_size'  # 自己指定每页显示多少个对象
    max_page_size = 4           #最大允许设置的每页显示的数量


class MyPagination2(pagination.PageNumberPagination):
    page_size = 3          # 每页显示的默认对象的个数
    page_query_param = 'pg'     #页号，第几页的参数
    page_size_query_param = 'ps'  # 自己指定每页显示多少个对象
    max_page_size = 100          #最大允许设置的每页显示的数量


class MyPagination3(pagination.LimitOffsetPagination):
    default_limit = 2
    limit_query_param = 'lm'
    offset_query_param = 'of'
    max_limit = 4

