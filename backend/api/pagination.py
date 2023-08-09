from rest_framework.pagination import PageNumberPagination
from foodgram.settings import PAGE_SIZE

class CustomRecipesPagination(PageNumberPagination):
    page_size = PAGE_SIZE


class CustomUsersPagination(PageNumberPagination):
    page_size_query_param = 'limit'
    page_size = PAGE_SIZE
