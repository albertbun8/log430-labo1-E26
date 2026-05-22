from daos.product_dao import ProductDAO
from models.product import Product

dao = ProductDAO()

def test_product_select():
    dao.seed()
    product_list = dao.select_all()
    assert len(product_list) >= 3

def test_product_insert():
    product = Product(None, 'Produit A', 'Brand A', 1)
    dao.insert(product)
    product_list = dao.select_all()
    products = [p.name for p in product_list]
    assert product.name in products

def test_product_update():
    product = Product(None, 'Produit B', 'Brand B', 2)
    assigned_id = dao.insert(product)

    corrected_brand = 'Brand C'
    product.id = assigned_id
    product.brand = corrected_brand
    dao.update(product)

    product_list = dao.select_all()
    products = [p.brand for p in product_list]
    assert corrected_brand in products

    # cleanup
    dao.delete(assigned_id)

def test_product_delete():
    product = Product(None, 'Product Test', 'Test brand', 3)
    assigned_id = dao.insert(product)

    dao.delete(assigned_id)

    product_list = dao.select_all()
    ids = [p.id for p in product_list]

    assert assigned_id not in ids