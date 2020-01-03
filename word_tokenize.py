def word_tokenize(_sentence):
    """
    Splits given sentence into words using regex.

    Args:
        _sentence(str): a sentence.

    Returns:
        list: word of given sentence. Some punctations (., !?; : )
        are evaluated as words with considering Turkish semantics.

        """

    word_pattern = re.compile(r"\w{2,15}' ?\w{1,4}|[\w{1,2}./-]+|[\d.,]+|\w+|[.,!?;:]")
    return word_pattern.findall(str(_sentence))
