import pytest
import os
import logging
import asyncio
from aiohttp.client_exceptions import ClientResponseError
from serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_unsported_endpoint_job_url():
    with pytest.raises(ValueError) as e:
        serply.__generate_url__(keyword="nurse practitioner", endpoint="asdf")
        logging.error(e)


def test_request_post_serp_with_website_url_not_exists():
    data = {"query": "q=iphone", "domain": "apple.com", "website": "apple.com"}
    url = "https://api.serply.io/v1/asdfasdf/"
    results = serply.__make_request__(url=url, method="post", json=data)
    assert results
    assert "error" in results


# test post versions
def test_request_post_serp_with_website_url_not_exists_async():
    data = {"query": "q=iphone", "domain": "apple.com", "website": "apple.com"}
    url = "https://api.serply.io/v1/asdfasdf/"
    with pytest.raises(ClientResponseError) as e:
        results = asyncio.run(
            serply.__make_request_async__(url=url, method="post", json=data)
        )
        assert "result" in results
        assert "title" in results["result"]
        assert "position" in results
        assert results["position"] == 1


# test post versions
def test_request_get_serp_with_website_url_not_exists_async():
    data = {"query": "q=iphone", "domain": "apple.com", "website": "apple.com"}
    url = "https://api.serply.io/v1/asdfasdf/"
    with pytest.raises(ClientResponseError) as e:
        results = asyncio.run(
            serply.__make_request_async__(url=url, method="get")
        )
        assert "result" in results
        assert "title" in results["result"]
        assert "position" in results
        assert results["position"] == 1