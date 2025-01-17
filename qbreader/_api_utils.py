"""Useful functions used by both the asynchronous and synchronous API wrappers."""

from __future__ import annotations

import warnings
from enum import Enum, EnumType
from typing import Iterable, Optional, Union, Tuple

from qbreader.types import (
    Difficulty,
    Category,
    Subcategory,
    AlternateSubcategory,
    UnnormalizedCategory,
    UnnormalizedDifficulty,
    UnnormalizedSubcategory,
    UnnormalizedAlternateSubcategory,
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


def normalize_subcat(unnormalized_subcats: UnnormalizedCategory):
    """Normalize a single or list of subcategories to a comma separated string."""
    return normalize_enumlike(unnormalized_subcats, Category)


def category_correspondence(
    typed_alt_subcat: AlternateSubcategory,
) -> Tuple[Category, Subcategory]:
    if typed_alt_subcat in [
        AlternateSubcategory.ASTRONOMY,
        AlternateSubcategory.COMPUTER_SCIENCE,
        AlternateSubcategory.MATH,
        AlternateSubcategory.EARTH_SCIENCE,
        AlternateSubcategory.ENGINEERING,
        AlternateSubcategory.MISC_SCIENCE,
    ]:
        return (None, Subcategory.OTHER_SCIENCE)

    if typed_alt_subcat in [
        AlternateSubcategory.ARCHITECTURE,
        AlternateSubcategory.DANCE,
        AlternateSubcategory.FILM,
        AlternateSubcategory.JAZZ,
        AlternateSubcategory.OPERA,
        AlternateSubcategory.PHOTOGRAPHY,
        AlternateSubcategory.MISC_ARTS,
    ]:
        return (None, Subcategory.OTHER_FINE_ARTS)

    if typed_alt_subcat in [
        AlternateSubcategory.ANTHROPOLOGY,
        AlternateSubcategory.ECONOMICS,
        AlternateSubcategory.LINGUISTICS,
        AlternateSubcategory.PSYCHOLOGY,
        AlternateSubcategory.SOCIOLOGY,
        AlternateSubcategory.OTHER_SOCIAL_SCIENCE,
    ]:
        return (None, Subcategory.SOCIAL_SCIENCE)

    if typed_alt_subcat in [
        AlternateSubcategory.DRAMA,
        AlternateSubcategory.LONG_FICTION,
        AlternateSubcategory.POETRY,
        AlternateSubcategory.SHORT_FICTION,
        AlternateSubcategory.MISC_LITERATURE,
    ]:
        return (Category.LITERATURE, None)


def normalize_cats(
    unnormalized_cats: UnnormalizedCategory,
    unnormalized_subcats: UnnormalizedSubcategory,
    unnormalized_alt_subcats: UnnormalizedAlternateSubcategory,
) -> Tuple[Category, Subcategory, AlternateSubcategory]:
    """
    Normalize a single or list of categories, subcategories, and alternate_subcategories
    to their corresponding comma-separated strings, taking into account categories and
    subcategories that must be added for the alternate_subcategories to work.
    """

    typed_alt_subcats: list[AlternateSubcategory] = []

    if isinstance(unnormalized_alt_subcats, str):
        typed_alt_subcats.append(AlternateSubcategory(unnormalized_alt_subcats))
    elif isinstance(unnormalized_alt_subcats, Iterable):
        for alt_subcat in unnormalized_alt_subcats:
            typed_alt_subcats.append(AlternateSubcategory(alt_subcat))

    to_be_pushed_cats: list[Category] = []
    to_be_pushed_subcats: list[Subcategory] = []

    for alt_subcat in typed_alt_subcats:
        cat, subcat = category_correspondence(alt_subcat)
        if cat:
            to_be_pushed_cats.append(cat)
        if subcat:
            to_be_pushed_subcats.append(subcat)

    final_cats = []
    if unnormalized_cats is None:
        final_cats = to_be_pushed_cats
    elif isinstance(unnormalized_cats, str):
        final_cats = [Category(unnormalized_cats), *to_be_pushed_cats]
    elif isinstance(unnormalized_cats, Iterable):
        for subcat in unnormalized_cats:
            final_cats.append(Subcategory(subcat))
        final_cats.append(*to_be_pushed_cats)

    final_subcats = []
    if unnormalized_subcats is None:
        final_subcats = to_be_pushed_subcats
    elif isinstance(unnormalized_subcats, str):
        final_subcats = [Subcategory(unnormalized_subcats), *to_be_pushed_subcats]
    elif isinstance(unnormalized_subcats, Iterable):
        for subcat in unnormalized_subcats:
            final_subcats.append(Subcategory(subcat))
        final_subcats.append(*to_be_pushed_subcats)

    return (
        normalize_enumlike(final_cats, Category),
        normalize_enumlike(final_subcats, Subcategory),
        normalize_enumlike(typed_alt_subcats, AlternateSubcategory),
    )


def prune_none(params: dict) -> dict:
    """Remove all None values from a dictionary."""
    return {
        key: value
        for key, value in params.items()
        if (value is not None and key is not None)
    }
