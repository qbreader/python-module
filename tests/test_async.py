"""Test the asynchronous API functions. This module specifically tests API interaction,
not the underlying data structures. See tests/test_types.py for that."""

import asyncio
from random import random
from typing import Any

import pytest
import pytest_asyncio

import qbreader as qbr
from qbreader import Async
from tests import async_assert_exception, check_internet_connection


@pytest.fixture(scope="module")
def event_loop():
    """Rescope the event loop to the module."""
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(autouse=True)
async def async_code_is_too_fast_lol():
    """Sleep for up to 0.1 seconds during each test to avoid getting rate limited."""
    await asyncio.sleep(random() / 10)


class TestAsync:
    """Test asynchronous API functions."""

    @pytest_asyncio.fixture(scope="class")
    async def qb(self):
        """Create an Async instance shared by all tests."""
        return await Async.create()

    @pytest.fixture()
    def mock_get(self, monkeypatch, qb):
        """Mock aiohttp.ClientSession.get for Async.session"""

        def _set_get(mock_status_code: int = 200, mock_json=None, *args, **kwargs):
            class MockResponse:
                def __init__(self):
                    self.status = mock_status_code

                async def __aenter__(self):
                    return self

                async def __aexit__(self, exc_type, exc_val, exc_tb):
                    pass

                async def json(self):
                    return mock_json

            monkeypatch.setattr(
                qb.session, "get", lambda *args, **kwargs: MockResponse()
            )

        return _set_get

    def test_internet(self):
        """Test that there is an internet connection."""
        assert check_internet_connection(), "No internet connection"

    @pytest.mark.asyncio
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
    async def test_query(self, qb, params: dict[str, Any], expected_answer: str):
        query: qbr.QueryResponse = await qb.query(**params)
        judgement: qbr.AnswerJudgement
        if params["questionType"] == "tossup":
            judgement = await query.tossups[0].check_answer_async(
                expected_answer, session=qb.session
            )
            assert judgement.correct()
        elif params["questionType"] == "bonus":
            judgement = await query.bonuses[0].check_answer_async(
                0, expected_answer, session=qb.session
            )
            assert judgement.correct()

    @pytest.mark.asyncio
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
    async def test_query_exception(
        self, qb, params: dict[str, Any], exception: Exception
    ):
        await async_assert_exception(qb.query, exception, **params)

    @pytest.mark.asyncio
    async def test_query_bad_response(self, qb, mock_get):
        mock_get(mock_status_code=404)
        await async_assert_exception(qb.query, Exception)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("number", [1, 20, 50, 100])
    async def test_random_tossup(self, qb, number: int):
        assert len(await qb.random_tossup(number=number)) == number

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "number, exception",
        [(0, ValueError), (-1, ValueError), ("1", TypeError), (1.0, TypeError)],
    )
    async def test_random_tossup_exception(self, qb, number: int, exception: Exception):
        await async_assert_exception(qb.random_tossup, exception, number=number)

    @pytest.mark.asyncio
    async def test_random_tossup_bad_response(self, qb, mock_get):
        mock_get(mock_status_code=404)
        await async_assert_exception(qb.random_tossup, Exception)

    @pytest.mark.asyncio
    @pytest.mark.parametrize("number", [1, 20, 50, 100])
    async def test_random_bonus(self, qb, number: int):
        assert len(await qb.random_bonus(number=number)) == number

    @pytest.mark.asyncio
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
    async def test_random_bonus_exception(
        self, qb, number: int, three_part: bool, exception: Exception
    ):
        await async_assert_exception(
            qb.random_bonus, exception, number=number, three_part_bonuses=three_part
        )

    @pytest.mark.asyncio
    async def test_random_bonus_bad_response(self, qb, mock_get):
        mock_get(mock_status_code=404)
        await async_assert_exception(qb.random_bonus, Exception)

    @pytest.mark.asyncio
    async def test_random_name(self, qb):
        assert await qb.random_name()

    @pytest.mark.asyncio
    async def test_random_name_bad_response(self, qb, mock_get):
        mock_get(mock_status_code=404)
        await async_assert_exception(qb.random_name, Exception)

    @pytest.mark.asyncio
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
    async def test_packet(
        self, qb, params: dict[str, Any], question: int, expected_answer: str
    ):
        packet: qbr.Packet = await qb.packet(**params)
        judgement: qbr.AnswerJudgement = await packet.tossups[
            question - 1
        ].check_answer_async(expected_answer, session=qb.session)
        assert judgement.correct()

    @pytest.mark.asyncio
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
    async def test_packet_exception(
        self, qb, params: dict[str, Any], exception: Exception
    ):
        await async_assert_exception(qb.packet, exception, **params)

    @pytest.mark.asyncio
    async def test_packet_bad_response(self, qb, monkeypatch, mock_get):
        mock_get(mock_status_code=404)

        async def mock_num_packets(x):
            return 21

        monkeypatch.setattr(
            qb, "num_packets", mock_num_packets
        )  # mocking get requests breaks num_packets
        await async_assert_exception(
            qb.packet, Exception, setName="2023 PACE NSC", packetNumber=1
        )

    @pytest.mark.asyncio
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
    async def test_packet_tossups(
        self, qb, params: dict[str, Any], question: int, expected_answer: str
    ):
        tus = await qb.packet_tossups(**params)
        judgement: qbr.AnswerJudgement = await tus[question - 1].check_answer_async(
            expected_answer, session=qb.session
        )
        assert judgement.correct()

    @pytest.mark.asyncio
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
    async def test_packet_tossups_exception(
        self, qb, params: dict[str, Any], exception: Exception
    ):
        await async_assert_exception(qb.packet_tossups, exception, **params)

    @pytest.mark.asyncio
    async def test_packet_tossups_bad_response(self, qb, monkeypatch, mock_get):
        mock_get(mock_status_code=404)

        async def mock_num_packets(x):
            return 21

        monkeypatch.setattr(
            qb, "num_packets", mock_num_packets
        )  # mocking get requests breaks num_packets
        await async_assert_exception(
            qb.packet_tossups, Exception, setName="2023 PACE NSC", packetNumber=1
        )

    @pytest.mark.asyncio
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
    async def test_packet_bonuses(
        self, qb, params: dict[str, Any], question: int, expected_answer: str
    ):
        bs = await qb.packet_bonuses(**params)
        judgement: qbr.AnswerJudgement = await bs[question - 1].check_answer_async(
            0, expected_answer, session=qb.session
        )
        assert judgement.correct()

    @pytest.mark.asyncio
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
    async def test_packet_bonuses_exception(
        self, qb, params: dict[str, Any], exception: Exception
    ):
        await async_assert_exception(qb.packet_bonuses, exception, **params)

    @pytest.mark.asyncio
    async def test_packet_bonuses_bad_response(self, qb, monkeypatch, mock_get):
        mock_get(mock_status_code=404)

        async def mock_num_packets(x):
            return 21

        monkeypatch.setattr(
            qb, "num_packets", mock_num_packets
        )  # mocking get requests breaks num_packets
        await async_assert_exception(
            qb.packet_bonuses, Exception, setName="2023 PACE NSC", packetNumber=1
        )

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "setName, expected",
        [("2023 PACE NSC", 21), ("2022 SHOW-ME", 15)],
    )
    async def test_num_packets(self, qb, setName: str, expected: int):
        assert await qb.num_packets(setName) == expected

    @pytest.mark.asyncio
    async def test_num_packets_bad_response(self, qb, mock_get):
        await async_assert_exception(
            qb.num_packets, ValueError, setName="not a set name"
        )
        mock_get(mock_status_code=400)
        await async_assert_exception(qb.num_packets, Exception, setName="2023 PACE NSC")

    @pytest.mark.asyncio
    async def test_set_list(self, qb):
        assert await qb.set_list()

    @pytest.mark.asyncio
    async def test_set_list_bad_response(self, qb, mock_get):
        mock_get(mock_status_code=404)
        await async_assert_exception(qb.set_list, Exception)

    @pytest.mark.asyncio
    async def test_room_list(self, qb):
        assert await qb.room_list()

    @pytest.mark.asyncio
    async def test_room_list_bad_response(self, qb, mock_get):
        mock_get(mock_status_code=404)
        await async_assert_exception(qb.room_list, Exception)

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "answerline, givenAnswer",
        [("Rubik's cubes [prompt on cubes and speedcubing]", "Rubik's cubes")],
    )
    async def test_check_answer(self, qb, answerline: str, givenAnswer: str):
        judgement: qbr.AnswerJudgement = await qb.check_answer(
            answerline=answerline, givenAnswer=givenAnswer
        )
        assert judgement.correct()
        judgement = await qbr.AnswerJudgement.check_answer_async(
            answerline=answerline, givenAnswer=givenAnswer
        )  # testing no session provided
        assert judgement.correct()

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        "answerline, givenAnswer, exception",
        [
            ("Rubik's cubes [prompt on cubes and speedcubing]", 1, TypeError),
            (1, "Rubik's cubes", TypeError),
        ],
    )
    async def test_check_answer_exception(
        self, qb, answerline: str, givenAnswer: str, exception: Exception
    ):
        await async_assert_exception(
            qb.check_answer, exception, answerline, givenAnswer
        )
        await async_assert_exception(
            qbr.AnswerJudgement.check_answer_async, exception, answerline, givenAnswer
        )

    @pytest.mark.asyncio
    async def test_check_answer_bad_response(self, qb, mock_get):
        mock_get(mock_status_code=404)
        await async_assert_exception(
            qb.check_answer,
            Exception,
            answerline="Rubik's cubes",
            givenAnswer="Rubik's cubes",
        )

    @pytest.mark.asyncio
    async def test_close(self, qb):
        await qb.close()
        assert qb.session.closed

    @pytest.mark.asyncio
    async def test_async_with(self):
        qb = await Async.create()
        async with qb:
            assert qb.session
        assert qb.session.closed
