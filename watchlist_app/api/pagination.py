"""
all this pagination classes either works with 'generic views' or 'view sts'
"""
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class WatchListPagination(PageNumberPagination):
    page_size = 3
    page_query_param = 'p'
    page_size_query_param = 'size'
    max_page_size = 10
    last_page_number = "end"


class WatchListLOPagination(LimitOffsetPagination):
    """
    You can change the limit and offset in the url unless other restrictions parameters exists
    """
    default_limit = 5
    max_limit = 10
    limit_query_param = 'limit'
    offset_query_param = 'start'


class WatchListCPagination(CursorPagination):
    page_size = 5
    ordering = 'created'
    cursor_query_param = 'record'
