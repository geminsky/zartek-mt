import math

from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

WING_PAGE = 3


class ServerSidePagination(PageNumberPagination):
    filter_data = None

    def paginate_queryset(self, queryset, request, view=None):
        """Checking NotFound exception"""
        if 'no_page' in request.query_params:
            return None
        try:
            return super(ServerSidePagination, self).paginate_queryset(queryset, request, view=view)
        except NotFound:  # intercept NotFound exception
            return list()

    def get_paginated_response(self, data):
        """ custom pagination"""

        if hasattr(self, 'page') and self.page is not None:
            return Response(
                {
                    "content": data,
                    'filter': self.filter_data,
                    "pageable": {
                        "sort": {
                            "sorted": False,
                            "unsorted": False
                        },
                        "pageSize": self.page_size,
                        "pageNumber": self.page.number,
                        "offset": 0,
                        "unpaged": False,
                        "paged": True
                    },
                    "last": self.get_last(),
                    "totalElements": self.page.paginator.count,
                    "totalPages": self.get_total_page(),
                    "first": self.get_first(),
                    "sort": {
                        "sorted": False,
                        "unsorted": True
                    },
                    "numberOfElements": self.get_number_of_elements(),
                    "size": self.page_size,
                    "number": self.page.number,
                    "page_number_range": self.get_page_number_range()
                })
        else:
            return Response({'error': 'no data'})

    def get_total_page(self):
        """ total number of pages"""
        return math.ceil(int(self.page.paginator.count) / self.page_size)

    def get_number_of_elements(self):
        """ calculate the range of pagination
            example 1-10
        """
        if self.page.paginator.count < int(self.page.number) * self.page_size:
            show = self.get_shows()

            return "{} - {}".format(show, self.page.paginator.count)
        else:
            show = self.get_shows()
            return "{} - {}".format(show, self.get_page_range())

    def get_last(self):
        """check last page"""
        if self.page.number == self.get_total_page():
            return True
        else:
            return False

    def get_first(self):
        """check first page"""
        if self.page.number == 1:
            return True
        else:
            return False

    def get_shows(self):
        """clauculate starting index"""
        start = self.page.number * self.page_size - self.page_size + 1
        return start

    def get_page_range(self):
        """clauculate ending index"""
        return self.page.number * self.page_size

    def get_page_number_range(self):
        """ limited page number """
        index = self.page.number
        max_index = self.page.paginator.num_pages
        start_index = index - WING_PAGE if index >= WING_PAGE else 1
        end_index = index + WING_PAGE if index <= max_index - WING_PAGE else max_index
        page_range = [page for page in range(start_index, end_index + 1)]
        return page_range[1:len(page_range)] if index == WING_PAGE else page_range
