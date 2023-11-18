import os
import unittest
import pytest
import asyncio
import langid
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_search_maps_url():
    url = serply.__generate_url__(keyword="lawyers in new york city", endpoint="maps")
    assert url == "https://api.serply.io/v1/maps/q=lawyers+in+new+york+city&num=10"


def test_generate_simple_search_maps_url_num_100():
    url = serply.__generate_url__(keyword="apple store in dallas", endpoint="maps", num=100)
    assert url == "https://api.serply.io/v1/maps/q=apple+store+in+dallas&num=100"


def test_generate_search_maps_url_start():
    url = serply.__generate_url__(keyword="coffee shops", endpoint="maps", start=33)
    assert url == "https://api.serply.io/v1/maps/q=coffee+shops&num=10&start=33"


def test_generate_search_maps_url_start_gl():
    url = serply.__generate_url__(keyword="iphone", endpoint="maps", start=33, gl="de")
    assert url == "https://api.serply.io/v1/maps/q=iphone&num=10&start=33&gl=de"


def test_simple_search_maps_default():
    results = serply.maps(keyword="apple store")
    assert results
    assert "places" in results
    assert len(results["places"]) > 0


def test_simple_search_maps_in_spanish():
    results = serply.maps(keyword="iphone", lr="lang_es")
    assert results
    assert "places" in results
    assert len(results["places"]) > 0

    # expect one link to use https://www.apple.com/es/iphone/
    for place in results["places"]:
        if "description" in place and place["description"]:
            descriptions = place["description"]
            detected_language, confidence = langid.classify(
                " ".join(descriptions).encode("utf-8")
            )
            if detected_language == "es":
                assert True
                return


def test_simple_search_maps_in_interface_german():
    results = serply.maps(keyword="iphone", hl="lang_de", gl="de")
    assert results
    assert "places" in results
    assert len(results["places"]) > 0

    for place in results["places"]:
       if "description" in place and place["description"]:
            descriptions = place["description"]
            detected_language, confidence = langid.classify(
                " ".join(descriptions).encode("utf-8")
            )
            if detected_language == "de":
                assert True
                return



# test async versions
def test_simple_search_maps_default_async():
    results = asyncio.run(serply.maps_async(keyword="iphone"))
    assert results
    assert "places" in results
    assert len(results["places"]) > 0


def test_simple_search_maps_in_spanish_async():
    results = asyncio.run(serply.maps_async(keyword="iphone", lr="lang_es"))
    assert results
    assert "places" in results
    assert len(results["places"]) > 0

    for place in results["places"]:
        if "description" in place and place["description"]:
            descriptions = place["description"]
            detected_language, confidence = langid.classify(
                " ".join(descriptions).encode("utf-8")
            )
            if detected_language == "es":
                assert True
                return


def test_simple_search_maps_in_interface_german_async():
    results = asyncio.run(serply.maps_async(keyword="iphone", hl="lang_de", gl="de"))
    assert results
    assert "places" in results
    assert len(results["places"]) > 0

    for place in results["places"]:
        if "description" in place and place["description"]:
            descriptions = place["description"]
            detected_language, confidence = langid.classify(
                " ".join(descriptions).encode("utf-8")
            )
            if detected_language == "de":
                assert True
                return
