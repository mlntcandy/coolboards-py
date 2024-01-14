from collections import OrderedDict
from rest_framework import viewsets

from .serializers import ItemSerializer, ReviewSerializer
from coolboards.models import Item, Review
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import filters
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from django.db.models import Q


class MyPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("count", self.page.paginator.count),
                    (
                        "links",
                        {
                            "next": self.get_next_link(),
                            "previous": self.get_previous_link(),
                        },
                    ),
                    ("data", data),
                ]
            )
        )


class ItemViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows items to be viewed or edited.
    """

    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    pagination_class = MyPagination
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    ordering_fields = ["price", "created_at"]

    @action(detail=True, methods=["post"])
    def disable_discount(self, request, pk=None):
        """
        Disable discount for a specific item
        """
        if not request.user.is_authenticated:
            return Response({"status": "not authenticated"})
        item = self.get_object()
        if item.discount == 0:
            return Response({"status": "no discount"})
        item.price = item.discount
        item.discount = 0
        item.save()
        return Response({"status": "ok"})

    @action(detail=False, methods=["get"])
    def top(self, request):
        """
        Get top items by price
        """
        top_items = Item.objects.order_by("-price")
        page = self.paginate_queryset(top_items)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(top_items, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def reviews(self, request, pk=None):
        """
        Get reviews for a specific item
        """
        item = self.get_object()
        reviews = item.review_set.all()
        page = self.paginate_queryset(reviews)
        if page is not None:
            serializer = ReviewSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = ReviewSerializer(reviews, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def deals(self, request):
        """
        Get items with discount or new items
        """
        deals = Item.objects.filter(Q(new=True) | ~Q(discount=0) & ~Q(stock=0))
        page = self.paginate_queryset(deals)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(deals, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reviews to be viewed or edited.
    """

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]

    def get_queryset(self):
        item = self.request.query_params.get("item", None)
        queryset = Review.objects.all()
        if item is not None:
            queryset = Review.objects.filter(item=item)
        return queryset

    @action(detail=False, methods=["get"])
    def invalid(self, request):
        """
        Get invalid reviews
        """
        invalid = Review.objects.filter(
            ~(Q(rating__gte=1) & Q(rating__lte=5)) | Q(text="")
        )
        page = self.paginate_queryset(invalid)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(invalid, many=True)
        return Response(serializer.data)
