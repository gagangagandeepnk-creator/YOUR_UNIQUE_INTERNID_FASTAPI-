from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Initial product list (do not modify manually)
products = [
    {"id": 1, "name": "Wireless Mouse", "price": 599, "category": "Electronics", "in_stock": True},
    {"id": 2, "name": "USB Hub", "price": 799, "category": "Electronics", "in_stock": True},
    {"id": 3, "name": "Notebook", "price": 99, "category": "Stationery", "in_stock": True},
    {"id": 4, "name": "Pen Set", "price": 49, "category": "Stationery", "in_stock": False}
]

class Product(BaseModel):
    name: str
    price: int
    category: str
    in_stock: bool


@app.get("/products")
def get_products():
    return {
        "total": len(products),
        "products": products
    }


@app.post("/products")
def add_product(product: Product):

    for p in products:
        if p["name"].lower() == product.name.lower():
            raise HTTPException(status_code=400, detail="Product already exists")

    new_id = max(p["id"] for p in products) + 1

    new_product = {
        "id": new_id,
        "name": product.name,
        "price": product.price,
        "category": product.category,
        "in_stock": product.in_stock
    }

    products.append(new_product)

    return {
        "message": "Product added",
        "product": new_product
    }

@app.put("/products/{product_id}")
def update_product(product_id: int, in_stock: bool = None, price: int = None):

    for product in products:
        if product["id"] == product_id:

            if in_stock is not None:
                product["in_stock"] = in_stock

            if price is not None:
                product["price"] = price

            return {
                "message": "Product updated",
                "product": product
            }

    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
def delete_product(product_id: int):

    for product in products:
        if product["id"] == product_id:
            products.remove(product)
            return {
                "message": f"Product '{product['name']}' deleted"
            }

    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/products/{product_id}")
@app.get("/products/audit")
def products_audit():
    total_products = len(products)

    in_stock_count = 0
    out_of_stock_names = []
    total_stock_value = 0
    most_expensive = None

    for product in products:
        if product["in_stock"]:
            in_stock_count += 1
            total_stock_value += product["price"] * 10
        else:
            out_of_stock_names.append(product["name"])

        if most_expensive is None or product["price"] > most_expensive["price"]:
            most_expensive = product

    return {
        "total_products": total_products,
        "in_stock_count": in_stock_count,
        "out_of_stock_names": out_of_stock_names,
        "total_stock_value": total_stock_value,
        "most_expensive": {
            "name": most_expensive["name"],
            "price": most_expensive["price"]
        }
    }