from mycroft import MycroftSkill, intent_file_handler


class MycroftWordGame(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('game.word.mycroft.intent')
    def handle_game_word_mycroft(self, message):
        self.speak_dialog('game.word.mycroft')


def create_skill():
    return MycroftWordGame()

