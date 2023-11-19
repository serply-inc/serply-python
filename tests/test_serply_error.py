import pytest
import os
import logging
from serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_unsported_endpoint_job_url():
    with pytest.raises(ValueError) as e:
        serply.__generate_url__(keyword="nurse practitioner", endpoint="asdf")
        logging.error(e)

