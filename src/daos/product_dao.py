"""
Product DAO (Data Access Object)
SPDX - License - Identifier: LGPL - 3.0 - or -later
Auteurs : Gabriel C. Ullmann, Fabio Petrillo, 2025
"""
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from models.product import Product

class ProductDAO:
    def __init__(self):
        load_dotenv(dotenv_path=".env")
        mongo_host = os.getenv("MONGODB_HOST")
        mongo_port = os.getenv("MONGODB_PORT")
        mongo_user = os.getenv("MONGODB_USERNAME")
        mongo_pass = os.getenv("MONGODB_PASSWORD")
        db_name = os.getenv("MONGODB_DB_NAME")

        self.client = MongoClient(
            f"mongodb://{mongo_user}:{mongo_pass}@{mongo_host}:{mongo_port}/"
        )

        self.db = self.client[db_name]
        self.collection = self.db["products"]

    def seed(self):
        if self.collection.count_documents({}) == 0:
            self.collection.insert_many([
                {"name": "Produit A", "brand": "Brand A", "price": 1},
                {"name": "Produit B", "brand": "Brand B", "price": 2},
                {"name": "Produit C", "brand": "Brand C", "price": 3},
            ])

    def select_all(self):
        """ Select all products from MySQL """
        rows = self.collection.find()
        return [
            Product(
                row.get("id"),
                row.get("name"),
                row.get("brand"),
                row.get("price"),
            )
            for row in rows
        ]

    def insert(self, product):
        """ Insert given product into MySQL """
        result = self.collection.insert_one({
            "name": product.name,
            "brand": product.brand,
            "price": product.price
        })
        return str(result.inserted_id)

    def update(self, product):
        self.collection.update_one(
            {"_id": ObjectId(product.id)},
            {"$set": {
                "name": product.name,
                "brand": product.brand,
                "price": product.price
            }}
        )

    def delete(self, product_id):
        """ Delete product from MySQL with given product ID """
        self.collection.delete_one(
            {"_id": ObjectId(product_id)}
        )

    def delete_all(self):
        """ Empty products table in MySQL """
        rows = self.collection.find()
        return [
            Product(
                str(row.get("_id")),
                row.get("name"),
                row.get("brand"),
                row.get("price"),
            )
            for row in rows
        ]
        
    def close(self):
        """ Close MongoDB connection """
        self.client.close()
