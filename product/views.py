from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, viewsets
from rest_framework.filters import SearchFilter

from catalogueapi.utils.pagination import StandardResultsSetPagination
from product.models import Product
from product.serializers import ProductSerializer

class ProductViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_fields = ("sku",)
    search_fields = ("name", "sku", "id_source",)
