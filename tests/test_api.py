#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (C) 2020-2021 Stɑrry Shivɑm.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
"""Includes unittests for public API endpoints."""


import pytest
import requests as r


BASE_URL = "https://superhero-quotes.herokuapp.com"


@pytest.mark.parametrize(
    ["banner", "expected_banner", "total"],
    [
        ("mcu", "Marvel Cinematic Universe (MCU)", 5),
        ("dcu", "DC Universe (DCU)", 10),
    ],
)
def test_grab_endpoint(banner, expected_banner, total):
    # make request to the API
    res = r.get(f"{BASE_URL}/grab?banner={banner}&size={total}")
    # check status code
    assert res.status_code == 200
    # check total quotes
    json_data = res.json()
    assert json_data["TotalQuotes"] == total
    assert len(json_data["Items"]) == total
    # finally check banner
    assert json_data["Banner"] == expected_banner


def test_default_grab_endpoint_size():
    # make request to the API without passing size parameter
    banners = ["dcu", "mcu"]
    for b in banners:
        res = r.get(f"{BASE_URL}/grab?banner={b}")
        # by default it should return 10 quotes
        assert res.json()["TotalQuotes"] == 10
        assert len(res.json()["Items"]) == 10


def test_invalid_grab_banner():
    # make request to API by passing 'pizza' in banner parameter
    res = r.get(f"{BASE_URL}/grab?banner=pizza")
    # status 404: not found
    assert res.status_code == 404
    assert res.json()["message"].startswith("Not found")


def test_random_endpoint():
    # make request to /random endpoint.
    res = r.get(f"{BASE_URL}/random")
    # check status code
    assert res.status_code == 200
    json_data = res.json()
    assert json_data["Banner"] in {
        "DC Universe (DCU)",
        "Marvel Cinematic Universe (MCU)",
    }


def test_quoteid_endpoint():
    # make request with specific quoteId
    quote_id = "k3fhzAKsvCeuFhXPHPQcnT"
    res = r.get(f"{BASE_URL}/quoteId/{quote_id}")
    # check status code
    assert res.status_code == 200
    json_data = res.json()
    # check if id & quote matches
    quote_text = "The pen, is truly mightier than the sword! "
    assert json_data["Stuff"]["id"] == quote_id
    assert json_data["Stuff"]["data"]["quote"] == quote_text


def test_invalid_quoteid():
    # make request with invalid quoteid
    invalid_id = "1234abcd"
    res = r.get(f"{BASE_URL}/quoteId/{invalid_id}")
    # status 404: not found
    assert res.status_code == 404
    # check error message
    err_msg = "Can't find any quote for this id."
    assert res.json()["message"] == err_msg
