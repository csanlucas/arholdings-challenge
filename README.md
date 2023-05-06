# arholdings-challenge

## Objetivo
Se está evaluando la posibilidad de implementar Shopify como plataforma de E-Commerce en la organización, por lo que se desea automatizar ciertos procesos para poder lograr esta implementación.

---

## Requisitos:

### **1. Migración catálogos de artículos, a una Base de datos local.**
Se tiene en un archivo separado por comas (sample_data.csv) con el catálogo de artículos que se desea publicar en Shopify, pero se
desea crear un portal web con acceso a esa información. Por lo tanto, lo primero que se requiere hacer es migrar dicha información a
una base de datos

### **2. Publicación de artículos a Shopify.**
Una vez cargados los artículos en la base de datos local, se desea migrar los mismos a una tienda en Shopify a 
través de API. Cabe destacar que se desea saber en la base de datos la última fecha de sincronización de los artículos.

### **3. Interfaz gráfica.**
Se desea crear una interfaz gráfica en el cual se consulte por SKU un artículo y muestre la información de este basado en el Wireframe entregado por el team de UI/UX:

---

## **Setup for development**

Este proyecto se encuentra configurado con Docker y docker-compose, con la finalidad de agilizar un deployment LOCAL para mantener un entorno de desarrollo independiente. Es necesario **verificar** previamente una instalación de Docker

**1)** Clonar repositorio
```sh
git clone https://github.com/csanlucas/arholdings-challenge.git
```
**2)** Ingresar a la carpeta del proyecto y ejecutar docker-compose up, este comando realizará la configuración de las imágenes de Docker para backend y para la DB
```sh
cd arholdings-challenge
cp .env.example .env
cp .mysqlenv.example .mysqlenv
docker-compose up --build
```
**3)** Aplicar migrations para Django
```sh
docker-compose exec backend bash
python manage.py migrate
exit
```

**4)** Copiar archivo de datos de productos
```sh
Se debe copiar archivo [sample_data].csv a la raiz del proyecto ./arholdings-challenge/
```
---

## Solución planteada y uso
Se realiza el desarrollo de un REST Api haciendo uso del siguiente stack de tecnologías:

    - Python 3.10+
    - Django 4.2.1
    - Django-Rest-Framework 3.14.0

Manejo de entornos de desarrollo para agilizar el cambio de variables de accesso y settings de DRF dependiendo el entorno al que
se hará deployment

    - LOCAL
    - PROD

Gestión de archivos de secrets, como variables de entorno, idealmente sus valores no se hacen tracking en git pero en esta situación
para facilitar la ejecución del proyecto se hace tracking de *.example

### **SUPUESTOS**
    - Se realiza implementación de commandos customs soportados por Django-admin para realizar las funcionalidades de 
    almacenamiento de catálogo de productos en base de datos y sincronización con Shopify API
    [En requisito 1] 
    - Se debe cumplir con exactamente el mismo número y labels de columnas del archivo entregado *sample_data.csv*, caso contrario
    se devolverá un error de operación sobre el archivo.
    - En caso de registros con valores vacíos, para las columnas que representan un dato númerico o boolean se establece con 0, para las demás columnas con caracter vacío.
    - Se contempla que parámetro SKU sea único, en caso de existir ese registro en base de datos local se actualizarán ciertas columnas
    [En requisito 2] 
    - Se toma a consideración los rate limits por defecto al momento de usar el API Admin para crear Productos en shopify
    - En caso de registrarse un producto previamente creado en Shopify se procederá a actualizar los parámetros en la tienda.

### **USO**
Se debe realizar los request a los endpoints haciendo uso de algún cliente de HTTP, se recomienda utilizar *Postman*
Se debe acceder a la consola para ejecutar los comandos a las soluciones de los *Requisitos 1 y 2*

### REQUISITO 1
```sh
docker-compose exec backend bash
python manage.py loadproducts sample_data.csv
exit
```

### REQUISITO 2
```sh
docker-compose exec backend bash
python manage.py shopifysync
exit
```
---

### REQUISITO 3
Para obtener la data de los productos se realiza la exposición de un servicio mediante REST Api, que mantiene los siguientes
endpoints

#### Filtrar producto mediante SKU
* **URL** : http://localhost:8101/products/
* **Method** `GET`
* **URL Params:**

  **Required**
  `sku=[sku_value]`

* **Success Response:**
    * **Code** 200 <br/>
    **Content** 
    ```json
    {
        "count": 1,
        "next": null,
        "previous": null,
        "results": [
            {
                "id": 2036,
                "id_source": "2042",
                "type": "simple",
                "sku": "24-WB03",
                "name": "Driven Backpack",
                "published": true,
                "is_featured": false,
                "visibility_in_catalog": "visible",
                "short_description": "This is a simple product called Driven Backpack",
                ...
            }
        ]
    }

* **Success Response:** En caso de no existir el producto por el SKU filtrado, se tiene el siguiente response
    * **Code** 200 <br/>
    **Content** 
    ```json
    {
        "count": 0,
        "next": null,
        "previous": null,
        "results": []
    }

---

#### Listar productos en base de datos local [Requisito Extra]
* **URL** : http://localhost:8101/products/
* **Method** `GET`
* **Success Response:**
    * **Code** 200 <br/>
    **Content** 
    ```json
    {
    "count": 2038,
    "next": "http://localhost:8101/products/?page=2",
    "previous": null,
    "results": [
        {
            "id": 2038,
            "id_source": "2044",
            "type": "simple",
            "sku": "24-WB04",
            "name": "Push It Messenger Bag",
            "published": true,
            "is_featured": false,
            "visibility_in_catalog": "visible",
            ...
        },
        ...
    ]
    ```
---

#### Buscar producto mediante propiedades name, sku, id_source(catalogo)
* **URL** : http://localhost:8101/products/
* **Method** `GET`
* **URL Params:**

  **Required**
  `search=[value]`

* **Success Response:**
    * **Code** 200 <br/>
    **Content** 
    ```json
    {
        "count": 208,
        "next": "http://localhost:8101/products/?page=2&search=mh",
        "previous": null,
        "results": [
            {
                "id": 2036,
                "id_source": "2042",
                "type": "simple",
                "sku": "24-WB03",
                "name": "Driven Backpack",
                "published": true,
                "is_featured": false,
                "visibility_in_catalog": "visible",
                "short_description": "This is a simple product called Driven Backpack",
                ...
            },
            ...
        ]
    }
