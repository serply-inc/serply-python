import os
import asyncio
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_scholar_search():
    url = serply.__generate_url__(keyword="machine learning research", endpoint="scholar")
    assert url == "https://api.serply.io/v1/scholar/q=machine+learning+research&num=10"

def test_generate_scholar_search_url_num_100():
    url = serply.__generate_url__(keyword="machine learning research", endpoint="scholar", num=100)
    assert url == "https://api.serply.io/v1/scholar/q=machine+learning+research&num=100"


def test_generate_scholar_search_url_start():
    url = serply.__generate_url__(keyword="machine learning research", endpoint="scholar", start=33)
    assert url == "https://api.serply.io/v1/scholar/q=machine+learning+research&num=10&start=33"


def test_generate_scholar_search_url_start_gl():
    url = serply.__generate_url__(keyword="machine learning research", endpoint="scholar", start=33, gl="de")
    assert url == "https://api.serply.io/v1/scholar/q=machine+learning+research&num=10&start=33&gl=de"


def test_simple_scholar_search_default():
    results = serply.scholar(keyword="machine learning")
    assert results
    assert "html" in results


def test_simple_search_default_async():
    results = asyncio.run(serply.scholar_async(keyword="machine learning"))
    assert results
    assert "html" in results