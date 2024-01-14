from collections import OrderedDict
from rest_framework import viewsets

from .serializers import ItemSerializer, ReviewSerializer
from coolboards.models import Item, Review
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


class ItemPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    ("nextPage", self.get_next_link()),
                    ("previousPage", self.get_previous_link()),
                    ("data", data),
                ]
            )
        )


class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = ItemPagination
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "created_at"]

    @action(detail=True, methods=["post"])
    def disable_discount(self, request, pk=None):
        item = self.get_object()
        if item.discount == 0:
            return Response({"status": "no discount"})
        item.price = item.discount
        item.discount = 0
        item.save()
        return Response({"status": "ok"})

    @action(detail=False, methods=["get"])
    def top(self, request):
        top_items = Item.objects.order_by("-price")
        page = self.paginate_queryset(top_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(top_items, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
