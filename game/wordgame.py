"""File containing the WordGame class."""
from urllib import request

class WordGame:
    """
    A class designed for Mycroft AI to generate hints for a game
    which asks the user to guess a "secret word".
    """
    def __init__(self, word_data):
        """
        Initialization

        Parameters
        __________
        word_data : pandas.DataFrame
            Data used for the case when there is no connection to the internet
            or for faster information retrieval.
            Each row contains:
            + the word
            + the POS tag
            + the most similar word
            + the definition from wiktionary
        """
        self._connected_to_internet = self._check_internet_connection()
        self.word_data = word_data
        self.word2id = {word: i for i, word in enumerate(self.word_data)}

    # TODO: check whether pandas row contain ids (name attribute?)
    def hints(self, word_id):
        """
        Produces hints for the word id.

        Parameters
        __________
        word_id : int
            Word index in the vocabulary.
        
        Returns
        _______
        hints : tuple[int, str, str, list[str], str, str]
            A tuple of hints. The tuple respectively contains:
            + the word's length
            + the first letter
            + the most similar word
            + definition from Wordnet
        """
        word_row = self.word_data.T[word_id]
        hints = (
            self._word_length_hint(word_row),
            self._first_letter_hint(word_row),
            self._pos_hint(word_row),
            self._semantics_hint(word_row),
            self._wiktionary_hint(word_row)
        )
        return hints

    def _word_length_hint(self, word_row):
        """
        Calculates and returns the length of the word in characters

        Parameters
        __________
        word_row : pandas.core.series.Series
            A row from the dataframe, which corresponds to the secret word.

        Returns
        _______
        int
            Length of the word in characters.
        """
        return len(word_row['word'])

    def _first_letter_hint(self, word_row):
        """
        Finds and returns the first character of the word

        Parameters
        __________
        word_row : pandas.core.series.Series
            A row from the dataframe, which corresponds to the secret word.

        Returns
        _______
        str
            The first character of the word.
        """
        return word_row['word'][0]

    def _pos_hint(self, word_row):
        """
        Returns the word's part of speech

        Parameters
        __________
        word_row : pandas.core.series.Series
            A row from the dataframe, which corresponds to the secret word.
        
        Returns
        _______
        str
            The word's part of speech, represented as a string.
        """
        pass

    def _semantics_hint(self, word_row):
        """
        Finds and returns the closest word in terms of distributional semantics.

        Parameters
        __________
        word_row : pandas.core.series.Series
            A row from the dataframe, which corresponds to the secret word.
        
        Returns
        _______
        closest_word : str
            The closest word.
        """
        pass

    def _wiktionary_hint(self, word_row):
        """
        Retrieves and returns the definition of the word.

        Parameters
        __________
        word_row : pandas.core.series.Series
            A row from the dataframe, which corresponds to the secret word.
        
        Returns
        _______
        definition : str
            The word's definition.
        """
        pass

    def _check_internet_connection(self, host='http://google.com'):
        try:
            request.urlopen(host)
            return True
        except request.URLError: 
            return False

    def _offline_game(self):
        pass