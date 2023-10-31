# 🧩 TrTokenizer

A simple sentence tokenizer.

![Python Version](https://img.shields.io/pypi/pyversions/trtokenizer.svg?style=plastic)
![PyPI Version](https://badge.fury.io/py/trtokenizer)

## Overview

**TrTokenizer** is a comprehensive solution for Turkish sentence and word tokenization, tailored to accommodate extensive language conventions. If you're seeking robust, fast, and accurate tokenization for natural language models, you've come to the right place. Our sentence tokenization approach employs a list of non-prefix keywords found in the 'tr_non_suffixes' file. Developers can conveniently expand this file, and lines starting with '#' are treated as comments. We've designed regular expressions that are pre-compiled for optimal performance.

## Installation

You can install **TrTokenizer** via pip:

```sh
pip install trtokenizer
```

## Usage

Here's how you can use **TrTokenizer** in your Python projects:

```python
from trtokenizer.tr_tokenizer import SentenceTokenizer, WordTokenizer

# Initialize a SentenceTokenizer object
sentence_tokenizer = SentenceTokenizer()

# Tokenize a given paragraph as a string
sentence_tokenizer.tokenize("Your paragraph goes here.")

# Initialize a WordTokenizer object
word_tokenizer = WordTokenizer()

# Tokenize a given sentence as a string
word_tokenizer.tokenize("Your sentence goes here.")
```

## To-do List

Our to-do list includes:

- Usage examples (Complete)
- Cython C-API for enhanced performance (Complete, see `build/tr_tokenizer.c`)
- Release platform-specific shared dynamic libraries (Complete, e.g., `build/tr_tokenizer.cpython-38-x86_64-linux-gnu.so`, available for Debian Linux with GCC compiler)
- Document any limitations
- Provide a straightforward guide for contributing

## Additional Resources

Explore more about natural language processing and related topics:

- [Speech and Language Processing](https://web.stanford.edu/~jurafsky/slp3/)
- [Bogazici University CMPE-561](https://www.cmpe.boun.edu.tr/tr/courses/cmpe561)
