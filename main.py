from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Modelo do Produto
class Product(BaseModel):
    name: str
    price: float

# Banco de dados em memória
products = []
next_id = 1

# CREATE
@app.post("/api/products")
def create_product(product: Product):
    global next_id
    new_product = {
        "id": next_id,
        "name": product.name,
        "price": product.price
    }
    next_id += 1
    products.append(new_product)
    return new_product


# READ ALL
@app.get("/api/products")
def get_all_products():
    return products


# READ ONE
@app.get("/api/products/{product_id}")
def get_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Produto não encontrado")


# UPDATE
@app.put("/api/products/{product_id}")
def update_product(product_id: int, updated: Product):
    for p in products:
        if p["id"] == product_id:
            p["name"] = updated.name
            p["price"] = updated.price
            return p
    raise HTTPException(status_code=404, detail="Produto não encontrado")


# DELETE
@app.delete("/api/products/{product_id}")
def delete_product(product_id: int):
    for p in products:
        if p["id"] == product_id:
            products.remove(p)
            return {"message": "Produto removido"}
    raise HTTPException(status_code=404, detail="Produto não encontrado")
