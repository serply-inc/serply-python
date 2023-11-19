import os
import asyncio
import langid
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_news_url():
    url = serply.__generate_url__(keyword="bitcoin", endpoint="news")
    assert url == "https://api.serply.io/v1/news/q=bitcoin&num=10"


def test_generate_simple_news_url_num_100():
    url = serply.__generate_url__(keyword="bitcoin", endpoint="news", num=100)
    assert url == "https://api.serply.io/v1/news/q=bitcoin&num=100"


def test_generate_news_url_start():
    url = serply.__generate_url__(keyword="bitcoin", endpoint="news", start=33)
    assert url == "https://api.serply.io/v1/news/q=bitcoin&num=10&start=33"


def test_generate_news_url_start_gl():
    url = serply.__generate_url__(keyword="bitcoin", endpoint="news", start=33, gl="de")
    assert url == "https://api.serply.io/v1/news/q=bitcoin&num=10&start=33&gl=de"


def test_simple_news_default():
    results = serply.news(keyword="bitcoin")
    assert "feed" in results
    assert results["feed"]
    assert "entries" in results
    assert results["entries"]
    assert len(results["entries"]) > 0


def test_simple_news_in_spanish():
    results = serply.news(keyword="bitcoin", hl="lang_es", gl="es")
    assert "feed" in results
    assert results["feed"]
    assert "entries" in results
    assert results["entries"]
    assert len(results["entries"]) > 0

    # expect first source to include "es" in the url and title to be in spanish
    detected_language, confidence = langid.classify(
        results["entries"][0]["title"].encode("utf-8")
    )
    assert detected_language == "es"


def test_simple_news_in_interface_german():
    results = serply.news(keyword="bitcoin", hl="lang_de", gl="de")
    assert results
    assert "feed" in results
    assert results["feed"]
    assert "entries" in results
    assert results["entries"]
    assert len(results["entries"]) > 0

    # expect first source to include "es" in the url and title to be in spanish
    detected_language, confidence = langid.classify(
        results["entries"][0]["title"].encode("utf-8")
    )
    assert detected_language == "de"


# test async versions
def test_simple_news_default_async():
    results = asyncio.run(serply.news_async(keyword="apple stock"))
    assert "feed" in results
    assert results["feed"]
    assert "entries" in results
    assert results["entries"]
    assert len(results["entries"]) > 0


def test_simple_news_in_spanish_async():
    results = asyncio.run(
        serply.news_async(keyword="apple", hl="lang_es", gl="es")
    )
    assert results
    assert "feed" in results
    assert results["feed"]
    assert "entries" in results
    assert results["entries"]
    assert len(results["entries"]) > 0

    # expect first source to include "es" in the url and title to be in spanish
    detected_language, confidence = langid.classify(
        results["entries"][0]["title"].encode("utf-8")
    )
    assert detected_language == "es"


def test_simple_news_in_interface_german_async():
    results = asyncio.run(
        serply.news_async(keyword="microsoft", hl="lang_de", gl="de")
    )
    assert results
    assert "feed" in results
    assert results["feed"]
    assert "entries" in results
    assert results["entries"]
    assert len(results["entries"]) > 0
    # expect first source to include "es" in the url and title to be in spanish
    detected_language, confidence = langid.classify(
        results["entries"][0]["title"].encode("utf-8")
    )
    assert detected_language == "de"
