import time
import platform
import requests
import aiohttp
import logging
from . import __version__
from .consts import PROXY_LOCATIONS
from urllib.parse import urlencode, unquote


class Serply(object):
    def __init__(
        self,
        api_key: str,
        api_version: str = "v1",
        device_type: str = None,
        proxy_location: str = "",
        logger: logging.Manager = None,
    ):
        """
            create a instance of Serply object
        :param api_key: str: api key to authenticate with API service
        :param api_version: str: the version
        :param device_type: str: device type to use (defaults to desktop) [desktop, mobile]
        :param logger:
        """
        self.logger = logger or logging.getLogger(__name__)
        self.base_url = "https://api.serply.io/"
        self.api_version = api_version
        self.api_key = api_key
        self.logger.info(
            f"Serply Python SDK version: {__version__} using API version {self.api_version} of the API."
        )

        self.headers = {
            "User-Agent": f"serply-python/{__version__}  ({platform.platform()}) API/{self.api_version}"
        }
        if not self.api_key:
            self.logger.error("API key is required.")
        else:
            self.headers["apikey"] = self.api_key

        # check additional options
        if device_type and device_type.lower() in ["mobile", "m"]:
            self.headers["X-User-Agent"] = "mobile"
        else:
            self.headers["X-User-Agent"] = "desktop"

        if proxy_location:
            if proxy_location.upper() in PROXY_LOCATIONS:
                self.headers["X-Proxy-Location"] = proxy_location.upper()

        self.session = requests.Session()
        self.session.headers.update(self.headers)


    def __generate_search_url__(self, keyword: str, num:int =10 , *args, **kwargs):
        """
            generate the search url
        :param args:
        :param kwargs:
        :return:
        """
        params = {
            "q": unquote(keyword),
            "num": num,
        }

        if "start" in kwargs and kwargs['start']:
            params["start"] = kwargs['start']
        if "gl" in kwargs and kwargs['gl']:
            params["gl"] = kwargs['gl']
        if "lr" in kwargs and kwargs['lr']:
            params["lr"] = kwargs['lr']
        if "hl" in kwargs and kwargs['hl']:
            params["hl"] = kwargs['hl']
        if "cr" in kwargs and kwargs['cr']:
            params["cr"] = kwargs['cr']
        if "cr" in kwargs and kwargs['cr']:
            params["cr"] = kwargs['cr']
        if "loc" in kwargs and kwargs['loc']:
            params["loc"] = kwargs['loc']

        if "engine" in kwargs and kwargs['engine'].lower() in ["bing", "b"]:
            return f"{self.base_url}{self.api_version}/b/search/{urlencode(params)}"
        else:
            # defaults to google
            return f"{self.base_url}{self.api_version}/search/{urlencode(params)}"

    def search(
        self,
        keyword: str,
        num: int = 10,
        engine: str = "google",
        *args,
        **kwargs
    ) -> dict:
        """
            search for a product
            https://www.seoquake.com/blog/google-search-param/ for guidance on params
            https://webapps.stackexchange.com/questions/16047/how-to-restrict-a-google-search-to-results-of-a-specific-language
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :param engine: str: search engine to use (defaults to google) [google, bing]
        :param start: int: start index for results (defaults to 0)
        :param lr: str: language code to use for search (defaults to en)
        :param hl: str: web interface language lang_xx (defaults to lang_en)
        :param cr: str: country code to use countrXX for search (e.g countryUS, countryCA, countryGB)
        :param gl: str: geolocation country code (xx) to perform search (e.g 'us', 'ca', 'gb')
        :param loc: str: find results for a given area (e.g. "new york", "san francisco", "london)
        :return: dict: response from API
        """
        results = {}
        url = self.__generate_search_url__(keyword=keyword, num=num, engine=engine, *args, **kwargs)

        start = time.time()
        resp = self.session.get(url)
        end = time.time()
        self.logger.debug(f"Search took {end - start} seconds")

        if resp.status_code != 200:
            self.logger.error(f"Error {resp.status_code} {resp.text}")
            return {}

        results = resp.json()
        results['real_time'] = end - start

        return resp.json()

    async def search_async(
        self,
        keyword: str,
        num: int = 10,
        engine: str = "google",
        *args,
        **kwargs
    ) -> dict:
        """
            search for a product
            https://www.seoquake.com/blog/google-search-param/ for guidance on params
            https://webapps.stackexchange.com/questions/16047/how-to-restrict-a-google-search-to-results-of-a-specific-language
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :param engine: str: search engine to use (defaults to google) [google, bing]
        :param start: int: start index for results (defaults to 0)
        :param lr: str: language code to use for search (defaults to en)
        :param hl: str: web interface language lang_xx (defaults to lang_en)
        :param cr: str: country code to use countrXX for search (e.g countryUS, countryCA, countryGB)
        :param gl: str: geolocation country code (xx) to perform search (e.g 'us', 'ca', 'gb')
        :param loc: str: find results for a given area (e.g. "new york", "san francisco", "london)
        :return: dict: response from API
        """
        results = {}

        url = self.__generate_search_url__(keyword=keyword, num=num, engine=engine, *args, **kwargs)

        start = time.time()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            async with session.get(url) as resp:
                resp.raise_for_status()
                text = await resp.text()
                results = await resp.json()

        end = time.time()
        self.logger.debug(f"Search took {end - start} seconds")
        results['real_time'] = end - start
        return results

