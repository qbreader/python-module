# qbreader/python-module

[![pypi](https://img.shields.io/pypi/v/qbreader?logo=pypi&logoColor=f0f0f0)](https://pypi.org/project/qbreader/)
[![downloads](https://img.shields.io/pypi/dm/qbreader?logo=pypi&logoColor=f0f0f0)](https://pypi.org/project/qbreader/)
[![python](https://img.shields.io/pypi/pyversions/qbreader?logo=python&logoColor=f0f0f0)](https://pypi.org/project/qbreader/)
[![build](https://img.shields.io/github/actions/workflow/status/qbreader/python-module/test.yml?logo=github&logoColor=f0f0f0)](https://github.com/qbreader/python-module/actions/workflows/test.yml)
[![docs](https://readthedocs.org/projects/python-qbreader/badge/?version=latest)](https://python-qbreader.readthedocs.io/en/latest/?badge=latest)

---

## Introduction

`qbreader` is a Python wrapper to the qbreader API as well as a general quizbowl library. It provides
both asynchronous and synchronous interfaces to the API along with functionality for representing questions.

Documentation for this package is available at <https://python-qbreader.readthedocs.io/>.

## Installation

### PyPI

```sh
$ pip install qbreader
# or whatever environment/dependency management system you use
```

### Git

Alternatively, you may install the most recent, but potentially unstable, development version directly from this repository.

```sh
$ pip install git+https://github.com/qbreader/python-module.git
```

### Developing with Poetry

1. [Install poetry](https://python-poetry.org/docs/#installation).
2. Run `poetry install`
3. After making changes, run `poetry run pytest`
  - You can also run individual files with `poetry run python your_file.py`

## A quick glance

```py
>>> from qbreader import Sync as qbr # synchronous interface
>>> sync_client = qbr()
>>> tossup = sync_client.random_tossup()[0]
>>> tossup.question
'<b>Tim Peters wrote 19 “guiding principles” of this programming language, which include the maxim “Complex is better than complicated.” The “pandas” library was written for this language. Unicode string values had to be defined with a “u” in version 2 of this language. Libraries in this language include Tkinter, Tensorflow, (*)</b> NumPy (“numb pie”) and SciPy (“sigh pie”). The framework Django was written in this language. This language uses “duck typing.” Variables in this language are often named “spam” and “eggs.” Guido van Rossum invented, for 10 points, what programming language named for a British comedy troupe?'
>>> tossup.question_sanitized
'Tim Peters wrote 19 “guiding principles” of this programming language, which include the maxim “Complex is better than complicated.” The “pandas” library was written for this language. Unicode string values had to be defined with a “u” in version 2 of this language. Libraries in this language include Tkinter, Tensorflow, (*) NumPy (“numb pie”) and SciPy (“sigh pie”). The framework Django was written in this language. This language uses “duck typing.” Variables in this language are often named “spam” and “eggs.” Guido van Rossum invented, for 10 points, what programming language named for a British comedy troupe?'
>>> tossup.answer
'<b><u>Python</u></b>'
>>> tossup.answer_sanitized
'Python'
>>> tossup.category
<Category.SCIENCE: 'Science'>
>>> tossup.subcategory
<Subcategory.OTHER_SCIENCE: 'Other Science'>
>>> tossup.difficulty
<Difficulty.HS_HARD: '4'>
>>> tossup.set.name
'2022 Prison Bowl'
>>> (tossup.packet.number, tossup.number)
(4, 20)
>>> bonus = sync_client.random_bonus()[0]
>>> bonus.leadin
'The Curry–Howard isomorphism states that computer programs are directly equivalent to these mathematical constructs, which can be automated using the languages Lean or Rocq (“rock”). For 10 points each:'
>>> bonus.leadin_sanitized
'The Curry-Howard isomorphism states that computer programs are directly equivalent to these mathematical constructs, which can be automated using the languages Lean or Rocq ("rock"). For 10 points each:'
>>> bonus.parts
('Name these mathematical constructs that are used to formally demonstrate the truth of a mathematical statement.', 'According to the Curry–Howard isomorphism, these programming concepts correspond to individual propositions of a proof. One method of “inferring” these things in programming languages like Python is named for the duck test.', 'Haskell Curry also lends his name to “currying,” a common tool in functional programming languages that transforms a function into a sequence of functions each with a smaller value for this property. A description is acceptable.')
>>> bonus.parts_sanitized
('Name these mathematical constructs that are used to formally demonstrate the truth of a mathematical statement.', 'According to the Curry-Howard isomorphism, these programming concepts correspond to individual propositions of a proof. One method of "inferring" these things in programming languages like Python is named for the duck test.', 'Haskell Curry also lends his name to "currying," a common tool in functional programming languages that transforms a function into a sequence of functions each with a smaller value for this property. A description is acceptable.')
>>> bonus.answers
('mathematical <b><u>proof</u>s</b> [or formal <b><u>proof</u></b>s or <b><u>proof</u></b>s of correctness; accept <b><u>proof</u></b> assistant or theorem <b><u>prover</u></b> or Rocq <b><u>prover</u></b>]', 'data <b><u>type</u></b>s [accept <b><u>type</u></b> inference or duck <b><u>typing</u></b>]', '<b><u>arity</u></b> [accept descriptions of the <b><u>number of argument</u></b>s or the <b><u>number of parameter</u></b>s or the <b><u>number of</u> <u>input</u></b>s of a function]')
>>> bonus.answers_sanitized
('mathematical proofs [or formal proofs or proofs of correctness; accept proof assistant or theorem prover or Rocq prover]', 'data types [accept type inference or duck typing]', 'arity [accept descriptions of the number of arguments or the number of parameters or the number of inputs of a function]')
>>> bonus.difficultyModifiers
('e', 'm', 'h')
>>> bonus.values
(10, 10, 10)
```
