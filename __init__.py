from mycroft import MycroftSkill, intent_file_handler

from .game.wordgame import WordGame
import random
import os   
import json


class MycroftWordGame(MycroftSkill):

    GAME_FILE_DIR = "cache"
    GAME_FILE_NAME = "current_game.json"
    DATA_FILE = "cache/wordnet-animals.csv"

    def __init__(self):
        MycroftSkill.__init__(self)
    
    def initialize(self):
        self.register_entity_file('animal.entity')
        self.log.info(self.file_system.path)
        # Create cache if it does not exist
        if not self.file_system.exists(self.GAME_FILE_DIR):
            os.mkdir(os.path.join(
                self.file_system.path,
                self.GAME_FILE_DIR
            ))
        # Create game file if it does not exist.
        if not self.file_system.exists(os.path.join(self.GAME_FILE_DIR, 
                                                    self.GAME_FILE_NAME)):
            self.start_new_game()
        # Read in file where current game data is stored.
        self.game_dict = self.read_current_game_file()

    def read_current_game_file(self) -> dict:
        path = os.path.join(
            self.file_system.path,
                            self.GAME_FILE_DIR,
                            self.GAME_FILE_NAME
        )
        with self.file_system.open(path, "r") as file:
            game_dict = json.load(file)
        return game_dict

    def start_new_game(self) -> None:
        # Path to data file
        path = os.path.join(
            self.file_system.path,
                            self.GAME_FILE_DIR,
                            self.GAME_FILE_NAME
        )
        # Choose word for animal
        data_path = os.path.join(self.root_dir, self.DATA_FILE)
        word_game = WordGame(data_path)
        word_game.answer
        animal = word_game.answer
        hints = word_game.hints()
        game_dict = {
            "animal": animal, 
            "no_guesses": 0,
            "hints": hints,
            "given_hints": []
        }
        with self.file_system.open(path, "w") as file:
            json.dump(game_dict, file)
        self.game_dict = game_dict
        return None

    def update_game_data(self):
        path = os.path.join(
            self.file_system.path,
                            self.GAME_FILE_DIR,
                            self.GAME_FILE_NAME
        )
        with self.file_system.open(path, "w") as file:
            json.dump(self.game_dict, file)
        return None

    def get_hint_template(self, hint_key):
        templates = {
            "length": "The animal's name has {} letters",
            "letter": " The first letter is {}",
            "category": "The animal is a {}",
            "synonyms": "Another way to call this animal is {}",
            "definition": "This is how I would describe the animal: {}"
        }   
        return templates[hint_key]

    def hint_utterance(self):
        hint_dict = self.game_dict["hints"]
        given = self.game_dict["given_hints"]
        available_hints = list(set(hint_dict).difference(given))
        available_hints = [h for h in available_hints if hint_dict[h]is not None]
        self.log.info("Available hints: {}".format(available_hints))
        if not available_hints:
            return "Out of hints. Try to guess."
        new_hint = random.choice(available_hints)
        template_str = self.get_hint_template(new_hint)
        hint_value = hint_dict[new_hint]
        hint_utterance = template_str.format(hint_value)
        self.game_dict["given_hints"] = given + [new_hint]
        self.update_game_data()
        return hint_utterance

    @intent_file_handler('game.word.mycroft.intent')
    def handle_game_word_mycroft(self, message):
        self.start_new_game() # Clear all previous data.
        # Logging.
        animal = self.game_dict["animal"]
        no_guess = self.game_dict["no_guesses"]
        self.log.info("New game: Animal={}, Number of guess={}".format(animal, no_guess))
        # Ask if user wants to hear the rules.
        yes_no_response = self.ask_yesno("game.word.mycroft")
        if yes_no_response == "yes":
            self.speak_dialog(("Okay. In this game, you have to try and guess an animal. \
                               I will give you hints until I run out."))
        # Give first hint.
        self.speak_dialog("Alright, let's start.")
        hint_utt = self.hint_utterance()
        self.speak(hint_utt)

    @intent_file_handler('guess.word.intent')
    def handle_guessing(self, message):
        # Logging:
        animal = self.game_dict["animal"]
        no_guess = self.game_dict["no_guesses"]
        self.log.info("New game: Animal={}, Number of guess={}".format(animal, no_guess))
        # Get guess from user utterances.
        animal_guess = message.data.get("animal")
        if self.game_dict["animal"] in animal_guess or animal_guess in self.game_dict["animal"]:
            self.speak("Congratulations! You won. The animal I was looking for was {}".format(self.game_dict["animal"]))
        else:
            self.game_dict["no_guesses"] += 1
            self.update_game_data()
            self.speak("No sorry, I dont think it is {}".format(animal_guess))
            if self.game_dict["no_guesses"] >= 8:
                self.speak("Sorry, that was too many guesses. You lost. The answer was {}".format(self.game_dict["animal"]))
            else:
                hint_utt = self.hint_utterance()
                self.speak(hint_utt)

    @intent_file_handler("dont_know.intent")
    def handle_dont_know(self, message):
        self.speak("Okay, let me think.")
        hint_utt = self.hint_utterance()
        self.speak(hint_utt)
    
    @intent_file_handler("give_up.intent")
    def handle_give_up(self, message):
        animal = self.game_dict["animal"]
        self.speak("Okay, Here is the answer: The animal I was looking for is: {}".format(animal))


def create_skill():
    return MycroftWordGame()

