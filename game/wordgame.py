"""File containing the WordGame class."""
from urllib import request

class WordGame:
    """
    A class designed for Mycroft AI to generate hints for a game
    which asks the user to guess a "secret word".
    """
    def __init__(self, word_data_path):
        """
        Initialization

        Parameters
        __________
        word_row : pandas.core.series.Series
            Data used for the case when there is no connection to the internet
            or for faster information retrieval.
            Each row contains:
            + the word
            + synonyms (WordNet)
            + category (one hypernym from WordNet)
            + the definition (WordNet)
        """
        self.word_data = pd.read_csv(word_data_path)

        sample = self.word_data.sample(n=1)
        self.word_row = sample.iloc[0]

        self._word_data_path = word_data_path

    def hints(self):
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
        hints = {
            "length": self._word_length_hint(),
            "letter": self._first_letter_hint(),
            "category": self._category_hint(),
            "synonyms": self._synonyms_hint(),
            "definition": self._wiktionary_hint()
        }
        return hints

    def _word_length_hint(self):
        """
        Calculates and returns the length of the word in characters

        Returns
        _______
        int
            Length of the word in characters.
        """
        word_row = self.word_row
        name = word_row.word
        return len(name)

    def _first_letter_hint(self):
        """
        Finds and returns the first character of the word

        Returns
        _______
        str
            The first character of the word.
        """
        word_row = self.word_row
        word = word_row.word
        return word[0]

    def _category_hint(self):
        """
        Returns the animal's category

        Returns
        _______
        str
            The word's category, represented as a string.
        """
        word_row = self.word_row
        category = word_row.category
        return category

    def _synonyms_hint(self):
        """
        Finds and returns synonyms, according to WordNet.

        Returns
        _______
        synonyms : list[str]
            Synonyms.
        """
        word_row = self.word_row
        synonyms_string = word_row.synonyms
        if isinstance(synonyms_string, float):
            return None
        synonyms = [syn.replace('_', ' ') for syn in synonyms_string.split()]
        return synonyms[:3] # we need no more than three.

    def _wiktionary_hint(self):
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
        word_row = self.word_row
        definition = word_row.definition
        return definition