from typing import Any, List
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from django.core.paginator import Paginator
from django.utils import timezone
from rest_framework import status
import requests
import time

from product.constants import (
    ADMIN_RATE_LIMIT_NUMBER_REQ_BY_MINUTE,
    ADMIN_RATE_LIMIT_NUMBER_REQ_BY_SECOND,
    DEFAULT_VISIBILITY,
    SHOPIFY_PRODUCT_VALIDS_STATUS,
    PRODUCT_ACTIVE_STATUS,
    PRODUCT_DRAFT_STATUS
)
from catalogueapi.secrets import Config
from product.models import Product, ShopifySyncStatus


class Command(BaseCommand):
    help = "Creacion y syncronizacion de productos en tienda Shopify"


    def create_or_update_products(self, products: List[Product]):
        headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': Config.SHOPIFY_ACCESS_TOKEN
        }
        sync_products_bulk = []
        index = 1
        for product in products:
            p_status = ''
            if product.visibility_in_catalog in SHOPIFY_PRODUCT_VALIDS_STATUS:
                p_status = product.visibility_in_catalog
            elif product.visibility_in_catalog == DEFAULT_VISIBILITY:
                p_status = PRODUCT_ACTIVE_STATUS
            else:
                p_status = PRODUCT_DRAFT_STATUS
            payload = {
                'product': {
                    'title': product.name,
                    'body_html': product.description,
                    'vendor': 'csanlucas',
                    'product_type': product.type,
                    'status': p_status,
                    'images': [{'src': i} for i in product.images.split(',')],
                    'variants': [
                        {
                            'price': str(product.sale_price).replace('.', ','),
                            'sku': product.sku,
                            'taxable': 'true' if product.tax_status else 'false',
                            'wheight': product.weight_lbs,
                            'wheight_unit': 'lbs',
                            'inventory_quantity': product.stock
                        }
                    ]
                }
            }
            try:
                shopify_sync_status = ShopifySyncStatus.objects.get(product = product)
            except ObjectDoesNotExist:
                shopify_sync_status = None
            try:
                if index % ADMIN_RATE_LIMIT_NUMBER_REQ_BY_SECOND == 0:
                    print('Admin Api at a rate of 2 requests per second, sleeping 0.5 second....')
                    time.sleep(0.5)
                if shopify_sync_status:
                    print('updating product ', shopify_sync_status.shopify_product_id)
                    req = requests.put(
                        f'{Config.SHOPIFY_API_URL_ROOT}products/{shopify_sync_status.shopify_product_id}.json',
                        json=payload,
                        headers=headers,
                        timeout=90
                    )
                else:
                    print('creating new product...')
                    req = requests.post(
                        f'{Config.SHOPIFY_API_URL_ROOT}products.json', 
                        json=payload ,
                        headers=headers,
                        timeout=90
                    )
                req.raise_for_status()
                product_response = req.json()['product']
                updated_at = product_response['updated_at']
                shopify_product_id = product_response['id']
                sync_products_bulk.append(
                    ShopifySyncStatus(product=product, last_updated=updated_at, shopify_product_id=shopify_product_id)
                )
                if len(sync_products_bulk) > ADMIN_RATE_LIMIT_NUMBER_REQ_BY_MINUTE:
                    ShopifySyncStatus.objects.bulk_create(
                        sync_products_bulk, update_conflicts=True,
                        update_fields=['last_updated']
                    )
                    sync_products_bulk =[]
                    print('Admin Api at a rate of 40 requests per minute, sleeping 1 minute ....')
                    time.sleep(65)
            except KeyError as ke:
                print('Key error at product response  ', ke)
            except requests.exceptions.HTTPError as errh:
                print ("Http Error:",errh)
            except requests.exceptions.ConnectionError as errc:
                print ("Error Connecting:",errc)
            except requests.exceptions.Timeout as errt:
                print ("Timeout Error:",errt)
            except requests.exceptions.RequestException as err:
                print ("Undefined error ",err)
            index += 1
        if sync_products_bulk:
            ShopifySyncStatus.objects.bulk_create(
                sync_products_bulk, update_conflicts=True,
                update_fields=['last_updated']
            )

    def handle(self, *args: Any, **options: Any) -> str | None:
        init_time = timezone.now()
        products_qs = Product.objects.all()[:150]
        paginator = Paginator(products_qs, 100)
        for page_number in paginator.page_range:
            page = paginator.page(page_number)
            self.create_or_update_products(page.object_list)
        finish_time = timezone.now()
        self.stdout.write(self.style.SUCCESS(
            f"Sync de productos en Shopify Store tuvo una duracion de: {(finish_time-init_time).total_seconds()} segundos"))
