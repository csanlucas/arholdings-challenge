from rest_framework import serializers

from product.models import Product, ShopifySyncStatus


class ShopifySyncStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShopifySyncStatus
        fields = ("last_updated", "shopify_product_id")

class ProductSerializer(serializers.ModelSerializer):
    shopify_sync_data = ShopifySyncStatusSerializer(many=False, read_only=True)
    class Meta:
        model = Product
        fields = "__all__"
