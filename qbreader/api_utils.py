"""Useful functions used by both the asynchronous and synchronous API wrappers."""

import warnings
from enum import Enum, EnumType
from typing import Iterable, Optional, Union

from qbreader.types import (
    Category,
    Difficulty,
    Subcategory,
    UnnormalizedCategory,
    UnnormalizedDifficulty,
    UnnormalizedSubcategory,
)


def normalize_bool(boolean: Optional[Union[bool, str]]) -> str:
    """Normalize a boolean value to a string for HTTP requests."""
    if isinstance(boolean, bool):
        return str(boolean).lower()
    elif isinstance(boolean, str):
        if (boolean := boolean.lower()) in ("true", "false"):
            return boolean
        else:
            raise ValueError(f"Invalid str value: {boolean}")
    else:
        raise TypeError(f"Invalid type: {type(boolean).__name__}, expected bool or str")


def normalize_enumlike(
    unnormalized: Optional[Union[Enum, str, int, Iterable[Union[Enum, str, int]]]],
    enum_type: EnumType,
) -> str:
    """Normalize a single or list of enum-like values into a comma separated string."""

    def valid_enumlike(item: Union[Enum, str, int]) -> bool:
        """Check if an item is a valid enum-like value."""
        return (
            item in enum_type.__members__.values()
            or str(item) in enum_type.__members__.values()
        )

    strs: list[str] = []

    if unnormalized is None:
        return ""

    if isinstance(unnormalized, (str, int, enum_type)):  # single item
        if isinstance(unnormalized, bool):  # python bools are ints
            raise TypeError(
                f"Invalid type: {type(unnormalized).__name__}, expected int, str, or "
                + f"{enum_type}."
            )
        if valid_enumlike(unnormalized):  # type: ignore
            # this is ok to ignore because it's counting strings as iterables
            strs.append(str(unnormalized))
            return ",".join(strs)
        else:
            warnings.warn(
                f"Invalid value: {unnormalized} for {enum_type}.", UserWarning
            )
            return ""

    if isinstance(unnormalized, Iterable):  # iterable of str, int, or Difficulty
        for item in unnormalized:
            if isinstance(item, (str, int, enum_type)):
                if valid_enumlike(item):
                    strs.append(str(item))
                else:
                    warnings.warn(
                        f"Invalid value: {item} for {enum_type}.", UserWarning
                    )

            else:
                raise TypeError(
                    f"Invalid type: {type(item).__name__}, expected int, str, or "
                    + f"{enum_type}."
                )
        strs = list(set(strs))  # remove duplicates
        return ",".join(strs)

    raise TypeError(
        f"Invalid type: {type(unnormalized).__name__}, expected int, str, {enum_type}, "
        + "or Iterable of those."
    )


def normalize_diff(unnormalized_diffs: UnnormalizedDifficulty):
    """Normalize a single or list of difficulty values to a comma separated string."""
    return normalize_enumlike(unnormalized_diffs, Difficulty)


def normalize_cat(unnormalized_cats: UnnormalizedCategory):
    """Normalize a single or list of categories to a comma separated string."""
    return normalize_enumlike(unnormalized_cats, Category)


def normalize_subcat(unnormalized_subcats: UnnormalizedSubcategory):
    """Normalize a single or list of subcategories to a comma separated string."""
    return normalize_enumlike(unnormalized_subcats, Subcategory)


def prune_none(params: dict) -> dict:
    """Remove all None values from a dictionary."""
    return {
        key: value
        for key, value in params.items()
        if (value is not None and key is not None)
    }
