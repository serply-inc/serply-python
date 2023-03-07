import os
import unittest
import pytest
import asyncio
import langid
from serply.serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_job_url():
    url = serply.__generate_url__(keyword="nurse practitioner", endpoint="job")
    assert url == "https://api.serply.io/v1/job/search/q=nurse+practitioner&num=10"


def test_generate_simple_job_url_num_100():
    url = serply.__generate_url__(keyword="nurse practitioner", endpoint="job", num=100)
    assert url == "https://api.serply.io/v1/job/search/q=nurse+practitioner&num=100"


def test_generate_job_url_start():
    url = serply.__generate_url__(keyword="nurse practitioner", endpoint="job", start=33)
    assert url == "https://api.serply.io/v1/job/search/q=nurse+practitioner&num=10&start=33"


def test_generate_job_url_start_gl():
    url = serply.__generate_url__(keyword="nurse practitioner", endpoint="job", start=33, gl="de")
    assert url == "https://api.serply.io/v1/job/search/q=nurse+practitioner&num=10&start=33&gl=de"


def test_simple_job_default():
    results = serply.job(keyword="real estate agent")
    assert "jobs" in results
    assert results['jobs']
    for job in results['jobs']:
        assert "link" in job


def test_simple_job_in_spanish():
    results = serply.job(keyword="nurse practitioner", hl="lang_es", gl="es")
    assert "jobs" in results
    assert results['jobs']
    # expect first source to include "es" in the url and title to be in spanish
    detected_language, confidence = langid.classify(
        results["jobs"][0]["title"].encode("utf-8")
    )
    assert detected_language == "es"


def test_simple_job_in_interface_german():
    results = serply.job(keyword="data analyst", hl="lang_de", gl="de")
    assert "jobs" in results
    assert results['jobs']
    # expect first source to include "es" in the url and title to be in spanish
    detected_language, confidence = langid.classify(
        results["jobs"][0]["title"].encode("utf-8")
    )
    assert detected_language == "de"


# test async versions
def test_simple_job_default_async():
    results = asyncio.run(serply.job_async(keyword="accountant"))
    assert "jobs" in results
    assert results['jobs']
    for job in results['jobs']:
        assert "link" in job

def test_simple_job_in_spanish_async():
    results = asyncio.run(
        serply.job_async(keyword="nurse practitioner", hl="lang_es", gl="es")
    )
    assert "jobs" in results
    assert results['jobs']
    for job in results['jobs']:
        assert "link" in job

    # expect first source to include "es" in the url and title to be in spanish
    detected_language, confidence = langid.classify(
        " ".jon(results["jobs"][0]["highlights"]).encode("utf-8")
    )
    assert detected_language == "es"


def test_simple_job_in_interface_german_async():
    results = asyncio.run(
        serply.job_async(keyword="data scientist", hl="lang_de", gl="de")
    )
    assert "jobs" in results
    assert results['jobs']
    for job in results['jobs']:
        assert "link" in job
    # expect first source to include "es" in the url and title to be in spanish
    detected_language, confidence = langid.classify(
        " ".jon(results["jobs"][0]["highlights"]).encode("utf-8")
    )
    assert detected_language == "de"
