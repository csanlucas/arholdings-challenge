REQUIRED_PRODUCTS_CSV_COLUMNS = ['id', 'type', 'sku', 'name', 'published', 'is featured?','visibility in catalog', 
                                 'short description', 'description', 'date sale price starts', 'date sale price ends', 
                                 'tax status', 'tax class', 'in stock?', 'stock', 'backorders allowed?', 'sold individually?',
                                 'weight (lbs)', 'length (in)', 'width (in)', 'height (in)', 'allow customer reviews?',
                                 'purchase note', 'sale price', 'regular price', 'categories', 'tags', 'shipping class',
                                 'images', 'download limit', 'download expiry days', 'parent', 'grouped products',
                                 'upsells', 'cross-sells', 'external url', 'button text', 'position', 'attribute 1 name',
                                 'attribute 1 value(s)', 'attribute 2 name', 'attribute 2 value(s)', 'attribute 3 name',
                                 'attribute 3 value(s)', 'attribute 4 name', 'attribute 4 value(s)', 'attribute 5 name',
                                 'attribute 5 value(s)', 'meta: _wpcom_is_markdown', 'download 1 name', 'download 1 url',
                                 'download 2 name', 'download 2 url']

NUMERIC_COLUMNS_CSV = ['published', 'is featured?', 'in stock?', 'stock', 'backorders allowed?', 'sold individually?',
                       'weight (lbs)', 'length (in)', 'width (in)', 'height (in)', 'allow customer reviews?',
                       'sale price', 'regular price', 'download expiry days']

MAX_BATCH_INSERT_PRODUCTS_ITEM = 500

PRODUCT_ACTIVE_STATUS = 'active'
PRODUCT_DRAFT_STATUS = 'draft'
PRODUCT_ARCHIVED_STATUS = 'archived'
SHOPIFY_PRODUCT_VALIDS_STATUS = [
    PRODUCT_ACTIVE_STATUS,
    PRODUCT_ARCHIVED_STATUS,
    PRODUCT_DRAFT_STATUS
]

DEFAULT_VISIBILITY = 'visible'
