"""Synchronous API functions."""

from typing import Optional, Type, Union

import requests

import qbreader.api_utils as api_utils
from qbreader.api_utils import BASE_URL
from qbreader.types import (
    Bonus,
    Category,
    Difficulty,
    QuestionType,
    SearchType,
    Subcategory,
    Tossup,
    UnnormalizedCategory,
    UnnormalizedDifficulty,
    UnnormalizedSubcategory,
)


def query(
    questionType: QuestionType = "all",
    searchType: SearchType = "all",
    queryString: Optional[str] = "",
    exactPhrase: Optional[bool] = False,
    ignoreDiacritics: Optional[bool] = False,
    regex: Optional[bool] = False,
    randomize: Optional[bool] = False,
    setName: Optional[str] = None,
    difficulties: UnnormalizedDifficulty = None,
    categories: UnnormalizedCategory = None,
    subcategories: UnnormalizedSubcategory = None,
    maxReturnLength: Optional[int] = 25,
    tossupPagination: Optional[int] = 1,
    bonusPagination: Optional[int] = 1,
) -> dict:
    """
    Query the qbreader database for questions.

    Original API doc at https://www.qbreader.org/api-docs/query.

    Parameters
    ----------
    questionType : qbreader.types.QuestionType
        The type of question to search for. Can be either a string or a question class
        type.
    searchType : qbreader.types.SearchType
        Where to search for the query string. Can only be a string.
    queryString : str, optional
        The string to search for.
    exactPhrase : bool, default = False
        Ensure that the query string is an exact phrase.
    ignoreDiacritics : bool, default = False
        Ignore or transliterate diacritical marks in `queryString`.
    regex : bool, default = False
        Treat `queryString` as a regular expression.
    randomize : bool, default = False
        Randomize the order of the returned questions.
    setName : str, optional
        The name of the set to search in.
    difficulties : qbreader.types.UnnormalizedDifficulty, optional
        The difficulties to search for. Can be a single or an array of `Difficulty`
        enums, strings, or integers.
    categories : qbreader.types.UnnormalizedCategory, optional
        The categories to search for. Can be a single or an array of `Category` enums or
        strings.
    subcategories : qbreader.types.UnnormalizedSubcategory, optional
        The subcategories to search for. Can be a single or an array of `Subcategory`
        enums or strings. The API does not check for consistency between categories and
        subcategories.
    maxReturnLength : int, default = 25
        The maximum number of questions to return.
    tossupPagination : int, default = 1
        The page of tossups to return.
    bonusPagination : int, default = 1
        The page of bonuses to return.


    """
    # normalize parameters
    if questionType == Tossup:
        questionType = "tossup"
    elif questionType == Bonus:
        questionType = "bonus"
    if questionType not in ["tossup", "bonus", "all"]:
        raise ValueError("questionType must be either 'tossup', 'bonus', or 'all'.")

    if searchType not in ["question", "answer", "all"]:
        raise ValueError("searchType must be either 'question', 'answer', or 'all'.")

    if not isinstance(queryString, str):
        raise TypeError(
            f"queryString must be a string, not {type(queryString).__name__}."
        )

    for name, param in tuple(
        zip(
            ("exactPhrase", "ignoreDiacritics", "regex", "randomize"),
            (exactPhrase, ignoreDiacritics, regex, randomize),
        )
    ):
        if not isinstance(param, bool):
            raise TypeError(f"{name} must be a boolean, not {type(param).__name__}.")

    if setName is not None and not isinstance(setName, str):
        raise TypeError(f"setName must be a string, not {type(setName).__name__}.")

    for name, param in tuple(
        zip(
            ("maxReturnLength", "tossupPagination", "bonusPagination"),
            (maxReturnLength, tossupPagination, bonusPagination),
        )
    ):
        if not isinstance(param, int):
            raise TypeError(f"{name} must be an integer, not {type(param).__name__}.")
        elif param < 1:
            raise ValueError(f"{name} must be at least 1.")

    url = BASE_URL + "/query"

    data = {
        "questionType": questionType,
        "searchType": searchType,
        "queryString": queryString,
        "exactPhrase": api_utils.normalize_bool(exactPhrase),
        "ignoreDiacritics": api_utils.normalize_bool(ignoreDiacritics),
        "regex": api_utils.normalize_bool(regex),
        "randomize": api_utils.normalize_bool(randomize),
        "setName": setName,
        "difficulties": api_utils.normalize_diff(difficulties),
        "categories": api_utils.normalize_cat(categories),
        "subcategories": api_utils.normalize_subcat(subcategories),
        "maxReturnLength": maxReturnLength,
        "tossupPagination": tossupPagination,
        "bonusPagination": bonusPagination,
    }

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(str(response.status_code) + " bad request")


def random_question(
    questionType: str,
    difficulties: dict = [],
    categories: list = [],
    subcategories: list = [],
    number: int = 1,
) -> list:
    """
    Get a random question from the QBreader database.

    This function gets a random question from the QBreader database.

    Parameters
    ----------
    questionType : str, must be one of "tossup" or "bonus"
        The type of question to search for (tossup or bonus or both). If one of the two is not set, returns a 400 Bad Request.
    difficulties : list (optional)
        The difficulties to search for. Defaults to []. Leave as an empty list to search all. Must be a list of ints from 1 to 10.
    categories : list (optional)
        The categories to search for. Defaults to []. Leave as an empty list to search all.
    subcategories : list (optional)
        The subcategories to search for. Defaults to []. Leave as an empty list to search all.
    number : int (optional)
        The number of questions to return. Defaults to None. Leave blank to return 1.

    Returns
    ----------
    list
        A list containing the results of the search.

    """
    url = BASE_URL + f"/random-{questionType}"

    data = {
        "categories": categories,
        "subcategories": subcategories,
        "difficulties": difficulties,
        "number": number,
    }

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(str(response.status_code) + " bad request")


def random_name() -> str:
    """
    Get a random name from the QBreader database.

    This function Generates an adjective-noun pair (used in multiplayer lobbies).

    Takes no parameters.

    Returns
    ----------
    str
        A string containing the random name.

    """
    url = BASE_URL + "/random-name"
    response = requests.get(url)

    if response.status_code == 200:
        return response.text
    else:
        raise Exception(str(response.status_code) + " bad request")


def packet(setName: str, packetNumber: int) -> dict:
    """
    Get a packet from the QBreader database.

    This function gets questions from a packet from the QBreader database.

    Parameters
    ----------
    setName : str
        The name of the set to search. Can be obtained from set_list().
    packetNumber : int
        The number of the packet to search for.

    Returns
    ----------
    dict
        A dictionary containing the results of the search.
    """
    url = BASE_URL + "/packet"
    data = {"setName": setName, "packetNumber": packetNumber}

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(str(response.status_code) + " bad request")


def packet_tossups(setName: str, packetNumber: int) -> dict:
    """
    Get a packet's tossups from the QBreader database.

    This function gets a packet's tossups from the QBreader database. Twice as fast as using packet().

    Parameters
    ----------
    setName : str
        The name of the set to search. Can be obtained from set_list().
    packetNumber : int
        The number of the packet to search for.

    Returns
    ----------
    dict
        A dictionary containing the results of the search.

    """

    url = BASE_URL + "/packet-tossups"
    data = {"setName": setName, "packetNumber": packetNumber}

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(str(response.status_code) + " bad request")


def packet_bonuses(setName: str, packetNumber: int) -> dict:
    """
    Get a packet's bonuses from the QBreader database.

    This function gets a packet's bonuses from the QBreader database. Twice as fast as using packet().

    Parameters
    ----------
    setName : str
        The name of the set to search. Can be obtained from set_list().
    packetNumber : int
        The number of the packet to search for.

    Returns
    ----------
    dict
        A dictionary containing the results of the search.

    """
    url = BASE_URL + "/packet-bonuses"
    data = {"setName": setName, "packetNumber": packetNumber}

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(str(response.status_code) + " bad request")


def num_packets(setName: str) -> dict:
    """
    Get the number of packets in a set from the QBreader database.

    This function gets the number of packets in a set from the QBreader database.

    Parameters
    ----------
    setName : str
        The name of the set to search. Can be obtained from set_list().

    Returns
    ----------
    dict
        A dictionary containing the results of the search.
    """
    url = BASE_URL + "/num-packets"
    data = {
        "setName": setName,
    }

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(str(response.status_code) + " bad request")


def set_list() -> list:
    """
    Get a list of sets from the QBreader database.

    This function gets a list of sets from the QBreader database.

    Takes no parameters.

    Returns
    ----------
    list
        A list containing the results of the search.
    """
    url = BASE_URL + "/set-list"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(str(response.status_code) + " bad request")


def room_list() -> dict:
    """
    Get a list of rooms from the QBreader database.

    This function gets a list of rooms from the QBreader database.

    Takes no parameters.

    Returns
    ----------
    dict
        A dictionary containing the results of the search.
    """
    url = BASE_URL + "/multiplayer/room-list"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(str(response.status_code) + " bad request")


def report_question(_id: str, reason: str = None, description: str = None) -> int:
    """
    Report a question from the QBreader database.

    This function reports a question from the QBreader database.

    Parameters
    ----------
    _id : str
        The ID of the question to report.
    reason : str (optional)
        The reason for reporting the question. Defaults to None.
    description : str (optional)
        A description of the reason for reporting the question. Defaults to None.

    Returns
    ----------
    int
        The status code of the request. 200 if successful, 400 if not.
    """
    url = BASE_URL + "/random-question"

    data = {"_id": _id, "reason": reason, "description": description}

    response = requests.post(url, json=data)

    return response.status_code


def check_answer(answerline: str, givenAnswer: str) -> list:
    """
    Check an answer against an answer line.

    This function checks an answer against an answer line.

    Parameters
    ----------
    answerline : str
        The answer line to check against.
    givenAnswer : str
        The answer to check.

    Returns
    ----------
    list
        A list containing the results of the check.
    """
    url = BASE_URL + "/check-answer"

    data = {"answerline": answerline, "givenAnswer": givenAnswer}

    response = requests.get(url, params=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(str(response.status_code) + " bad request")
