import re

def word_tokenize(sentence):
    """
    

    Args:
        sentence (str): any sentence.

    Returns:
        list: each item is a word.

    """
    
    
    acronym_each_dot = r"(?:[a-zğçşöüı]\.){2,}"
    acronym_end_dot = r"\b[a-zğçşöüı]{2,3}\."
    suffixes = r"[a-zğçşöüı]{3,}' ?[a-zğçşöüı]{0,3}"
    numbers = r"\d+[.,:\d]+"
    any_word = r"[a-zğçşöüı]+"
    punctuations = r"[a-zğçşöüı]*[.,!?;:]"
    word_regex = "|".join([acronym_each_dot,
                           acronym_end_dot,
                           suffixes,
                           numbers,
                           any_word,
                           punctuations])
    
    return re.compile("%s"%word_regex, re.I).findall(sentence)
