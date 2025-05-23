from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultSetPagination(PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):
        current_page = self.page.number
        next_page = self.page.next_page_number() if self.page.has_next() else None
        previous_page = self.page.previous_page_number() if self.page.has_previous() else None

        return Response({
            'count' : self.page.paginator.count,
            'current_page' : current_page,
            'next_page' : next_page,
            'previous_page' : previous_page,
            'result' : data 
        })