import os
import asyncio
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

PROXY_LOCATIONS = [
    "US",
    "CA",
    "IE",
    "GB",
    "FR",
    "DE",
    "SE",
    "IN",
    "JP",
    "KR",
    "SG",
    "AU",
    "BR",
    "EU",
]


async def search_proxy_location(proxy_location: str):
    serply = Serply(api_key=API_KEY, proxy_location=proxy_location)
    results = await serply.search_async(keyword="iphone", num=30)
    return results


async def search_proxy_locations():
    tasks = [
        search_proxy_location(proxy_location) for proxy_location in PROXY_LOCATIONS
    ]
    results = await asyncio.gather(*tasks)
    return results


def test_search_with_num_async():
    results = results = asyncio.run(search_proxy_locations())
    assert results
    for result in results:
        assert result
        assert "results" in result
        assert len(result["results"]) >= 10
