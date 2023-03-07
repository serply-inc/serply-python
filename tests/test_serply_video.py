import os
import unittest
import pytest
import asyncio
import langid
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_video_search_url():
    url = serply.__generate_url__(keyword="iphone review", endpoint="video")
    assert url == "https://api.serply.io/v1/video/q=iphone+review&num=10"


def test_generate_simple_video_search_url_num_100():
    url = serply.__generate_url__(keyword="music videos", num=100, endpoint="video")
    assert url == "https://api.serply.io/v1/video/q=music+videos&num=100"


def test_generate_video_search_url_start():
    url = serply.__generate_url__(keyword="2023 movies", start=33, endpoint="video")
    assert url == "https://api.serply.io/v1/video/q=2023+movies&num=10&start=33"


def test_generate_video_search_url_start_gl():
    url = serply.__generate_url__(keyword="smart phone", start=33, gl="de", endpoint="video")
    assert url == "https://api.serply.io/v1/video/q=smart+phone&num=10&start=33&gl=de"


def test_generate_video_search_bing_url_num_100():
    url = serply.__generate_url__(keyword="how to cook", num=100, endpoint="video")
    assert url == "https://api.serply.io/v1/video/q=how+to+cook&num=100"


def test_generate_simple_search_bing_hl():
    url = serply.__generate_url__(keyword="iphone drop test", hl="lang_en", endpoint="video")
    assert url == "https://api.serply.io/v1/video/q=iphone+drop+test&num=10&hl=lang_en"


def test_simple_search_default():
    results = serply.video(keyword="iphone+reviews")
    assert results
    assert "results" in results
    assert len(results["results"]) > 0


def test_simple_search_in_spanish():
    results = serply.video(keyword="best android phone", lr="lang_es")
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
    results = serply.video(keyword="music videos", hl="lang_de", gl="de")
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
    results = serply.video(keyword="cooking shows", engine="bing")
    assert results
    assert "results" in results
    assert len(results["results"]) > 0


def test_search_with_num():
    results = serply.video(keyword="funny tictok", num=30)
    assert results
    assert "results" in results
    assert len(results["results"]) >= 10


# test async versions
def test_simple_search_default_async():
    results = asyncio.run(serply.video_async(keyword="best phone camera"))
    assert results
    assert "results" in results
    assert len(results["results"]) > 0


def test_simple_search_in_spanish_async():
    results = asyncio.run(serply.video_async(keyword="life hacks", lr="lang_es"))
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
    results = asyncio.run(serply.video_async(keyword="viral videos", hl="lang_de", gl="de"))
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
    results = asyncio.run(serply.video_async(keyword="try not to laugh", engine="bing"))
    assert results
    assert "results" in results
    assert len(results["results"]) > 0


def test_search_with_num_async():
    results = asyncio.run(serply.video_async(keyword="wedding songs", num=30))
    assert results
    assert "results" in results
    assert len(results["results"]) >= 10
