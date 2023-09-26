# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import sys
from os import path

import qbreader

sys.path.insert(0, path.abspath(".."))

project = "python-qbreader"
copyright = "2023, Sky Hong, Rohan Arni, Geoffrey Wu"
author = "Sky Hong, Rohan Arni, Geoffrey Wu"
release = qbreader.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.duration",
    "sphinx.ext.intersphinx",
    "sphinx.ext.napoleon",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
default_role = "py:obj"

highlight_language = "python3"

autodoc_member_order = "bysource"
autodoc_type_aliases = {
    "Async": "qbreader.asynchronous.Async",
    "Sync": "qbreader.synchronous.Sync",
    "Tossup": "qbreader.types.Tossup",
    "Bonus": "qbreader.types.Bonus",
    "Category": "qbreader.types.Category",
    "Subcategory": "qbreader.types.Subcategory",
    "Difficulty": "qbreader.types.Difficulty",
    "QueryResponse": "qbreader.types.QueryResponse",
    "Directive": "qbreader.types.Directive",
    "AnswerJudgement": "qbreader.types.AnswerJudgement",
    "Packet": "qbreader.types.Packet",
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "furo"
html_favicon = "_static/favicon.ico"
html_logo = "_static/logo.png"
html_static_path = ["_static"]

intersphinx_mapping = {
    "py": ("https://docs.python.org/3", None),
}
