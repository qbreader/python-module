"""Test the synchronous API functions. This module specifically tests API interaction,
not the underlying data structures. See tests/test_types.py for that."""

from typing import Any

import pytest
import requests

import qbreader as qbr
from qbreader import Sync as qb
from tests import assert_exception, check_internet_connection


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

    @pytest.mark.parametrize("number", [1, 50, 100, 37])
    def test_random_tossup(self, number: int):
        assert len(qb.random_tossup(number=number)) == number

    @pytest.mark.parametrize(
        "number, exception",
        [(0, ValueError), (-1, ValueError), ("1", TypeError), (1.0, TypeError)],
    )
    def test_random_tossup_exception(self, number: int, exception: Exception):
        assert_exception(qb.random_tossup, exception, number=number)

    def test_random_tossup_bad_response(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=404))
        assert_exception(qb.random_tossup, Exception)

    @pytest.mark.parametrize("number", [1, 50, 100, 37])
    def test_random_bonus(self, number: int):
        assert len(qb.random_bonus(number=number)) == number

    @pytest.mark.parametrize(
        "number, three_part, exception",
        [
            (0, False, ValueError),
            (-1, False, ValueError),
            ("1", False, TypeError),
            (1.0, False, TypeError),
            (1, "not a bool", TypeError),
        ],
    )
    def test_random_bonus_exception(
        self, number: int, three_part: bool, exception: Exception
    ):
        assert_exception(
            qb.random_bonus, exception, number=number, three_part_bonuses=three_part
        )

    def test_random_bonus_bad_response(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=404))
        assert_exception(qb.random_bonus, Exception)

    def test_random_name(self):
        assert qb.random_name()

    def test_random_name_bad_response(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=404))
        assert_exception(qb.random_name, Exception)

    @pytest.mark.parametrize(
        "params, question, expected_answer",
        [
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": 1,
                },
                5,
                "negative",
            ),
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": 4,
                },
                16,
                "spin",
            ),
        ],
    )
    def test_packet(self, params: dict[str, Any], question: int, expected_answer: str):
        packet: qbr.Packet = qb.packet(**params)
        assert packet.tossups[question - 1].check_answer_sync(expected_answer).correct()

    @pytest.mark.parametrize(
        "params, exception",
        [
            (
                {
                    "setName": 1,
                    "packetNumber": 1,
                },
                TypeError,
            ),
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": "not an int",
                },
                TypeError,
            ),
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": 0,
                },
                ValueError,
            ),
        ],
    )
    def test_packet_exception(self, params: dict[str, Any], exception: Exception):
        assert_exception(qb.packet, exception, **params)

    def test_packet_bad_response(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=404))
        monkeypatch.setattr(
            qb, "num_packets", lambda x: 21
        )  # mocking get requests breaks num_packets
        assert_exception(qb.packet, Exception, setName="2023 PACE NSC", packetNumber=1)

    @pytest.mark.parametrize(
        "params, question, expected_answer",
        [
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": 1,
                },
                5,
                "negative",
            ),
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": 4,
                },
                16,
                "spin",
            ),
        ],
    )
    def test_packet_tossups(
        self, params: dict[str, Any], question: int, expected_answer: str
    ):
        tus = qb.packet_tossups(**params)
        assert tus[question - 1].check_answer_sync(expected_answer).correct()

    @pytest.mark.parametrize(
        "params, exception",
        [
            (
                {
                    "setName": 1,
                    "packetNumber": 1,
                },
                TypeError,
            ),
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": "not an int",
                },
                TypeError,
            ),
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": 0,
                },
                ValueError,
            ),
        ],
    )
    def test_packet_tossups_exception(
        self, params: dict[str, Any], exception: Exception
    ):
        assert_exception(qb.packet_tossups, exception, **params)

    def test_packet_tossups_bad_response(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=404))
        monkeypatch.setattr(
            qb, "num_packets", lambda x: 21
        )  # mocking get requests breaks num_packets
        assert_exception(
            qb.packet_tossups, Exception, setName="2023 PACE NSC", packetNumber=1
        )

    @pytest.mark.parametrize(
        "params, question, expected_answer",
        [
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": 1,
                },
                5,
                "church",
            ),
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": 4,
                },
                16,
                "bananafish",
            ),
        ],
    )
    def test_packet_bonuses(
        self, params: dict[str, Any], question: int, expected_answer: str
    ):
        bs = qb.packet_bonuses(**params)
        assert bs[question - 1].check_answer_sync(0, expected_answer).correct()

    @pytest.mark.parametrize(
        "params, exception",
        [
            (
                {
                    "setName": 1,
                    "packetNumber": 1,
                },
                TypeError,
            ),
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": "not an int",
                },
                TypeError,
            ),
            (
                {
                    "setName": "2023 PACE NSC",
                    "packetNumber": 0,
                },
                ValueError,
            ),
        ],
    )
    def test_packet_bonuses_exception(
        self, params: dict[str, Any], exception: Exception
    ):
        assert_exception(qb.packet_bonuses, exception, **params)

    def test_packet_bonuses_bad_response(self, monkeypatch):
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=404))
        monkeypatch.setattr(
            qb, "num_packets", lambda x: 21
        )  # mocking get requests breaks num_packets
        assert_exception(
            qb.packet_bonuses, Exception, setName="2023 PACE NSC", packetNumber=1
        )

    @pytest.mark.parametrize(
        "setName, expected",
        [("2023 PACE NSC", 21), ("2022 SHOW-ME", 15)],
    )
    def test_num_packets(self, setName: str, expected: int):
        assert qb.num_packets(setName) == expected

    def test_num_packets_bad_response(self, monkeypatch):
        assert_exception(qb.num_packets, ValueError, setName="not a set name")
        monkeypatch.setattr(requests, "get", self.mock_get(mock_status_code=400))
        assert_exception(qb.num_packets, Exception, setName="2023 PACE NSC")

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

    @pytest.mark.parametrize(
        "answerline, givenAnswer",
        [("Rubik's cubes [prompt on cubes and speedcubing]", "Rubik's cubes")],
    )
    def test_check_answer(self, answerline: str, givenAnswer: str):
        assert qb.check_answer(answerline=answerline, givenAnswer=givenAnswer).correct()
