from typing import Any
from django.core.exceptions import ObjectDoesNotExist
from django.core.management import BaseCommand
from django.core.paginator import Paginator
from rest_framework import status
import requests

from product.constants import (
    DEFAULT_VISIBILITY,
    SHOPIFY_PRODUCT_VALIDS_STATUS,
    PRODUCT_ACTIVE_STATUS,
    PRODUCT_DRAFT_STATUS
)
from catalogueapi.secrets import Config
from product.models import Product, ShopifySyncStatus


class Command(BaseCommand):
    help = "Creacion y syncronizacion de productos en tienda Shopify"


    def create_or_update_product(self, product: Product):
        headers = {
            'Content-Type': 'application/json',
            'X-Shopify-Access-Token': Config.SHOPIFY_ACCESS_TOKEN
        }
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
            if shopify_sync_status:
                print('update product ')
                print('p id ', shopify_sync_status.product.id)
                print('shopify id ', shopify_sync_status.shopify_product_id)
                req = requests.put(
                    f'{Config.SHOPIFY_API_URL_ROOT}products/{shopify_sync_status.shopify_product_id}.json',
                    json=payload,
                    headers=headers,
                    timeout=90
                )
            else:
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
            #TODO improve on bulk_create and params update conflit
            if req.status_code == status.HTTP_201_CREATED:
                print('shopify id')
                print(shopify_product_id)
                print('last updated ')
                print(updated_at)
                print('--------')
                ShopifySyncStatus.objects.create(
                    product=product,
                    last_updated=updated_at,
                    shopify_product_id=shopify_product_id
                )
            elif req.status_code == status.HTTP_200_OK:
                shopify_sync_status.last_updated = updated_at
                shopify_sync_status.save()
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

    def handle(self, *args: Any, **options: Any) -> str | None:
        products_qs = Product.objects.all().order_by('-id')[:3]
        paginator = Paginator(products_qs, 100)
        for page_number in paginator.page_range:
            page = paginator.page(page_number)
            for product in page.object_list:
                self.create_or_update_product(product)
