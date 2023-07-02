"""Types and classes used by the library."""

import enum
from typing import Optional, Self


class Category(enum.StrEnum):
    """Question category."""

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
    """Question subcategory."""

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


class Difficulty(enum.IntEnum):
    """Question difficulty."""

    MS = 1
    HS_EASY = 2
    HS_REGS = 3
    HS_HARD = 4
    HS_NATS = 5
    ONE_DOT = 6
    TWO_DOT = 7
    THREE_DOT = 8
    FOUR_DOT = 9
    OPEN = 10


class Tossup:
    """Tossup."""

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
    """Bonus."""

    def __init__(
        self: Self,
        leadin: str,
        parts: list[str],
        formatted_answers: Optional[list[str]],
        answers: list[str],
        category: Category,
        subcategory: Subcategory,
        set: str,
        packet_number: int,
        question_number: int,
        difficulty: Difficulty,
    ):
        self.leadin: str = leadin
        self.parts: list[str] = parts
        self.formatted_answers: list[str] = (
            formatted_answers if formatted_answers else answers
        )
        self.answers: list[str] = answers
        self.category: Category = category
        self.subcategory: Subcategory = subcategory
        self.set: str = set
        self.packet_number: int = packet_number
        self.question_number: int = question_number
        self.difficulty: Difficulty = difficulty
