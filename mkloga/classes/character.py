class Character:
    def __init__(self, character, button_id):
        self.character = character
        self.button_id = button_id

    def __eq__(self, other):
        if type(other) is Character:
            return self.character == other.character
        return False
