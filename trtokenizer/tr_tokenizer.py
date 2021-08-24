# -*- coding: utf-8 -*-

"""
Turkish sentence and word tokenizers
"""

__all__ = ['SentenceTokenizer', 'WordTokenizer']
__version__ = '0.0.0.1'

import os
import pathlib
from enum import Enum
from typing import Optional, Tuple, Union

import regex as re

from trtokenizer.errors import NonPrefixFileNotExistError


class SentenceTokenizer:
    class PrefixType(Enum):
        DEFAULT: int
        NUMERIC_ONLY: int

        DEFAULT = 1
        NUMERIC_ONLY = 2

    __slots__ = (
        # Dictionary of non-breaking prefixes; keys are string prefixes, values are PrefixType enums
        '__non_breaking_prefixes',
        'non_breaking_prefix_file',
        'pre_compiled_regexes'
    )

    def __repr__(self):
        if self.non_breaking_prefix_file:
            return f'Sentence tokenizer integrated with "{self.non_breaking_prefix_file}" look-up table'
        else:
            return f'Sentence tokenizer not integrated with look-up table'

    def __init__(self, non_breaking_prefix_file: Optional[str] = None):
        """Sentence tokenizer

        Parameters
        ----------
        non_breaking_prefix_file : str, optional
            path to non-breaking prefix file.

        Raises
        ------
        NonBreakingPrefixFileError
            when non breaking file for given language not exist in abbrev_sentence_tokenizer folder

        """

        self.non_breaking_prefix_file: Optional[str] = non_breaking_prefix_file
        self.__non_breaking_prefixes: dict
        self.pre_compiled_regexes: dict
        line: str
        prefix_type: int
        item: int

        if self.non_breaking_prefix_file is None:
            self.non_breaking_prefix_file = str(
                pathlib.Path(__file__).parent.resolve() / "tr_non_suffixes"
            )

        if not os.path.isfile(self.non_breaking_prefix_file):
            raise NonPrefixFileNotExistError(self.non_breaking_prefix_file)

        self.__non_breaking_prefixes = {}
        with open(self.non_breaking_prefix_file, mode='r', encoding='utf-8') as fp_prefix_file:
            for line in fp_prefix_file.readlines():

                if '#NUMERIC_ONLY#' in line:
                    prefix_type = SentenceTokenizer.PrefixType.NUMERIC_ONLY
                else:
                    prefix_type = SentenceTokenizer.PrefixType.DEFAULT

                # Remove comments
                line = re.sub(pattern=r'#.*', repl='', string=line, flags=re.DOTALL | re.UNICODE)

                line = line.strip()

                if not line:
                    continue

                self.__non_breaking_prefixes[line] = prefix_type

        prefix_type = SentenceTokenizer.PrefixType.DEFAULT
        for item in range(1, 10000):
            self.__non_breaking_prefixes[str(item)] = prefix_type

        # boost regex performance
        self.pre_compiled_regexes = {
            1: re.compile(
                r'([?!]) *([\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[\p{Uppercase_Letter}\p{Other_Letter}])',
                re.U
            ),
            2: re.compile(  # + changed to *
                r'(\.[\.]+) *([\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[\p{Uppercase_Letter}\p{Other_Letter}])',
                re.U
            ),
            3: re.compile(
                r'([?!\.][\ ]*[\'")\]\p{Final_Punctuation}]+) +([\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[\ ]*'
                r'[\p{Uppercase_Letter}\p{Other_Letter}])',
                re.U
            ),
            4: re.compile(
                r'([?!\.]) +([\'"[\u00bf\u00A1\p{Initial_Punctuation}]+[\ ]*[\p{Uppercase_Letter}\p{Other_Letter}])',
                re.U
            ),
            5: re.compile(r' +', re.U),
            6: re.compile(r'([\w\.\-]*)([\'\"\)\]\%\p{Final_Punctuation}]*)(\.+)$', re.U),
            7: re.compile(r'[\p{Uppercase_Letter}\p{Lowercase_Letter}\p{Other_Letter}\-]+', re.U),
            8: re.compile(r'(\.)[\p{Uppercase_Letter}\p{Other_Letter}\-]+(\.+)$', re.U),
            9: re.compile(r'^([ ]*[\'"([\u00bf\u00A1\p{Initial_Punctuation}]*[ ]*[\p{Uppercase_Letter}'
                          r'\p{Other_Letter}0-9])',
                          re.U),
            10: re.compile('^[0-9]+', re.U),
            11: re.compile(r' +'),
            12: re.compile(r'\n '),
            13: re.compile(r' \n ')
        }

    def tokenize(self, text: Optional[str], mode: Optional[str] = None) -> Tuple:
        """Sentence tokenize

        Parameters
        ----------
        text: str
            Text to be split into individual sentences
        mode: None, str
            if given as table, sentence tokenizer is performed only splitting text using enters (\n)
            other wise considers Turkish abbreviations and grammar rules

        Returns
        -------

        """

        words: list
        i: int
        w: list
        forward_word: str

        if text is None:
            return ()

        if not text:
            return ()

        if mode not in {'table', 'only_index'}:

            # Add sentence breaks as needed:

            # Non-period end of sentence markers (?!) followed by sentence starters
            text = self.pre_compiled_regexes[1].sub(repl='\\1\n\\2', string=text)

            # Multi-dots followed by sentence starters
            text = self.pre_compiled_regexes[2].sub(repl='\\1\n\\2', string=text)

            # Add breaks for sentences that end with some sort of punctuation inside a quote or parenthetical and are
            # followed by a possible sentence starter punctuation and upper case
            text = self.pre_compiled_regexes[3].sub(repl='\\1\n\\2', string=text)

            # Add breaks for sentences that end with some sort of punctuation are followed by a
            # sentence starter punctuation and upper case
            text = self.pre_compiled_regexes[4].sub(repl='\\1\n\\2', string=text)

            # Special punctuation cases are covered. Check all remaining periods
            words = self.pre_compiled_regexes[5].split(string=text)

            text = ''
            for i in range(0, len(words) - 1):
                match = self.pre_compiled_regexes[6].search(string=words[i])

                if match:
                    w = words[i].split('.')
                    if self.pre_compiled_regexes[7].search(string=w[-1]):
                        forward_word = w[-1]
                    else:
                        forward_word = words[i + 1]
                    prefix = match.group(1)
                    starting_punctuation = match.group(2)

                    def is_prefix_honorific(prefix_: str, starting_punct_: str) -> bool:
                        """Check if \\1 is a known honorific and \\2 is empty."""
                        if prefix_:
                            if prefix_ in self.__non_breaking_prefixes:
                                if self.__non_breaking_prefixes[prefix_] == SentenceTokenizer.PrefixType.DEFAULT:
                                    if not starting_punct_:
                                        return True
                        return False

                    if is_prefix_honorific(prefix_=prefix, starting_punct_=starting_punctuation):
                        # Not breaking
                        pass

                    elif self.pre_compiled_regexes[8].search(words[i]):
                        # Not breaking - upper case acronym
                        pass

                    elif self.pre_compiled_regexes[9].search(string=forward_word):
                        def is_numeric(prefix_: str, starting_punct_: str, next_word: str):
                            """The next word has a bunch of initial quotes, maybe a space, then either upper case or a
                            number."""
                            if prefix_:
                                if prefix_ in self.__non_breaking_prefixes:
                                    if self.__non_breaking_prefixes[prefix_] == \
                                            SentenceTokenizer.PrefixType.NUMERIC_ONLY:
                                        if not starting_punct_:
                                            if self.pre_compiled_regexes[10].search(string=next_word):
                                                return True
                            return False

                        if not is_numeric(prefix_=prefix, starting_punct_=starting_punctuation,
                                          next_word=forward_word):
                            if words[i + 1] == forward_word:
                                words[i] = ''.join([w[0], '.\n'])
                            else:
                                words[i] = ''.join(['.'.join(w[:-1]), '.\n', forward_word])
                        # We always add a return for these unless we have a numeric non-breaker and a number start
                text = ''.join([text, words[i], " "])

            # We stopped one token from the end to allow for easy look-ahead. Append it now.
            text = ''.join([text, words[-1]])
            text = self.pre_compiled_regexes[11].sub(repl=' ', string=text)
            text = self.pre_compiled_regexes[12].sub(repl='\n', string=text)
            text = self.pre_compiled_regexes[13].sub(repl='\n', string=text)
            text = text.strip()

        return tuple(text.split('\n'))


class WordTokenizer:
    __slots__ = 'pre_compiled_regexes'

    def __init__(self):
        suffixes: str
        numbers: str
        any_word: str
        punctuations: str

        suffixes = r"[a-zğçşöüı]{3,}' ?[a-zğçşöüı]+"
        numbers = r"%\d{2,}[.,:/\d-]+"
        any_word = r"[a-zğçşöüı_+%\.()@&`’/\\\d-]+"
        punctuations = r"[a-zğçşöüı]*[,!?;:]"
        self.pre_compiled_regexes = re.compile(
            "|".join(
                [suffixes,
                 numbers,
                 any_word,
                 punctuations
                 ]
            ), re.I
        )

    def tokenize(self, sentence: str) -> Tuple:
        words: Union[list, tuple]
        dots: str

        try:
            words = self.pre_compiled_regexes.findall(sentence)
        except (re.error, TypeError):
            return ()
        else:
            # If last word ends with dot, it should be another word
            words = tuple(words)
            if words:
                end_dots = re.search(r'\b(\.+)$', words[-1])
                if end_dots:
                    dots = end_dots.group(1)
                    words = words[:-1] + (words[-1][:-len(dots)],) + (dots,)
            return words
