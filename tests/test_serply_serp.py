import os
import unittest
import pytest
import asyncio
import langid
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_serp_without_domain_or_website_url():
    try:
        url = serply.__generate_url__(keyword="iphone", endpoint="serp")
        assert url == "https://api.serply.io/v1/serp/q=iphone&num=10"
    except ValueError:
        pass


def test_generate_simple_serp_url_num_100_url():
    url = serply.__generate_url__(keyword="iphone", endpoint="serp", domain="example.com")
    assert url == "https://api.serply.io/v1/serp/q=iphone&num=10&domain=example.com"


def test_generate_serp_url_start_url():
    url = serply.__generate_url__(keyword="iphone", start=33, endpoint="serp", domain="example.com")
    assert url == "https://api.serply.io/v1/serp/q=iphone&num=10&start=33&domain=example.com"


def test_generate_serp_url_start_gl_url():
    url = serply.__generate_url__(keyword="iphone", start=33, gl="de", endpoint="serp", domain="example.com")
    assert url == "https://api.serply.io/v1/serp/q=iphone&num=10&start=33&gl=de&domain=example.com"


def test_generate_serp_with_website_url():
    url = serply.__generate_url__(keyword="iphone", start=33, gl="de", endpoint="serp", website="https://www.example.com")
    assert url == "https://api.serply.io/v1/serp/q=iphone&num=10&start=33&gl=de&website=https%3A%2F%2Fwww.example.com"


def test_simple_serp_default_without_domain():
    # should raise value error without domain or website
    try:
        results = serply.serp(keyword="android")
    except ValueError:
        pass
    except TypeError:
        pass


def test_simple_serp_default_apple():
    # should raise value error without domain or website
    results = serply.serp(keyword="iphone", domain="apple.com")
    assert results
    assert "result" in results
    assert "title" in results['result']
    assert "position" in results
    assert results["position"] == 1


def test_simple_serp_default_microsoft():
    results = serply.serp(keyword="windows", domain="microsoft.com")
    assert "result" in results
    assert "title" in results['result']
    assert "position" in results
    assert results["position"] == 1


def test_simple_serp_default_not_found():
    results = serply.serp(keyword="search engine", domain="exmaple.com")
    assert "result" in results
    assert not results["result"]


def test_simple_search_in_spanish():
    results = serply.serp(keyword="iphone", lr="lang_es", domain="apple.com")
    assert "result" in results
    assert "title" in results['result']
    assert "position" in results
    assert results["position"] == 1
    assert results["result"]["link"] == "https://www.apple.com/es/iphone/"


def test_simple_search_in_interface_german():
    results = serply.serp(keyword="iphone", hl="lang_de", gl="de", domain="apple.com")
    assert "result" in results
    assert "title" in results['result']
    assert "position" in results
    assert results["position"] == 1
    assert results["result"]["link"] == "https://www.apple.com/de/iphone/"


# test async versions
def test_simple_search_default_async():
    results = asyncio.run(serply.serp_async(keyword="youtube", domain="youtube.com"))
    assert "result" in results
    assert "title" in results['result']
    assert "position" in results
    assert results["position"] == 1