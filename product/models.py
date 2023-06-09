from django.db import models

class Product(models.Model):
    id_source = models.CharField(max_length=20)
    type = models.CharField(max_length=50)
    sku = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=150)
    published = models.BooleanField()
    is_featured = models.BooleanField()
    visibility_in_catalog = models.CharField(max_length=50)
    short_description = models.TextField()
    description = models.TextField()
    sale_price_start_date = models.DateField(null=True)
    sale_price_end_date = models.DateField(null=True)
    tax_status = models.CharField(max_length=50)
    tax_class = models.CharField(max_length=50)
    in_stock = models.BooleanField()
    stock = models.IntegerField()
    backorders_allowed = models.BooleanField()
    sold_individually = models.BooleanField()
    weight_lbs = models.SmallIntegerField()
    length_in = models.SmallIntegerField()
    width_in = models.SmallIntegerField()
    height_in = models.SmallIntegerField()
    allow_customer_reviews = models.BooleanField()
    purchase_note = models.CharField(max_length=500)
    sale_price = models.DecimalField(max_digits=10, decimal_places=3, )
    regular_price = models.DecimalField(max_digits=10, decimal_places=3, )
    categories = models.TextField()
    tags = models.TextField()
    shipping_class = models.CharField(max_length=50)
    images = models.TextField()
    download_limit = models.CharField(max_length=100)
    download_expiry_days = models.IntegerField()
    parent = models.CharField(max_length=100)
    grouped_products = models.CharField(max_length=200)
    upsells = models.CharField(max_length=200)
    cross_sells = models.CharField(max_length=200)
    external_url = models.CharField(max_length=500)
    button_text = models.CharField(max_length=50)
    position = models.CharField(max_length=100)
    attribute_1_name = models.CharField(max_length=100)
    attribute_1_values = models.CharField(max_length=200)
    attribute_2_name = models.CharField(max_length=100)
    attribute_2_values = models.CharField(max_length=200)
    attribute_3_name = models.CharField(max_length=100)
    attribute_3_values = models.CharField(max_length=200)
    attribute_4_name = models.CharField(max_length=100)
    attribute_4_values = models.CharField(max_length=200)
    attribute_5_name = models.CharField(max_length=100)
    attribute_5_values = models.CharField(max_length=200)
    meta_wpcom_is_markdown = models.CharField(max_length=500)
    download_1_name = models.CharField(max_length=100)
    download_1_url = models.CharField(max_length=500)
    download_2_name = models.CharField(max_length=100)
    download_2_url = models.CharField(max_length=500)

    @property
    def shopify_sync_data(self):
        try:
            return self.shopifysyncstatus
        except ShopifySyncStatus.DoesNotExist:
            pass
        return None

    class Meta:
        ordering = ["-id"]


class ShopifySyncStatus(models.Model):
    product = models.OneToOneField(Product, on_delete=models.PROTECT)
    last_updated = models.DateTimeField(null=True)
    shopify_product_id = models.CharField(max_length=200)

    class Meta:
        ordering = ['product']
