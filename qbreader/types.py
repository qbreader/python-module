"""Types and classes used by the library."""

from __future__ import annotations

import enum
from collections.abc import Iterable, Sequence
from typing import Any, Literal, Optional, Self, Type, TypeAlias, Union

import aiohttp
import requests

from qbreader._consts import BASE_URL


class Category(enum.StrEnum):
    """Question category enum."""

    LITERATURE = "Literature"
    HISTORY = "History"
    SCIENCE = "Science"
    FINE_ARTS = "Fine Arts"
    RELIGION = "Religion"
    MYTHOLOGY = "Mythology"
    PHILOSOPHY = "Philosophy"
    SOCIAL_SCIENCE = "Social Science"
    CURRENT_EVENTS = "Current Events"
    GEOGRAPHY = "Geography"
    OTHER_ACADEMIC = "Other Academic"
    TRASH = "Trash"


class Subcategory(enum.StrEnum):
    """Question subcategory enum."""

    LITERATURE = "Literature"  # regular cats also included because of database quirks
    HISTORY = "History"
    SCIENCE = "Science"
    FINE_ARTS = "Fine Arts"
    RELIGION = "Religion"
    MYTHOLOGY = "Mythology"
    PHILOSOPHY = "Philosophy"
    SOCIAL_SCIENCE = "Social Science"
    CURRENT_EVENTS = "Current Events"
    GEOGRAPHY = "Geography"
    OTHER_ACADEMIC = "Other Academic"
    TRASH = "Trash"

    AMERICAN_LITERATURE = "American Literature"
    BRITISH_LITERATURE = "British Literature"
    CLASSICAL_LITERATURE = "Classical Literature"
    EUROPEAN_LITERATURE = "European Literature"
    WORLD_LITERATURE = "World Literature"
    OTHER_LITERATURE = "Other Literature"

    AMERICAN_HISTORY = "American History"
    ANCIENT_HISTORY = "Ancient History"
    EUROPEAN_HISTORY = "European History"
    WORLD_HISTORY = "World History"
    OTHER_HISTORY = "Other History"

    BIOLOGY = "Biology"
    CHEMISTRY = "Chemistry"
    PHYSICS = "Physics"
    OTHER_SCIENCE = "Other Science"

    VISUAL_FINE_ARTS = "Visual Fine Arts"
    AUDITORY_FINE_ARTS = "Auditory Fine Arts"
    OTHER_FINE_ARTS = "Other Fine Arts"

class AlternateSubcategory(enum.StrEnum):
    """Question alternate subcategory enum."""

    DRAMA = "Drama"
    LONG_FICTION = "Long Fiction"
    POETRY = "Poetry"
    SHORT_FICTION = "Short Fiction"
    MISC_LITERATURE = "Misc Literature"

    MATH = "Math"
    ASTRONOMY = "Astronomy"
    COMPUTER_SCIENCE = "Computer Science"
    EARTH_SCIENCE = "Earth Science"
    ENGINEERING = "Engineering"
    MISC_SCIENCE = "Misc Science"

    ARCHITECTURE = "Architecture"
    DANCE = "Dance"
    FILM = "Film"
    JAZZ = "Jazz"
    OPERA = "Opera"
    PHOTOGRAPHY = "Photography"
    MISC_ARTS = "Misc Arts"

    ANTHROPOLOGY = "Anthropology"
    ECONOMICS = "Economics"
    LINGUISTICS = "Linguistics"
    PSYCHOLOGY = "Psychology"
    SOCIOLOGY = "Sociology"
    OTHER_SOCIAL_SCIENCE = "Other Social Science"

    BELIEFS = "Beliefs"
    PRACTICES = "Practices"

class Difficulty(enum.StrEnum):
    """Question difficulty enum."""

    UNRATED = "0"
    MS = "1"
    HS_EASY = "2"
    HS_REGS = "3"
    HS_HARD = "4"
    HS_NATS = "5"
    ONE_DOT = "6"
    TWO_DOT = "7"
    THREE_DOT = "8"
    FOUR_DOT = "9"
    OPEN = "10"


class DifficultyModifier(enum.StrEnum):
    """Difficulty modifier enum."""

    EASY = "e"
    MEDIUM = "m"
    HARD = "h"


class Directive(enum.StrEnum):
    """Directives given by `api/check-answer`."""

    ACCEPT = "accept"
    REJECT = "reject"
    PROMPT = "prompt"


class Year(enum.IntEnum):
    """Min/max year enum."""

    MIN_YEAR = 2010
    CURRENT_YEAR = 2024


class AnswerJudgement:
    """A judgement given by `api/check-answer`."""

    def __init__(
        self: Self, directive: Directive, directed_prompt: Optional[str] = None
    ):
        self.directive: Directive = directive
        self.directed_prompt: Optional[str] = directed_prompt

    def __bool__(self: Self) -> bool:
        """Return whether the answer was correct."""
        return self.directive == Directive.ACCEPT

    def __str__(self: Self) -> str:
        """Return a string representation of the judgement."""
        return self.directive.value + (
            f" ({self.directed_prompt})" if self.directed_prompt else ""
        )

    def correct(self: Self) -> bool:
        """Return whether the answer was correct."""
        return self.__bool__()

    @classmethod
    def from_json(cls: Type[Self], json: dict[str, Any]) -> Self:
        """Create an AnswerJudgement from a JSON object.

        See https://www.qbreader.org/api-docs/check-answer#returns for schema.
        """
        return cls(
            directive=Directive(json["directive"]),
            directed_prompt=json.get("directedPrompt", None),
        )

    @classmethod
    def check_answer_sync(cls: Type[Self], answerline: str, givenAnswer: str) -> Self:
        """Create an AnswerJudgement given an answerline and an answer.

        Original API doc at https://www.qbreader.org/api-docs/check-answer.

        Parameters
        ----------
        answerline : str
            The answerline to check against. Preferably including the HTML tags <b> and
            <u>, if they are present.
        givenAnswer : str
            The answer to check.
        """
        # normalize and type check parameters
        if not isinstance(answerline, str):
            raise TypeError(
                f"answerline must be a string, not {type(answerline).__name__}"
            )

        if not isinstance(givenAnswer, str):
            raise TypeError(
                f"givenAnswer must be a string, not {type(givenAnswer).__name__}"
            )

        url = BASE_URL + "/check-answer"

        data = {"answerline": answerline, "givenAnswer": givenAnswer}

        response: requests.Response = requests.get(url, params=data)

        if response.status_code != 200:
            raise Exception(str(response.status_code) + " bad request")

        return cls.from_json(response.json())

    @classmethod
    async def check_answer_async(
        cls: Type[Self],
        answerline: str,
        givenAnswer: str,
        session: aiohttp.ClientSession | None = None,
    ) -> Self:
        """Asynchronously create an AnswerJudgement given an answerline and an answer.

        Original API doc at https://www.qbreader.org/api-docs/check-answer.

        Parameters
        ----------
        answerline : str
            The answerline to check against. Preferably including the HTML tags <b> and
            <u>, if they are present.
        givenAnswer : str
            The answer to check.
        session : aiohttp.ClientSession
            The aiohttp session to use for the request.
        """
        # normalize and type check parameters
        if not isinstance(answerline, str):
            raise TypeError(
                f"answerline must be a string, not {type(answerline).__name__}"
            )

        if not isinstance(givenAnswer, str):
            raise TypeError(
                f"givenAnswer must be a string, not {type(givenAnswer).__name__}"
            )

        url = BASE_URL + "/check-answer"

        data = {"answerline": answerline, "givenAnswer": givenAnswer}

        temp_session: bool = False
        if session is None:
            temp_session = True
            session = aiohttp.ClientSession()

        async with session.get(url, params=data) as response:
            if response.status != 200:
                raise Exception(str(response.status) + " bad request")

            json = await response.json()
            if temp_session:
                await session.close()
            return cls.from_json(json)


class Tossup:
    """Tossup class."""

    def __init__(
        self: Self,
        question: str,
        question_sanitized: str,
        answer: str,
        answer_sanitized: str,
        difficulty: Difficulty,
        category: Category,
        subcategory: Subcategory,
        packet: PacketMetadata,
        set: SetMetadata,
        number: int,
        alternate_subcategory: Optional[AlternateSubcategory] = None,
    ):
        self.question: str = question
        self.question_sanitized: str = question_sanitized
        self.answer: str = answer
        self.answer_sanitized: str = answer_sanitized
        self.difficulty: Difficulty = difficulty
        self.category: Category = category
        self.subcategory: Subcategory = subcategory
        self.packet: PacketMetadata = packet
        self.set: SetMetadata = set
        self.number: int = number
        self.alternate_subcategory: AlternateSubcategory = alternate_subcategory

    @classmethod
    def from_json(cls: Type[Self], json: dict[str, Any]) -> Self:
        """Create a Tossup from a JSON object.

        See https://www.qbreader.org/api-docs/schemas#tossups for schema.
        """
        alternate_subcategory = json.get("alternate_subcategory", None)
        return cls(
            question=json["question"],
            question_sanitized=json["question_sanitized"],
            answer=json["answer"],
            answer_sanitized=json["answer_sanitized"],
            difficulty=Difficulty(str(json["difficulty"])),
            category=Category(json["category"]),
            subcategory=Subcategory(json["subcategory"]),
            packet=PacketMetadata.from_json(json["packet"]),
            set=SetMetadata.from_json(json["set"]),
            number=json["number"],
            alternate_subcategory=AlternateSubcategory(alternate_subcategory) if alternate_subcategory else None,
        )

    def check_answer_sync(self, givenAnswer: str) -> AnswerJudgement:
        """Check whether an answer is correct."""
        return AnswerJudgement.check_answer_sync(self.answer, givenAnswer)

    async def check_answer_async(
        self, givenAnswer: str, session: aiohttp.ClientSession | None = None
    ) -> AnswerJudgement:
        """Asynchronously check whether an answer is correct."""
        return await AnswerJudgement.check_answer_async(
            self.answer, givenAnswer, session
        )

    def __eq__(self, other: object) -> bool:
        """Return whether two tossups are equal."""
        if not isinstance(other, Tossup):
            return NotImplemented

        return (
            self.question == other.question
            and self.question_sanitized == other.question_sanitized
            and self.answer == other.answer
            and self.answer_sanitized == other.answer_sanitized
            and self.difficulty == other.difficulty
            and self.category == other.category
            and self.subcategory == other.subcategory
            and self.alternate_subcategory == other.alternate_subcategory
            and self.packet == other.packet
            and self.set == other.set
            and self.number == other.number
        )

    def __str__(self) -> str:
        """Return the question."""
        return self.question


class Bonus:
    """Bonus class."""

    def __init__(
        self: Self,
        leadin: str,
        leadin_sanitized: str,
        parts: Sequence[str],
        parts_sanitized: Sequence[str],
        answers: Sequence[str],
        answers_sanitized: Sequence[str],
        difficulty: Difficulty,
        category: Category,
        subcategory: Subcategory,
        set: SetMetadata,
        packet: PacketMetadata,
        number: int,
        alternate_subcategory: Optional[AlternateSubcategory] = None,
        values: Optional[Sequence[int]] = None,
        difficultyModifiers: Optional[Sequence[DifficultyModifier]] = None,
    ):
        self.leadin: str = leadin
        self.leadin_sanitized: str = leadin_sanitized
        self.parts: tuple[str, ...] = tuple(parts)
        self.parts_sanitized: tuple[str, ...] = tuple(parts_sanitized)
        self.answers: tuple[str, ...] = tuple(answers)
        self.answers_sanitized: tuple[str, ...] = tuple(answers_sanitized)
        self.difficulty: Difficulty = difficulty
        self.category: Category = category
        self.subcategory: Subcategory = subcategory
        self.set: SetMetadata = set
        self.packet: PacketMetadata = packet
        self.number: int = number
        self.alternate_subcategory: AlternateSubcategory = alternate_subcategory
        self.values: Optional[tuple[int, ...]] = tuple(values) if values else None
        self.difficultyModifiers: Optional[tuple[DifficultyModifier, ...]] = (
            tuple(difficultyModifiers) if difficultyModifiers else None
        )

    @classmethod
    def from_json(cls: Type[Self], json: dict[str, Any]) -> Self:
        """Create a Bonus from a JSON object.

        See https://www.qbreader.org/api-docs/schemas#bonus for schema.
        """
        alternate_subcategory = json.get("alternate_subcategory", None)
        return cls(
            leadin=json["leadin"],
            leadin_sanitized=json["leadin_sanitized"],
            parts=json["parts"],
            parts_sanitized=json["parts_sanitized"],
            answers=json["answers"],
            answers_sanitized=json["answers_sanitized"],
            difficulty=Difficulty(str(json["difficulty"])),
            category=Category(json["category"]),
            subcategory=Subcategory(json["subcategory"]),
            set=SetMetadata.from_json(json["set"]),
            packet=PacketMetadata.from_json(json["packet"]),
            number=json["number"],
            alternate_subcategory=AlternateSubcategory(alternate_subcategory) if alternate_subcategory else None,
            values=json.get("values", None),
            difficultyModifiers=json.get("difficultyModifiers", None),
        )

    def check_answer_sync(self, part: int, givenAnswer: str) -> AnswerJudgement:
        """Check whether an answer is correct."""
        return AnswerJudgement.check_answer_sync(self.answers[part], givenAnswer)

    async def check_answer_async(
        self, part: int, givenAnswer: str, session: aiohttp.ClientSession
    ) -> AnswerJudgement:
        """Asynchronously check whether an answer is correct."""
        return await AnswerJudgement.check_answer_async(
            self.answers[part], givenAnswer, session
        )

    def __eq__(self, other: object) -> bool:
        """Return whether two bonuses are equal."""
        if not isinstance(other, Bonus):
            return NotImplemented

        return (
            self.leadin == other.leadin
            and self.leadin_sanitized == other.leadin_sanitized
            and self.parts == other.parts
            and self.parts_sanitized == other.parts_sanitized
            and self.answers == other.answers
            and self.answers_sanitized == other.answers_sanitized
            and self.difficulty == other.difficulty
            and self.category == other.category
            and self.subcategory == other.subcategory
            and self.alternate_subcategory == other.alternate_subcategory
            and self.set == other.set
            and self.packet == other.packet
            and self.number == other.number
            and self.values == other.values
            and self.difficultyModifiers == other.difficultyModifiers
        )

    def __str__(self) -> str:
        """Return the parts of the bonus."""
        return "\n".join(self.parts)


class QueryResponse:
    """Class for responses to `api/query` requests."""

    def __init__(
        self: Self,
        tossups: Sequence[Tossup],
        bonuses: Sequence[Bonus],
        tossups_found: int,
        bonuses_found: int,
        query_string: str,
    ):
        self.tossups: tuple[Tossup, ...] = tuple(tossups)
        self.bonuses: tuple[Bonus, ...] = tuple(bonuses)
        self.tossups_found: int = tossups_found
        self.bonuses_found: int = bonuses_found
        self.query_string: str = query_string

    @classmethod
    def from_json(cls: Type[Self], json: dict[str, Any]) -> Self:
        """Create a QueryResponse from a JSON object.

        See https://www.qbreader.org/api-docs/query#returns for schema.
        """
        return cls(
            tossups=[
                Tossup.from_json(tossup) for tossup in json["tossups"]["questionArray"]
            ],
            bonuses=[
                Bonus.from_json(bonus) for bonus in json["bonuses"]["questionArray"]
            ],
            tossups_found=json["tossups"]["count"],
            bonuses_found=json["bonuses"]["count"],
            query_string=json["queryString"],
        )

    def __str__(self) -> str:
        """Return the queried tossups and bonuses."""
        return (
            "\n\n".join([str(tossup) for tossup in self.tossups])
            + "\n\n\n"
            + "\n\n".join([str(bonus) for bonus in self.bonuses])
        )


class Packet:
    """Class for packets in sets."""

    def __init__(
        self: Self,
        tossups: Sequence[Tossup],
        bonuses: Sequence[Bonus],
        number: Optional[int] = None,
        name: Optional[str] = None,
        year: Optional[int] = None,
    ):
        self.tossups: tuple[Tossup, ...] = tuple(tossups)
        self.bonuses: tuple[Bonus, ...] = tuple(bonuses)
        self.number: Optional[int] = number if number else self.tossups[0].packet.number
        self.name: Optional[str] = name if name else self.tossups[0].set.name
        self.year: Optional[int] = year if year else self.tossups[0].set.year

    @classmethod
    def from_json(
        cls: Type[Self], json: dict[str, Any], number: Optional[int] = None
    ) -> Self:
        """Create a Packet from a JSON object.

        See https://www.qbreader.org/api-docs/packet#returns for schema.
        """
        return cls(
            tossups=[Tossup.from_json(tossup) for tossup in json["tossups"]],
            bonuses=[Bonus.from_json(bonus) for bonus in json["bonuses"]],
            number=number,
        )

    def paired_questions(self) -> zip[tuple[Tossup, Bonus]]:
        """Yield pairs of tossups and bonuses."""
        return zip(self.tossups, self.bonuses)

    def __iter__(self) -> zip[tuple[Tossup, Bonus]]:
        """Alias to `paired_questions()`."""
        return self.paired_questions()

    def __eq__(self, other: object) -> bool:
        """Return whether two packets are equal."""
        if not isinstance(other, Packet):
            return NotImplemented

        return (
            self.tossups == other.tossups
            and self.bonuses == other.bonuses
            and self.number == other.number
            and self.name == other.name
            and self.year == other.year
        )

    def __str__(self) -> str:
        """Return the tossups and bonuses in the packet."""
        return (
            "\n\n".join([str(tossup) for tossup in self.tossups])
            + "\n\n\n"
            + "\n\n".join([str(bonus) for bonus in self.bonuses])
        )


class PacketMetadata:
    def __init__(
        self: Self,
        _id: str,
        name: str,
        number: int,
    ):
        self._id: str = _id
        self.name: str = name
        self.number: int = number

    @classmethod
    def from_json(cls: Type[Self], json: dict[str, Any]) -> Self:
        return cls(
            _id=json["_id"],
            name=json["name"],
            number=json["number"],
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PacketMetadata):
            return NotImplemented

        return (
            self._id == other._id
            and self.name == other.name
            and self.number == other.number
        )

    def __str__(self) -> str:
        return self.name


class SetMetadata:
    def __init__(
        self: Self,
        _id: str,
        name: str,
        year: int,
        standard: bool,
    ):
        self._id: str = _id
        self.name: str = name
        self.year: int = year
        self.standard: bool = standard

    @classmethod
    def from_json(cls: Type[Self], json: dict[str, Any]) -> Self:
        return cls(
            _id=json["_id"],
            name=json["name"],
            year=json["year"],
            standard=json["standard"],
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SetMetadata):
            return NotImplemented

        return (
            self._id == other._id
            and self.name == other.name
            and self.year == other.year
            and self.standard == other.standard
        )

    def __str__(self) -> str:
        return self.name


QuestionType: TypeAlias = Union[
    Literal["tossup", "bonus", "all"], Type[Tossup], Type[Bonus]
]
"""Type alias for question types."""

SearchType: TypeAlias = Literal["question", "answer", "all"]
"""Type alias for query search types."""

ValidDifficulties: TypeAlias = Literal[
    0,
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
]
"""Type alias for valid difficulties."""

UnnormalizedDifficulty: TypeAlias = Optional[
    Union[Difficulty, ValidDifficulties, Iterable[Union[Difficulty, ValidDifficulties]]]
]
"""Type alias for unnormalized difficulties. Union of `Difficulty`, `ValidDifficulties`,
and `collections.abc.Iterable` containing either."""

UnnormalizedCategory: TypeAlias = Optional[
    Union[Category, str, Iterable[Union[Category, str]]]
]
"""Type alias for unnormalized categories. Union of `Category`, `str`, and
`collections.abc.Iterable` containing either."""

UnnormalizedSubcategory: TypeAlias = Optional[
    Union[Subcategory, str, Iterable[Union[Subcategory, str]]]
]
"""Type alias for unnormalized subcategories. Union of `Subcategory`, `str`, and
`collections.abc.Iterable` containing either."""

UnnormalizedAlternateSubcategory: TypeAlias = Optional[
    Union[AlternateSubcategory, str, Iterable[Union[AlternateSubcategory, str]]]
]
"""Type alias for unnormalized alternate subcategories. Union of `AlternateSubcategory`, `str`, and
`collections.abc.Iterable` containing either."""


__all__ = (
    "Tossup",
    "Bonus",
    "Packet",
    "QueryResponse",
    "AnswerJudgement",
    "Category",
    "Subcategory",
    "AlternateSubcategory",
    "Difficulty",
    "Directive",
    "QuestionType",
    "SearchType",
    "ValidDifficulties",
    "UnnormalizedDifficulty",
    "UnnormalizedCategory",
    "UnnormalizedSubcategory",
    "UnnormalizedAlternateSubcategory"
)
