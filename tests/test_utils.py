import pytest

import qbreader.api_utils as api_utils
from qbreader.types import Category, Difficulty, Subcategory
from tests import assert_exception, assert_warning


class TestNormalization:
    """Test normalization functions."""

    @pytest.mark.parametrize(
        "boolean, expected",
        [
            (True, "true"),
            (False, "false"),
            ("true", "true"),
            ("false", "false"),
        ],
    )
    def test_normalize_bool(self, boolean, expected):
        assert api_utils.normalize_bool(boolean) == expected

    @pytest.mark.parametrize(
        "boolean, exception", [(None, TypeError), (1, TypeError), ("1", ValueError)]
    )
    def test_normalize_bool_exception(self, boolean, exception):
        assert_exception(api_utils.normalize_bool, exception, boolean)

    @pytest.mark.parametrize(
        "diff, expected",
        [
            (Difficulty.HS_REGS, "3"),
            (10, "10"),
            ("2", "2"),
            ([Difficulty.HS_REGS], "3"),
            ([Difficulty.HS_REGS, Difficulty.HS_HARD], "3,4"),
            ([Difficulty.HS_REGS, "3", "4"], "3,4"),
            (["3", "4"], "3,4"),
            (["1", "4", 7], "1,4,7"),
            (["3", "2", 5, Difficulty.HS_HARD], "2,3,4,5"),
            (list(range(11)), "0,1,2,3,4,5,6,7,8,9,10"),
            (None, ""),
            ([], ""),
        ],
    )
    def test_normalize_diff(self, diff, expected):
        assert set(api_utils.normalize_diff(diff).split(",")) == set(
            expected.split(",")
        )  # contains the same elements

    @pytest.mark.parametrize(
        "diff, exception",
        [
            (3.14, TypeError),
            (3 + 4j, TypeError),
            (True, TypeError),
            ([3.14], TypeError),
        ],
    )
    def test_normalize_diff_exception(self, diff, exception):
        assert_exception(api_utils.normalize_diff, exception, diff)

    @pytest.mark.parametrize(
        "diff, warning",
        [
            ("3.14", UserWarning),
            ("11", UserWarning),
            (["-1"], UserWarning),
            (1000, UserWarning),
        ],
    )
    def test_normalize_diff_warning(self, diff, warning):
        assert assert_warning(api_utils.normalize_diff, warning, diff) == ""

    @pytest.mark.parametrize(
        "cat, expected",
        [
            (Category.SCIENCE, "Science"),
            (Category.SCIENCE.value, "Science"),
            ("Science", "Science"),
            (["Science"], "Science"),
            ([Category.SCIENCE], "Science"),
            ([Category.SCIENCE, Category.LITERATURE], "Science,Literature"),
            ([Category.SCIENCE, "Literature"], "Science,Literature"),
            (["Science", "Literature"], "Science,Literature"),
            (["Science", "Literature", "Literature"], "Science,Literature"),
            (
                [
                    "Science",
                    "Literature",
                    "Literature",
                    Category.SCIENCE,
                    Category.HISTORY,
                ],
                "Science,Literature,History",
            ),
        ],
    )
    def test_normalize_cat(self, cat, expected):
        assert set(api_utils.normalize_cat(cat).split(",")) == set(expected.split(","))

    @pytest.mark.parametrize(
        "cat, exception",
        [
            (3.14, TypeError),
            (3 + 4j, TypeError),
            (True, TypeError),
            ([3.14], TypeError),
        ],
    )
    def test_normalize_cat_exception(self, cat, exception):
        assert_exception(api_utils.normalize_cat, exception, cat)

    @pytest.mark.parametrize(
        "cat, warning",
        [
            ("3.14", UserWarning),
            ("11", UserWarning),
            (["-1"], UserWarning),
            (1000, UserWarning),
        ],
    )
    def test_normalize_cat_warning(self, cat, warning):
        assert assert_warning(api_utils.normalize_cat, warning, cat) == ""

    @pytest.mark.parametrize(
        "subcat, expected",
        [  # reused because subcat is a superset of cat
            (Subcategory.SCIENCE, "Science"),
            (Subcategory.SCIENCE.value, "Science"),
            ("Science", "Science"),
            (["Science"], "Science"),
            ([Subcategory.SCIENCE], "Science"),
            ([Subcategory.SCIENCE, Subcategory.LITERATURE], "Science,Literature"),
            ([Subcategory.SCIENCE, "Literature"], "Science,Literature"),
            (["Science", "Literature"], "Science,Literature"),
            (["Science", "Literature", "Literature"], "Science,Literature"),
            (
                [
                    "Science",
                    "Literature",
                    "Literature",
                    Subcategory.SCIENCE,
                    Subcategory.HISTORY,
                ],
                "Science,Literature,History",
            ),
        ],
    )
    def test_normalize_subcat(self, subcat, expected):
        assert set(api_utils.normalize_subcat(subcat).split(",")) == set(
            expected.split(",")
        )

    @pytest.mark.parametrize(
        "subcat, exception",
        [
            (3.14, TypeError),
            (3 + 4j, TypeError),
            (True, TypeError),
            ([3.14], TypeError),
        ],
    )
    def test_normalize_subcat_exception(self, subcat, exception):
        assert_exception(api_utils.normalize_subcat, exception, subcat)

    @pytest.mark.parametrize(
        "subcat, warning",
        [
            ("3.14", UserWarning),
            ("11", UserWarning),
            (["-1"], UserWarning),
            (1000, UserWarning),
        ],
    )
    def test_normalize_subcat_warning(self, subcat, warning):
        assert assert_warning(api_utils.normalize_cat, warning, subcat) == ""

    @pytest.mark.parametrize(
        "dict, expected",
        [
            ({"a": 1, "b": 2, "c": 3}, {"a": 1, "b": 2, "c": 3}),
            ({"a": 1, "b": None, "c": 3}, {"a": 1, "c": 3}),
            ({"a": 1, "b": None, None: ""}, {"a": 1}),
            (
                {"a": 1, "b": None, None: None, "c": True, "d": False},
                {"a": 1, "c": True, "d": False},
            ),
        ],
    )
    def test_prune_none(self, dict, expected):
        assert api_utils.prune_none(dict) == expected
