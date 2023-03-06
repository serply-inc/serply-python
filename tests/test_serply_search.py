import os
import unittest
import pytest
import asyncio
import langid
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_search_url():
    url = serply.__generate_url__(keyword="iphone")
    assert url == "https://api.serply.io/v1/search/q=iphone&num=10"


def test_generate_simple_search_url_num_100():
    url = serply.__generate_url__(keyword="iphone", num=100)
    assert url == "https://api.serply.io/v1/search/q=iphone&num=100"


def test_generate_search_url_start():
    url = serply.__generate_url__(keyword="iphone", start=33)
    assert url == "https://api.serply.io/v1/search/q=iphone&num=10&start=33"


def test_generate_search_url_start_gl():
    url = serply.__generate_url__(keyword="iphone", start=33, gl="de")
    assert url == "https://api.serply.io/v1/search/q=iphone&num=10&start=33&gl=de"


def test_generate_simple_search_bing_url_num_100():
    url = serply.__generate_url__(keyword="iphone", num=100, engine="bing")
    assert url == "https://api.serply.io/v1/b/search/q=iphone&num=100"


def test_generate_simple_search_bing_hl():
    url = serply.__generate_url__(keyword="iphone", hl="lang_en", engine="bing")
    assert url == "https://api.serply.io/v1/b/search/q=iphone&num=10&hl=lang_en"


def test_simple_search_default():
    results = serply.search(keyword="iphone")
    assert results
    assert "results" in results
    assert len(results["results"]) > 0


def test_simple_search_in_spanish():
    results = serply.search(keyword="iphone", lr="lang_es")
    assert results
    assert "results" in results
    assert len(results["results"]) > 0

    # expect one link to use https://www.apple.com/es/iphone/
    for result in results["results"]:
        detected_language, confidence = langid.classify(
            result["description"].encode("utf-8")
        )
        if detected_language == "es":
            assert True
            return


def test_simple_search_in_interface_german():
    results = serply.search(keyword="iphone", hl="lang_de", gl="de")
    assert results
    assert "results" in results
    assert len(results["results"]) > 0

    for result in results["results"]:
        detected_language, confidence = langid.classify(
            result["description"].encode("utf-8")
        )
        if detected_language == "de":
            assert True
            return


def test_simple_search_bing():
    results = serply.search(keyword="iphone", engine="bing")
    assert results
    assert "results" in results
    assert len(results["results"]) > 0


def test_search_with_num():
    results = serply.search(keyword="iphone", num=30)
    assert results
    assert "results" in results
    assert len(results["results"]) >= 10


# test async versions
def test_simple_search_default_async():
    results = asyncio.run(serply.search_async(keyword="iphone"))
    assert results
    assert "results" in results
    assert len(results["results"]) > 0


def test_simple_search_in_spanish_async():
    results = asyncio.run(serply.search_async(keyword="iphone", lr="lang_es"))
    assert results
    assert "results" in results
    assert len(results["results"]) > 0

    for result in results["results"]:
        detected_language, confidence = langid.classify(
            result["description"].encode("utf-8")
        )
        if detected_language == "es":
            assert True
            return


def test_simple_search_in_interface_german_async():
    results = asyncio.run(serply.search_async(keyword="iphone", hl="lang_de", gl="de"))
    assert results
    assert "results" in results
    assert len(results["results"]) > 0

    for result in results["results"]:
        detected_language, confidence = langid.classify(
            result["description"].encode("utf-8")
        )
        if detected_language == "de":
            assert True
            return


def test_simple_search_bing_async():
    results = asyncio.run(serply.search_async(keyword="iphone", engine="bing"))
    assert results
    assert "results" in results
    assert len(results["results"]) > 0


def test_search_with_num_async():
    results = asyncio.run(serply.search_async(keyword="iphone", num=30))
    assert results
    assert "results" in results
    assert len(results["results"]) >= 10
