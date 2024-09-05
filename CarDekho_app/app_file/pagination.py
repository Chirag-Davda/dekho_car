from rest_framework .pagination import PageNumberPagination,LimitOffsetPagination,CursorPagination

class Reviewlistpagiation(PageNumberPagination):
    page_size = 1
    page_query_param = 'page'
    page_size_query_param = 'page_size'
    max_page_size = 100
    last_page_strings = 'end'
    
class ReviewListlimitoffpag(LimitOffsetPagination):
    default_limit = 2
    # max_limit = 3
    # limit_query_param = 'limit'
    # offset_query_param = 'start'
    
class ReviewListcursorpag(CursorPagination):
    page_size = 2
    ordering = 'rating'