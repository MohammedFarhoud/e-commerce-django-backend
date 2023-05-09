from rest_framework.pagination import PageNumberPagination



class ProductPagination(PageNumberPagination):
    page_size = 2
    page_size_query_param = 'size'
    max_page_size = 100
    
    