from urllib import request

class WordGame:
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
        self.word2id = {word: i for i, word in enumerate(self.backup_words)}

    # TODO: check whether pandas row contain ids (name attribute?)
    def hints(self, word_id):
        word_row = self.word_data.T[word_id]
        hints = (
            self._word_length_hint(word_row),
            self._first_letter_hint(word_row),
            self._pos_hint(word_row),
            self._coocurence_hint(word_row),
            self._semantics_hint(word_row),
            self._wiktionary_hint(word_row)
        )
        return hints

    def _word_length_hint(self, word_row):
        return len(word_row[0])

    def _first_letter_hint(self, word_row):
        return word_row[0][0]

    def _pos_hint(self, word, word_id):
        pass

    def _coocurence_hint(self, word, word_id):
        pass

    def _semantics_hint(self, word, word_id):
        pass

    def _wiktionary_hint(self, word, word_id):
        pass

    def _check_internet_connection(self, host='http://google.com'):
        try:
            request.urlopen(host)
            return True
        except request.URLError: 
            return False

    def _offline_game(self):
        pass