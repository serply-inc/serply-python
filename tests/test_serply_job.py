import os
import asyncio
from serply import Serply

API_KEY = os.getenv("API_KEY", None)

serply = Serply(api_key=API_KEY)


def test_generate_simple_job_url():
    url = serply.__generate_url__(keyword="nurse practitioner", endpoint="job")
    assert url == "https://api.serply.io/v1/job/search/q=nurse+practitioner&num=10"


def test_generate_simple_job_url_num_100():
    url = serply.__generate_url__(keyword="nurse practitioner", endpoint="job", num=100)
    assert url == "https://api.serply.io/v1/job/search/q=nurse+practitioner&num=100"


def test_generate_job_url_start():
    url = serply.__generate_url__(
        keyword="nurse practitioner", endpoint="job", start=33
    )
    assert (
        url
        == "https://api.serply.io/v1/job/search/q=nurse+practitioner&num=10&start=33"
    )


def test_generate_job_url_start_gl():
    url = serply.__generate_url__(
        keyword="nurse practitioner", endpoint="job", start=33, gl="de"
    )
    assert (
        url
        == "https://api.serply.io/v1/job/search/q=nurse+practitioner&num=10&start=33&gl=de"
    )


def test_simple_job_default():
    results = serply.job(keyword="real estate agent")
    assert "jobs" in results
    assert results["jobs"]
    for job in results["jobs"]:
        assert "link" in job


def test_simple_job_in_spanish():
    results = serply.job(keyword="nurse practitioner")
    assert "jobs" in results
    assert results["jobs"]
    for job in results["jobs"]:
        assert "link" in job
    # right now the interface has to be english and in US or Canada


def test_simple_job_in_interface_german():
    results = serply.job(keyword="data analyst")
    assert "jobs" in results
    assert results["jobs"]
    for job in results["jobs"]:
        assert "link" in job
    # right now the interface has to be english and in US or Canada


# test async versions
def test_simple_job_default_async():
    results = asyncio.run(serply.job_async(keyword="accountant"))
    assert "jobs" in results
    assert results["jobs"]
    for job in results["jobs"]:
        assert "link" in job


def test_loan_officer_job():
    results = asyncio.run(serply.job_async(keyword="loan officers"))
    assert "jobs" in results
    assert results["jobs"]
    for job in results["jobs"]:
        assert "link" in job
    # right now the interface has to be english and in US or Canada


def test_data_scientist_job():
    results = asyncio.run(serply.job_async(keyword="data scientist"))
    assert "jobs" in results
    assert results["jobs"]
    for job in results["jobs"]:
        assert "link" in job
    # right now the interface has to be english and in US or Canada
