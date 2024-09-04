from fastapi import FastAPI
from fastapi import Path, Query, HTTPException, status
from schemas.models import *

app = FastAPI()

# Example products list
PRODUCTS = [
    Product(1, 'Widget Pro', 'Widgets', 'A high-quality widget', 29.99),
    Product(2, 'Gadget Max', 'Gadgets', 'A versatile gadget for all your needs', 49.99),
]

# Create a product
@app.post('/products/', status_code=status.HTTP_201_CREATED)
async def create_product(product_request: ProductRequest):
    new_product = Product(**product_request.model_dump())
    PRODUCTS.append(new_product)
    return new_product

# Read all products
@app.get('/products/', status_code=status.HTTP_200_OK)
async def read_all_products():
    return PRODUCTS

# Read a product by ID
@app.get('/products/{product_id}', status_code=status.HTTP_200_OK)
async def read_product(product_id: int = Path(gt=0)):
    for product in PRODUCTS:
        if product.id == product_id:
            return product
    raise HTTPException(status_code=404, detail='Product not found')

# Update a product
@app.put('/products/{product_id}', status_code=status.HTTP_200_OK)
async def update_product(product_id: int, product_request: ProductRequest):
    for i, product in enumerate(PRODUCTS):
        if product.id == product_id:
            updated_product = Product(**product_request.model_dump())
            PRODUCTS[i] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail='Product not found')

# Delete a product
@app.delete('/products/{product_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(product_id: int):
    for i, product in enumerate(PRODUCTS):
        if product.id == product_id:
            PRODUCTS.pop(i)
            return
    raise HTTPException(status_code=404, detail='Product not found')