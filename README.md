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

```py
>>> from qbreader import Sync as qbr # synchronous interface
>>> sync_client = qbr()
>>> tossup = sync_client.random_tossup()[0]
>>> tossup.question
'Tim Peters wrote 19 “guiding principles” of this programming language, which include the maxim “Complex is better than complicated.” The “pandas” library was written for this language. Unicode string values had to be defined with a “u” in version 2 of this language. Libraries in this language include Tkinter, Tensorflow, (*) NumPy (“numb pie”) and SciPy (“sigh pie”). The framework Django was written in this language. This language uses “duck typing.” Variables in this language are often named “spam” and “eggs.” Guido van Rossum invented, for 10 points, what programming language named for a British comedy troupe?'
>>> tossup.answer
'Python'
>>> tossup.category
<Category.SCIENCE: 'Science'>
>>> tossup.subcategory
<Subcategory.OTHER_SCIENCE: 'Other Science'>
>>> tossup.difficulty
<Difficulty.HS_HARD: '4'>
>>> tossup.set
'2022 Prison Bowl'
>>> (tossup.packet_number, tossup.question_number)
(4, 20)
```
