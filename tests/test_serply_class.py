import os
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", "")


def test_no_api_key():
    Serply(api_key=None)


def test_search_with_no_api_key():
    s = Serply(api_key=None)

    # making search withouth api key
    results = s.search(keyword="test")
    assert "error" in results

    # making search async withouth api key
    results = s.search(keyword="test")
    assert "error" in results


def test_empty_api_key():
    Serply(api_key="")
