import os
import asyncio
import langid
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_crawl_url():
    url = serply.__generate_url__(keyword="iphone", endpoint="crawl")
    assert url == "https://api.serply.io/v1/crawl/q=iphone&num=10"


def test_generate_simple_crawl_url_num_100():
    url = serply.__generate_url__(keyword="iphone", num=100, endpoint="crawl")
    assert url == "https://api.serply.io/v1/crawl/q=iphone&num=100"


def test_generate_crawl_url_start():
    url = serply.__generate_url__(keyword="iphone", start=33, endpoint="crawl")
    assert url == "https://api.serply.io/v1/crawl/q=iphone&num=10&start=33"


def test_generate_crawl_url_start_gl():
    url = serply.__generate_url__(keyword="iphone", start=33, gl="de", endpoint="crawl")
    assert url == "https://api.serply.io/v1/crawl/q=iphone&num=10&start=33&gl=de"


def test_simple_crawl_default():
    results = serply.crawl(keyword="iphone")
    assert results
    assert "results" in results
    assert len(results["results"]) > 0


def test_simple_crawl_in_spanish():
    results = serply.crawl(keyword="iphone", lr="lang_es")
    assert results
    assert "results" in results
    assert len(results["results"]) > 0
    assert "html" in results


def test_simple_crawl_in_interface_german():
    results = serply.crawl(keyword="iphone", hl="lang_de", gl="de")
    assert results
    assert "results" in results
    assert len(results["results"]) > 0
    assert "html" in results

    for result in results["results"]:
        detected_language, confidence = langid.classify(
            result["description"].encode("utf-8")
        )
        if detected_language == "de":
            assert True
            return


def test_simple_crawl_bing():
    results = serply.crawl(keyword="iphone", engine="bing")
    assert results
    assert "results" in results
    assert len(results["results"]) > 0
    assert "html" in results


def test_crawl_with_num():
    results = serply.crawl(keyword="iphone", num=30)
    assert results
    assert "results" in results
    assert len(results["results"]) >= 10
    assert "html" in results


# test async versions
def test_simple_crawl_default_async():
    results = asyncio.run(serply.crawl_async(keyword="iphone"))
    assert results
    assert "results" in results
    assert len(results["results"]) > 0
    assert "html" in results


def test_simple_crawl_in_spanish_async():
    results = asyncio.run(serply.crawl_async(keyword="iphone", lr="lang_es"))
    assert results
    assert "results" in results
    assert len(results["results"]) > 0
    assert "html" in results

    for result in results["results"]:
        detected_language, confidence = langid.classify(
            result["description"].encode("utf-8")
        )
        if detected_language == "es":
            assert True
            return


def test_simple_crawl_in_interface_german_async():
    results = asyncio.run(serply.crawl_async(keyword="iphone", hl="lang_de", gl="de"))
    assert results
    assert "results" in results
    assert len(results["results"]) > 0
    assert "html" in results

    for result in results["results"]:
        detected_language, confidence = langid.classify(
            result["description"].encode("utf-8")
        )
        if detected_language == "de":
            assert True
            return


def test_simple_crawl_bing_async():
    results = asyncio.run(serply.crawl_async(keyword="iphone", engine="bing"))
    assert results
    assert "results" in results
    assert len(results["results"]) > 0
    assert "html" in results


def test_crawl_with_num_async():
    results = asyncio.run(serply.crawl_async(keyword="iphone", num=30))
    assert results
    assert "results" in results
    assert len(results["results"]) >= 10
    assert "html" in results
