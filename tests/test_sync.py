"""Test the synchronous API functions. This module specifically tests API interaction,
not the underlying data structures. See tests/test_types.py for that."""

from qbreader import Sync as qb
import qbreader as qbr
from typing import Any
from tests import check_internet_connection, assert_exception
import pytest
import requests


class TestSync:
    """Test synchronous API functions."""

    def mock_get(self, mock_status_code: int = 200, mock_json=None):
        """Mock the requests.get function."""

        def get(*args, **kwargs):
            class MockResponse:
                def __init__(self):
                    self.status_code = mock_status_code

                def json(self):
                    return mock_json

            return MockResponse()

        return get

    def test_internet(self):
        """Test that there is an internet connection."""
        assert check_internet_connection(), "No internet connection"

    @pytest.mark.parametrize(
        "params, expected_answer",
        [
            (
                {
                    "questionType": "tossup",
                    "setName": "2023 PACE NSC",
                    "queryString": "hashes",
                },
                "password",
            ),
            (
                {
                    "questionType": qbr.Tossup,
                    "setName": "2023 PACE NSC",
                    "queryString": "hashes",
                },
                "password",
            ),
            (
                {
                    "questionType": "bonus",
                    "setName": "2023 PACE NSC",
                    "queryString": "bell labs",
                },
                "C",
            ),
            (
                {
                    "questionType": qbr.Bonus,
                    "setName": "2023 PACE NSC",
                    "queryString": "bell labs",
                },
                "C",
            ),
        ],
    )
    def test_query(self, params: dict[str, Any], expected_answer: str):
        query: qbr.QueryResponse = qb.query(**params)
        if params["questionType"] == "tossup":
            assert query.tossups[0].check_answer_sync(expected_answer).correct()
        elif params["questionType"] == "bonus":
            assert query.bonuses[0].check_answer_sync(0, expected_answer).correct()

    @pytest.mark.parametrize(
        "params, exception",
        [
            (
                {
                    "questionType": "no a valid question type",
                },
                ValueError,
            ),
            (
                {
                    "searchType": "not a valid search type",
                },
                ValueError,
            ),
            (
                {
                    "queryString": 1,
                },
                TypeError,
            ),
            (
                {
                    "regex": "str not bool",
                },
                TypeError,
            ),
            (
                {
                    "setName": 1,
                },
                TypeError,
            ),
            (
                {
                    "maxReturnLength": "str not int",
                },
                TypeError,
            ),
            (
                {
                    "maxReturnLength": -1,
                },
                ValueError,
            ),
        ],
    )
    def test_query_exception(self, params: dict[str, Any], exception: Exception):
        assert_exception(qb.query, exception, **params)

    def test_query_bad_response(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=404))
        assert_exception(qb.query, Exception)

    def test_random_name(self):
        assert qb.random_name()

    def test_random_name_bad_response(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=404))
        assert_exception(qb.random_name, Exception)

    def test_set_list(self):
        assert qb.set_list()

    def test_set_list_bad_response(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=404))
        assert_exception(qb.set_list, Exception)

    def test_room_list(self):
        assert qb.room_list()

    def test_room_list_bad_response(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=404))
        assert_exception(qb.room_list, Exception)
