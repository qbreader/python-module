"""Types and classes used by the library."""

import enum
from typing import Iterable, Literal, Optional, Self, Sequence, Type, TypeAlias, Union


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
    MATH = "Math"
    OTHER_SCIENCE = "Other Science"

    VISUAL_FINE_ARTS = "Visual Fine Arts"
    AUDITORY_FINE_ARTS = "Auditory Fine Arts"
    OTHER_FINE_ARTS = "Other Fine Arts"


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


class Tossup:
    """Tossup class."""

    def __init__(
        self: Self,
        question: str,
        formatted_answer: Optional[str],
        answer: str,
        category: Category,
        subcategory: Subcategory,
        set: str,
        packet_number: int,
        question_number: int,
        difficulty: Difficulty,
    ):
        self.question: str = question
        self.formatted_answer: str = formatted_answer if formatted_answer else answer
        self.answer: str = answer
        self.category: Category = category
        self.subcategory: Subcategory = subcategory
        self.set: str = set
        self.packet_number: int = packet_number
        self.question_number: int = question_number
        self.difficulty: Difficulty = difficulty


class Bonus:
    """Bonus class."""

    def __init__(
        self: Self,
        leadin: str,
        parts: Sequence[str],
        formatted_answers: Optional[Sequence[str]],
        answers: Sequence[str],
        category: Category,
        subcategory: Subcategory,
        set: str,
        packet_number: int,
        question_number: int,
        difficulty: Difficulty,
    ):
        self.leadin: str = leadin
        self.parts: tuple[str, ...] = tuple(parts)
        self.formatted_answers: tuple[str, ...] = tuple(
            formatted_answers if formatted_answers else answers
        )
        self.answers: tuple[str, ...] = tuple(answers)
        self.category: Category = category
        self.subcategory: Subcategory = subcategory
        self.set: str = set
        self.packet_number: int = packet_number
        self.question_number: int = question_number
        self.difficulty: Difficulty = difficulty


QuestionType: TypeAlias = Union[
    Literal["tossup", "bonus", "all"], Type[Tossup], Type[Bonus]
]
SearchType: TypeAlias = Literal["question", "answer", "all"]

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
UnnormalizedDifficulty: TypeAlias = Optional[
    Union[Difficulty, ValidDifficulties, Iterable[Union[Difficulty, ValidDifficulties]]]
]
UnnormalizedCategory: TypeAlias = Optional[
    Union[Category, str, Iterable[Union[Category, str]]]
]
UnnormalizedSubcategory: TypeAlias = Optional[
    Union[Subcategory, str, Iterable[Union[Subcategory, str]]]
]
