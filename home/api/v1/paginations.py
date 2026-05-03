from rest_framework.pagination import PageNumberPagination


class ObjectivePagination(PageNumberPagination):
    page_size = 3
    max_page_size = 30
    page_query_param = "objective_page"
