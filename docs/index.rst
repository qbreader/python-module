.. python-qbreader documentation master file, created by
   sphinx-quickstart on Fri Sep 22 19:37:45 2023.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

python-qbreader
===============

.. toctree::
   :hidden:
   :caption: API Reference

   qbreader <api/qbreader>

.. toctree::
   :hidden:
   :caption: Indices

   genindex
   modindex

``qbreader`` is a Python wrapper to the qbreader_ API as well as a general quizbowl library. It provides
both asynchronous and synchronous interfaces to the API along with functionality for representing questions.

A small example
---------------

.. code:: python

   >>> from qbreader import Sync as qbr # synchronous interface
   >>> tossup = qbr.random_tossup()[0]
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

.. _qbreader: https://www.qbreader.org/