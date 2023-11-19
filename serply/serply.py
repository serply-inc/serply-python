import time
import platform
import requests
import aiohttp
import logging
from typing import Dict
from . import __version__
from .consts import PROXY_LOCATIONS
from urllib.parse import urlencode, unquote


class Serply(object):
    def __init__(
        self,
        api_key: str,
        api_version: str = "v1",
        device_type: str = "",
        proxy_location: str = "",
        logger: logging.Logger = logging.getLogger(__name__),
    ):
        """
            create a instance of Serply object
        :param api_key: str: api key to authenticate with API service
        :param api_version: str: the version
        :param device_type: str: device type to use (defaults to desktop) [desktop, mobile]
        :param logger:
        """
        self.logger = logger
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

    def __generate_url__(
        self, keyword: str, num: int = 10, endpoint: str = "search", *args, **kwargs
    ):
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

        if "start" in kwargs and kwargs["start"]:
            params["start"] = kwargs["start"]
        if "gl" in kwargs and kwargs["gl"]:
            params["gl"] = kwargs["gl"]
        if "lr" in kwargs and kwargs["lr"]:
            params["lr"] = kwargs["lr"]
        if "hl" in kwargs and kwargs["hl"]:
            params["hl"] = kwargs["hl"]
        if "cr" in kwargs and kwargs["cr"]:
            params["cr"] = kwargs["cr"]
        if "loc" in kwargs and kwargs["loc"]:
            params["loc"] = kwargs["loc"]
        if "domain" in kwargs and kwargs["domain"]:
            params["domain"] = kwargs["domain"]
        if "website" in kwargs and kwargs["website"]:
            params["website"] = kwargs["website"]

        if endpoint == "image":
            return f"{self.base_url}{self.api_version}/image/{urlencode(params)}"
        elif endpoint == "video":
            return f"{self.base_url}{self.api_version}/video/{urlencode(params)}"
        elif endpoint == "scholar":
            return f"{self.base_url}{self.api_version}/scholar/{urlencode(params)}"
        elif endpoint == "job":
            return f"{self.base_url}{self.api_version}/job/search/{urlencode(params)}"
        elif endpoint == "news":
            return f"{self.base_url}{self.api_version}/news/{urlencode(params)}"
        elif endpoint == "maps":
            return f"{self.base_url}{self.api_version}/maps/{urlencode(params)}"
        elif endpoint == "product":
            # product doesn't take num
            if "num" in params:
                del params["num"]
            return (
                f"{self.base_url}{self.api_version}/product/search/{urlencode(params)}"
            )
        elif endpoint == "crawl":
            return f"{self.base_url}{self.api_version}/crawl/{urlencode(params)}"
        elif endpoint == "serp":
            if "domain" not in params and "website" not in params:
                raise ValueError("domain or website is required for the SERP endpoint.")
            return f"{self.base_url}{self.api_version}/serp/{urlencode(params)}"
        elif endpoint == "search":
            # default to search
            if "engine" in kwargs and kwargs["engine"].lower() in ["bing", "b"]:
                return f"{self.base_url}{self.api_version}/b/search/{urlencode(params)}"
            else:
                # defaults to google
                return f"{self.base_url}{self.api_version}/search/{urlencode(params)}"
        else:
            e = "endpoint selected: {endpoint} is not supported."
            self.logger.error(e)
            raise ValueError(e)

    def __make_request__(self, url: str, method: str = "get", *args, **kwargs) -> Dict:
        """
            make a request to the API
        :param url: str: url to make request to
        :param method: str: method to use for request (defaults to get) [get, post]
        :param args:
        :param kwargs:
        :return:
        """
        results = {}
        start = time.time()
        if method.lower() == "post":
            resp = self.session.post(url, *args, **kwargs)
        else:
            resp = self.session.get(url, *args, **kwargs)

        if resp.status_code == 200:
            results = resp.json()
        else:
            self.logger.error(
                f"Error making request to {method} {url} status code: {resp.status_code}"
            )
            results = {
                "error": f"Error making request to {method} {url} status code: {resp.status_code}"
            }

        end = time.time()

        self.logger.debug(f"Request took {end - start} seconds")
        results["request_time"] = end - start

        return results

    async def __make_request_async__(
        self, url: str, method: str = "get", *args, **kwargs
    ) -> Dict:
        """
            make a request to the API
        :param url: str: url to make request to
        :param method: str: method to use for request (defaults to get) [get, post]
        :param args:
        :param kwargs:
        :return:
        """
        results = {}
        start = time.time()
        async with aiohttp.ClientSession(headers=self.headers) as session:
            if method.lower() == "post":
                async with session.post(url, *args, **kwargs) as resp:
                    if resp.status != 200:
                        self.logger.error(
                            f"Error making request to {method} {url} status code: {resp.status}"
                        )
                    resp.raise_for_status()
                    results = await resp.json()
            else:
                async with session.get(url) as resp:
                    if resp.status != 200:
                        self.logger.error(
                            f"Error making request to {method} {url} status code: {resp.status}"
                        )
                    resp.raise_for_status()
                    results = await resp.json()

        end = time.time()
        self.logger.debug(f"Request took {end - start} seconds")
        results["request_time"] = end - start
        return results

    def search(
        self,
        keyword: str,
        num: int = 10,
        engine: str = "google",
        hl="lang_en",
        gl="us",
        lr="lang_en",
        *args,
        **kwargs,
    ) -> dict:
        """
            perform a search
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
        url = self.__generate_url__(
            keyword=keyword,
            num=num,
            engine=engine,
            hl=hl,
            gl=gl,
            lr=lr,
            *args,
            **kwargs,
        )
        self.logger.debug(f"Performing search with {locals()}")
        return self.__make_request__(url=url)

    async def search_async(
        self, keyword: str, num: int = 10, engine: str = "google", *args, **kwargs
    ) -> dict:
        """
            perform a search asynchronously
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

        url = self.__generate_url__(
            keyword=keyword, num=num, endpoint="video", *args, **kwargs
        )

        self.logger.debug(f"Performing async search with {locals()}")
        return await self.__make_request_async__(url=url)

    def video(
        self,
        keyword: str,
        num: int = 10,
        hl="lang_en",
        gl="us",
        lr="lang_en",
        *args,
        **kwargs,
    ) -> dict:
        """
            search for a videos
            https://www.seoquake.com/blog/google-search-param/ for guidance on params
            https://webapps.stackexchange.com/questions/16047/how-to-restrict-a-google-search-to-results-of-a-specific-language
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :param start: int: start index for results (defaults to 0)
        :param lr: str: language code to use for search (defaults to en)
        :param hl: str: web interface language lang_xx (defaults to lang_en)
        :param cr: str: country code to use countrXX for search (e.g countryUS, countryCA, countryGB)
        :param gl: str: geolocation country code (xx) to perform search (e.g 'us', 'ca', 'gb')
        :param loc: str: find results for a given area (e.g. "new york", "san francisco", "london)
        :return: dict: response from API
        """
        url = self.__generate_url__(
            keyword=keyword,
            num=num,
            hl=hl,
            gl=gl,
            lr=lr,
            endpoint="video",
            *args,
            **kwargs,
        )
        self.logger.debug(f"Performing video search with {locals()}")
        return self.__make_request__(url=url)

    async def video_async(self, keyword: str, num: int = 10, *args, **kwargs) -> dict:
        """
            search for videos
            https://www.seoquake.com/blog/google-search-param/ for guidance on params
            https://webapps.stackexchange.com/questions/16047/how-to-restrict-a-google-search-to-results-of-a-specific-language
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :param start: int: start index for results (defaults to 0)
        :param lr: str: language code to use for search (defaults to en)
        :param hl: str: web interface language lang_xx (defaults to lang_en)
        :param cr: str: country code to use countrXX for search (e.g countryUS, countryCA, countryGB)
        :param gl: str: geolocation country code (xx) to perform search (e.g 'us', 'ca', 'gb')
        :param loc: str: find results for a given area (e.g. "new york", "san francisco", "london)
        :return: dict: response from API
        """
        results = {}

        url = self.__generate_url__(
            keyword=keyword, num=num, endpoint="video", *args, **kwargs
        )

        self.logger.debug(f"Performing video async search with {locals()}")
        return await self.__make_request_async__(url=url)

    def image(
        self,
        keyword: str,
        num: int = 10,
        hl="lang_en",
        gl="us",
        lr="lang_en",
        *args,
        **kwargs,
    ) -> dict:
        """
            search for a images
            https://www.seoquake.com/blog/google-search-param/ for guidance on params
            https://webapps.stackexchange.com/questions/16047/how-to-restrict-a-google-search-to-results-of-a-specific-language
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :param start: int: start index for results (defaults to 0)
        :param lr: str: language code to use for search (defaults to en)
        :param hl: str: web interface language lang_xx (defaults to lang_en)
        :param cr: str: country code to use countrXX for search (e.g countryUS, countryCA, countryGB)
        :param gl: str: geolocation country code (xx) to perform search (e.g 'us', 'ca', 'gb')
        :param loc: str: find results for a given area (e.g. "new york", "san francisco", "london)
        :return: dict: response from API
        """
        url = self.__generate_url__(
            keyword=keyword,
            num=num,
            hl=hl,
            gl=gl,
            lr=lr,
            endpoint="image",
            *args,
            **kwargs,
        )
        self.logger.debug(f"Performing image search with {locals()}")
        return self.__make_request__(url=url)

    async def image_async(self, keyword: str, num: int = 10, *args, **kwargs) -> dict:
        """
            search for images
            https://www.seoquake.com/blog/google-search-param/ for guidance on params
            https://webapps.stackexchange.com/questions/16047/how-to-restrict-a-google-search-to-results-of-a-specific-language
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :param start: int: start index for results (defaults to 0)
        :param lr: str: language code to use for search (defaults to en)
        :param hl: str: web interface language lang_xx (defaults to lang_en)
        :param cr: str: country code to use countrXX for search (e.g countryUS, countryCA, countryGB)
        :param gl: str: geolocation country code (xx) to perform search (e.g 'us', 'ca', 'gb')
        :param loc: str: find results for a given area (e.g. "new york", "san francisco", "london)
        :return: dict: response from API
        """
        results = {}

        url = self.__generate_url__(
            keyword=keyword, num=num, endpoint="image", *args, **kwargs
        )

        self.logger.debug(f"Performing image async search with {locals()}")
        return await self.__make_request_async__(url=url)

    def product(
        self,
        keyword: str,
        num: int = 10,
        *args,
        **kwargs,
    ) -> dict:
        """
            search for products
            https://www.seoquake.com/blog/google-search-param/ for guidance on params
            https://webapps.stackexchange.com/questions/16047/how-to-restrict-a-google-search-to-results-of-a-specific-language
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :return: dict: response from API
        """
        url = self.__generate_url__(
            keyword=keyword,
            num=num,
            endpoint="product",
            *args,
            **kwargs,
        )
        self.logger.debug(f"Performing product search with {locals()}")
        return self.__make_request__(url=url)

    async def product_async(self, keyword: str, *args, **kwargs) -> dict:
        """
            search for products
            https://www.seoquake.com/blog/google-search-param/ for guidance on params
            https://webapps.stackexchange.com/questions/16047/how-to-restrict-a-google-search-to-results-of-a-specific-language
        :param keyword: str: keywords to search for
        :return: dict: response from API
        """
        results = {}

        url = self.__generate_url__(
            keyword=keyword, endpoint="product", *args, **kwargs
        )

        self.logger.debug(f"Performing product async search with {locals()}")
        return await self.__make_request_async__(url=url)

    def news(
        self, keyword: str, num: int = 10, engine: str = "google", *args, **kwargs
    ) -> dict:
        """
            search for news
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
        url = self.__generate_url__(
            keyword=keyword, num=num, endpoint="news", engine=engine, *args, **kwargs
        )

        self.logger.debug(f"Performing news search with {locals()}")
        return self.__make_request__(url=url)

    async def news_async(
        self, keyword: str, num: int = 10, engine: str = "google", *args, **kwargs
    ) -> dict:
        """
            search for news
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

        url = self.__generate_url__(
            keyword=keyword, num=num, endpoint="news", engine=engine, *args, **kwargs
        )

        self.logger.debug(f"Performing news async search with {locals()}")
        return await self.__make_request_async__(url=url)

    def job(
        self, keyword: str, num: int = 10, engine: str = "google", start: int = 0
    ) -> dict:
        """
            search for jobs
        NOTE: right now job only supports the English interface has to be in US or Canada
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :param engine: str: search engine to use (defaults to google) [google, bing]
        :param start: int: start index for results (defaults to 0)
        :return: dict: response from API
        """
        results = {}
        url = self.__generate_url__(
            keyword=keyword, num=num, endpoint="job", engine=engine, start=start
        )

        self.logger.debug(f"Performing job search with {locals()}")
        return self.__make_request__(url=url)

    async def job_async(
        self, keyword: str, num: int = 10, engine: str = "google", start: int = 0
    ) -> dict:
        """
            search for jobs
        NOTE: right now job only supports the English interface has to be in US or Canada
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :param engine: str: search engine to use (defaults to google) [google, bing]
        :param start: int: start index for results (defaults to 0)
        :return: dict: response from API
        """
        results = {}

        url = self.__generate_url__(
            keyword=keyword, num=num, endpoint="job", engine=engine, start=start
        )

        self.logger.debug(f"Performing job async search with {locals()}")
        return await self.__make_request_async__(url=url)

    def crawl(
        self,
        keyword: str,
        num: int = 10,
        engine: str = "google",
        hl="lang_en",
        gl="us",
        lr="lang_en",
        *args,
        **kwargs,
    ) -> dict:
        """
            perform a search also returning back the HTML for custom parsing
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
        url = self.__generate_url__(
            keyword=keyword,
            num=num,
            engine=engine,
            hl=hl,
            gl=gl,
            lr=lr,
            endpoint="crawl",
            *args,
            **kwargs,
        )
        self.logger.debug(f"Performing crawl with {locals()}")
        return self.__make_request__(url=url)

    async def crawl_async(
        self, keyword: str, num: int = 10, engine: str = "google", *args, **kwargs
    ) -> dict:
        """
            perform a search asynchronously returning back the HTML for custom parsing
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

        url = self.__generate_url__(
            keyword=keyword, num=num, endpoint="crawl", *args, **kwargs
        )

        self.logger.debug(f"Performing async crawl with {locals()}")
        return await self.__make_request_async__(url=url)

    def serp(
        self,
        keyword: str,
        domain: str,
        num: int = 100,
        engine: str = "google",
        hl="lang_en",
        gl="us",
        lr="lang_en",
        *args,
        **kwargs,
    ) -> dict:
        """
            perform a search also returning back the HTML for custom parsing
            https://www.seoquake.com/blog/google-search-param/ for guidance on params
            https://webapps.stackexchange.com/questions/16047/how-to-restrict-a-google-search-to-results-of-a-specific-language
        :param keyword: str: keywords to search for
        :param domain: str: domain to find SERP results for
        :param num: int: number of results to return (max 100)
        :param engine: str: search engine to use (defaults to google) [google, bing]
        :param start: int: start index for results (defaults to 0)
        :param lr: str: language code to use for search (defaults to en)
        :param hl: str: web interface language lang_xx (defaults to lang_en)
        :param cr: str: country code to use countrXX for search (e.g countryUS, countryCA, countryGB)
        :param gl: str: geolocation country code (xx) to perform search (e.g 'us', 'ca', 'gb')
        :param loc: str: find results for a given area (e.g. "new york", "san francisco", "london)
        :return: dict: response from API
        """
        url = self.__generate_url__(
            keyword=keyword,
            domain=domain,
            num=num,
            engine=engine,
            hl=hl,
            gl=gl,
            lr=lr,
            endpoint="serp",
            *args,
            **kwargs,
        )
        self.logger.debug(f"Performing serp with {locals()}")
        return self.__make_request__(url=url)

    async def serp_async(
        self,
        keyword: str,
        domain: str,
        num: int = 100,
        engine: str = "google",
        *args,
        **kwargs,
    ) -> dict:
        """
            perform a search asynchronously returning back the HTML for custom parsing
            https://www.seoquake.com/blog/google-search-param/ for guidance on params
            https://webapps.stackexchange.com/questions/16047/how-to-restrict-a-google-search-to-results-of-a-specific-language
        :param keyword: str: keywords to search for
        :param domain: str: domain to find SERP results for
        :param num: int: number of results to return (max 100)
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

        url = self.__generate_url__(
            keyword=keyword, num=num, domain=domain, endpoint="serp", *args, **kwargs
        )

        self.logger.debug(f"Performing async serp with {locals()}")
        return await self.__make_request_async__(url=url)

    def maps(
        self,
        keyword: str,
        num: int = 10,
        hl="lang_en",
        gl="us",
        lr="lang_en",
        engine="google",
        *args,
        **kwargs,
    ) -> dict:
        """
            search places on Google Maps
        :param keyword: str: keywords to search for, include location for local results
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :param engine: str: search engine to use (defaults to google) [google, bing]
        :param start: int: start index for results (defaults to 0)
        :return: dict: response from API
        """
        results = {}
        url = self.__generate_url__(
            keyword=keyword,
            num=num,
            engine=engine,
            hl=hl,
            gl=gl,
            lr=lr,
            endpoint="maps",
            *args,
            **kwargs,
        )

        self.logger.debug(f"Performing job search with {locals()}")
        return self.__make_request__(url=url)

    async def maps_async(
        self,
        keyword: str,
        num: int = 10,
        hl="lang_en",
        gl="us",
        lr="lang_en",
        engine="google",
        *args,
        **kwargs,
    ) -> dict:
        """
            search places on Google Maps
        :param keyword: str: keywords to search for, include location for local results
        :param num: int: number of results to return (max 100, defaults to 10)
        :param engine: str: search engine to use (defaults to google) [google, bing]
        :param start: int: start index for results (defaults to 0)
        :return: dict: response from API
        """
        results = {}

        url = self.__generate_url__(
            keyword=keyword,
            num=num,
            engine=engine,
            hl=hl,
            gl=gl,
            lr=lr,
            endpoint="maps",
            *args,
            **kwargs,
        )

        self.logger.debug(f"Performing job async search with {locals()}")
        return await self.__make_request_async__(url=url)

    def scholar(
        self,
        keyword: str,
        num: int = 10,
        hl="lang_en",
        gl="us",
        lr="lang_en",
        engine="google",
        *args,
        **kwargs,
    ) -> dict:
        """
            search places on Google scholar
        :param keyword: str: keywords to search for scholar
        :param keyword: str: keywords to search for
        :param num: int: number of results to return (max 100, defaults to 10)
        :param engine: str: search engine to use (defaults to google) [google, bing]
        :param start: int: start index for results (defaults to 0)
        :return: dict: response from API
        """
        results = {}
        url = self.__generate_url__(
            keyword=keyword,
            num=num,
            engine=engine,
            hl=hl,
            gl=gl,
            lr=lr,
            endpoint="scholar",
            *args,
            **kwargs,
        )

        self.logger.debug(f"Performing job search with {locals()}")
        return self.__make_request__(url=url)

    async def scholar_async(
        self,
        keyword: str,
        num: int = 10,
        hl="lang_en",
        gl="us",
        lr="lang_en",
        engine="google",
        *args,
        **kwargs,
    ) -> dict:
        """
            search places on Google scholar
        :param keyword: str: keywords to search for scholar
        :param num: int: number of results to return (max 100, defaults to 10)
        :param engine: str: search engine to use (defaults to google) [google, bing]
        :param start: int: start index for results (defaults to 0)
        :return: dict: response from API
        """
        results = {}

        url = self.__generate_url__(
            keyword=keyword,
            num=num,
            engine=engine,
            hl=hl,
            gl=gl,
            lr=lr,
            endpoint="scholar",
            *args,
            **kwargs,
        )

        self.logger.debug(f"Performing job async search with {locals()}")
        return await self.__make_request_async__(url=url)
