[![Build Status](https://travis-ci.org/amenezes/pybmoore.svg?branch=master)](https://travis-ci.org/amenezes/pybmoore)
[![Maintainability](https://api.codeclimate.com/v1/badges/7b8b70e0c20c6809df54/maintainability)](https://codeclimate.com/github/amenezes/pybmoore/maintainability)
[![codecov](https://codecov.io/gh/amenezes/pybmoore/branch/master/graph/badge.svg)](https://codecov.io/gh/amenezes/pybmoore)
[![PyPI version](https://badge.fury.io/py/pybmoore.svg)](https://badge.fury.io/py/pybmoore)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pybmoore)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# pybmoore

Pure Python implementation of [Boyer-Moore string-search algorithm](https://en.wikipedia.org/wiki/Boyer%E2%80%93Moore_string-search_algorithm).

## Installing

Install and update using pip:

````bash
pip install pybmoore
````

## Usage

### Single term

The search method in the `pybmoore` module will return a list of tuples with all occurrences, where the tuple have the initial and final position. For example:

```python
import pybmoore

TEXT = "The Boyer–Moore string-search algorithm is an efficient string-searching algorithm that is the standard benchmark for practical string-search literature."

matches = pybmoore.search('string', TEXT)
print(f"Occurrences: {len(matches)}")
print(matches)
# output: [(16, 22), (56, 62), (128, 134)]

for x, y in matches:
    print(f"({x},{y}) - {TEXT[x:y]}")
```

> notice: this implemenation it's case sensitive.


```python
import pybmoore

TEXT = "The algorithm preprocesses the string being searched for (the pattern), but not the string being searched in (the text). It is thus well-suited for applications in which the pattern is much shorter than the text or where it persists across multiple searches."

pybmoore.search('algorithm', TEXT)
# output: [(4, 13)]

pybmoore.search('Algorithm', TEXT)
# output: []
```

### Multiple terms

```python
import pybmoore

TEXT = "The Boyer-Moore algorithm searches for occurrences of P in T by performing explicit character comparisons at different alignments. Instead of a brute-force search of all alignments (of which there are m − n + 1, Boyer-Moore uses information gained by preprocessing P to skip as many alignments as possible."

pybmoore.search(['brute-force', 'Boyer-Moore'], TEXT)
print(matches)
# output: {'brute-force': [(144, 155)], 'Boyer-Moore': [(4, 15), (212, 223)]}
```

## Links

- License: [Apache License](https://choosealicense.com/licenses/apache-2.0/)
- Code: [https://github.com/amenezes/pybmoore](https://github.com/amenezes/pybmoore)
- Issue tracker: [https://github.com/amenezes/pybmoore/issues](https://github.com/amenezes/pybmoore/issues)