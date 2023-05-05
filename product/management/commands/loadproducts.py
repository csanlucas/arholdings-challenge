from typing import Any
from django.core.management.base import CommandParser
import pandas as pd
import numpy as np
from django.core.management import BaseCommand
from django.utils import timezone

from product.constants import REQUIRED_PRODUCTS_CSV_COLUMNS, MAX_BATCH_INSERT_PRODUCTS_ITEM, NUMERIC_COLUMNS_CSV
from product.models import Product


class Command(BaseCommand):
    help = "Subida de lista de productos desde archivo CSV"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("file_path", type=str)
    
    def handle(self, *args: Any, **options: Any) -> str | None:
        init_time = timezone.now()
        product_df = pd.read_csv(options["file_path"])
        product_df.columns = product_df.columns.str.lower()
        if ( set(REQUIRED_PRODUCTS_CSV_COLUMNS) != set(list(product_df.columns)) ):
            raise ValueError("Error!! Columnas deben ser las requeridas, revisar archivo csv")
        product_df.drop_duplicates(subset='sku', inplace=True)
        for col in NUMERIC_COLUMNS_CSV:
            product_df[col].fillna(0, inplace=True)
        product_df.fillna('', inplace=True)
        products_bulk = []
        for index, item in product_df.iterrows():
            sale_price_start_date = item['date sale price starts'] if item['date sale price starts'] else None
            sale_price_end_date = item['date sale price ends'] if item['date sale price ends'] else None
            try:
                products_bulk.append(Product(
                    id_source = item['id'],
                    type = item['type'],
                    sku = item['sku'],
                    name = item['name'],
                    published = item['published'],
                    is_featured = item['is featured?'],
                    visibility_in_catalog = item['visibility in catalog'],
                    short_description = item['short description'],
                    description = item['description'],
                    sale_price_start_date = sale_price_start_date,
                    sale_price_end_date = sale_price_end_date,
                    tax_status = item['tax status'],
                    tax_class = item['tax class'],
                    in_stock = item['in stock?'],
                    stock = item['stock'],
                    backorders_allowed = item['backorders allowed?'],
                    sold_individually = item['sold individually?'],
                    weight_lbs = item['weight (lbs)'],
                    length_in = item['length (in)'],
                    width_in = item['width (in)'],
                    height_in = item['height (in)'],
                    allow_customer_reviews = item['allow customer reviews?'],
                    purchase_note = item['purchase note'],
                    sale_price = item['sale price'],
                    regular_price = item['regular price'],
                    categories = item['categories'],
                    tags = item['tags'],
                    shipping_class = item['shipping class'],
                    images = item['images'],
                    download_limit = item['download limit'],
                    download_expiry_days = item['download expiry days'],
                    parent = item['parent'],
                    grouped_products = item['grouped products'],
                    upsells = item['upsells'],
                    cross_sells = item['cross-sells'],
                    external_url = item['external url'],
                    button_text = item['button text'],
                    position = item['position'],
                    attribute_1_name = item['attribute 1 name'],
                    attribute_1_values = item['attribute 1 value(s)'],
                    attribute_2_name = item['attribute 2 name'],
                    attribute_2_values = item['attribute 2 value(s)'],
                    attribute_3_name = item['attribute 3 name'],
                    attribute_3_values = item['attribute 3 value(s)'],
                    attribute_4_name = item['attribute 4 name'],
                    attribute_4_values = item['attribute 4 value(s)'],
                    attribute_5_name = item['attribute 5 name'],
                    attribute_5_values = item['attribute 5 value(s)'],
                    meta_wpcom_is_markdown = item['meta: _wpcom_is_markdown'],
                    download_1_name = item['download 1 name'],
                    download_1_url = item['download 1 url'],
                    download_2_name = item['download 2 name'],
                    download_2_url = item['download 2 url']
                ))
            except KeyError as e:
                print('Keyerror! Product cannot be inserted on database', e)
            if len(products_bulk) > MAX_BATCH_INSERT_PRODUCTS_ITEM:
                Product.objects.bulk_create(
                    products_bulk, update_conflicts=True,
                    update_fields=['name', 'published', 'in_stock', 'stock', 'sale_price']
                )
                products_bulk = []
        if products_bulk:
            Product.objects.bulk_create(
                products_bulk, update_conflicts=True,
                update_fields=['name', 'published', 'in_stock', 'stock', 'sale_price']
            )
        finish_time = timezone.now()
        self.stdout.write(self.style.SUCCESS(
            f"Almacenamiento de productos tuvo una duracion de: {(finish_time-init_time).total_seconds()} segundos"))
