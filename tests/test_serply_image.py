import os
import asyncio
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_image_search_url():
    url = serply.__generate_url__(keyword="computers", endpoint="image")
    assert url == "https://api.serply.io/v1/image/q=computers&num=10"


def test_generate_simple_image_search_url_num_100():
    url = serply.__generate_url__(keyword="toys", num=100, endpoint="image")
    assert url == "https://api.serply.io/v1/image/q=toys&num=100"


def test_generate_image_url_start():
    url = serply.__generate_url__(keyword="movies", start=33, endpoint="image")
    assert url == "https://api.serply.io/v1/image/q=movies&num=10&start=33"


def test_generate_image_search_url_start_gl():
    url = serply.__generate_url__(
        keyword="smart phone", start=33, gl="de", endpoint="image"
    )
    assert url == "https://api.serply.io/v1/image/q=smart+phone&num=10&start=33&gl=de"


def test_generate_image_search_food():
    url = serply.__generate_url__(keyword="food", num=100, endpoint="image")
    assert url == "https://api.serply.io/v1/image/q=food&num=100"


def test_generate_simple_search_bing_hl():
    url = serply.__generate_url__(
        keyword="iphone drop test", hl="lang_en", endpoint="image"
    )
    assert url == "https://api.serply.io/v1/image/q=iphone+drop+test&num=10&hl=lang_en"


def test_simple_image_search_default():
    results = serply.image(keyword="iphone+reviews")
    assert results
    assert "results" in results
    assert len(results["results"]) == 0
    assert "image_results" in results
    assert len(results["image_results"]) > 0


def test_simple_image_search_in_spanish():
    results = serply.image(keyword="best android phone", lr="lang_es")
    assert results
    assert "results" in results
    assert len(results["results"]) == 0
    assert "image_results" in results
    assert len(results["image_results"]) > 0


def test_simple_image_search_in_interface_german():
    results = serply.image(keyword="music", hl="lang_de", gl="de")
    assert results
    assert "results" in results
    assert len(results["results"]) == 0
    assert "image_results" in results
    assert len(results["image_results"]) > 0


def test_image_simple_image_search():
    results = serply.image(keyword="hamburgers")
    assert results
    # should expect zero results but more than 0 image_results
    assert "results" in results
    assert len(results["results"]) == 0
    assert "image_results" in results
    assert len(results["image_results"]) > 0


def test_image_search_with_num():
    results = serply.image(keyword="tictok", num=30)
    assert results
    # should expect zero results but more than 0 image_results
    assert "results" in results
    assert len(results["results"]) == 0
    assert "image_results" in results
    assert len(results["image_results"]) > 0


# test async versions
def test_simple_image_search_default_async():
    results = asyncio.run(serply.image_async(keyword="best phone camera"))
    assert results
    # should expect zero results but more than 0 image_results
    assert "results" in results
    assert len(results["results"]) == 0
    assert "image_results" in results
    assert len(results["image_results"]) > 0


def test_simple_image_search_in_spanish_async():
    results = asyncio.run(serply.image_async(keyword="life hacks", lr="lang_es"))
    assert results
    # should expect zero results but more than 0 image_results
    assert "results" in results
    assert len(results["results"]) == 0
    assert "image_results" in results
    assert len(results["image_results"]) > 0


def test_simple_search_in_interface_german_async():
    results = asyncio.run(
        serply.image_async(keyword="viral videos", hl="lang_de", gl="de")
    )
    assert results
    # should expect zero results but more than 0 image_results
    assert "results" in results
    assert len(results["results"]) == 0
    assert "image_results" in results
    assert len(results["image_results"]) > 0


def test_simple_image_search_music_async():
    results = asyncio.run(serply.image_async(keyword="music"))
    assert results
    # should expect zero results but more than 0 image_results
    assert "results" in results
    assert len(results["results"]) == 0
    assert "image_results" in results
    assert len(results["image_results"]) > 0


def test_image_search_with_num_async():
    results = asyncio.run(serply.image_async(keyword="wedding", num=30))
    assert results
    # should expect zero results but more than 0 image_results
    assert "results" in results
    assert len(results["results"]) == 0
    assert "image_results" in results
    assert len(results["image_results"]) > 0
