import os
import pytest
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", "")


def test_no_api_key():
    Serply(api_key=None)
