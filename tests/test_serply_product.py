import os
import asyncio
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_product_one_search_url():
    url = serply.__generate_url__(keyword="computers", endpoint="product")
    assert url == "https://api.serply.io/v1/product/search/q=computers"


def test_generate_simple_product_two_search_url():
    url = serply.__generate_url__(keyword="toys", endpoint="product")
    assert url == "https://api.serply.io/v1/product/search/q=toys"


def test_generate_product_search_snacks():
    url = serply.__generate_url__(keyword="snacks", endpoint="product")
    assert url == "https://api.serply.io/v1/product/search/q=snacks"


def test_simple_product_search_default():
    results = serply.product(keyword="iphones")
    assert results
    assert "results" not in results
    assert "products" in results
    assert len(results["products"]) > 0
    for product in results["products"]:
        assert "link" in product
        assert product["link"]


def test_simple_product_search_async():
    results = asyncio.run(serply.product_async(keyword="laptops"))
    assert results
    assert "results" not in results
    assert "products" in results
    assert len(results["products"]) > 0
    for product in results["products"]:
        assert "link" in product
        assert product["link"]
