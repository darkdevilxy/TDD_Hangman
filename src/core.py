import random

words = []


class Engine:
    def __init__(self) -> None:
        pass
    
    def setup(self, mode):
        if mode == "basic":
            word = self.choose_word()
        elif mode == "intermediate":
            phrase = self.choose_phrase()

    def choose_word(self) -> str:
        if words == []:
            with open("./datasets/cleaned_data.txt", "r") as f:
                for data in f:
                    words.append(data.strip())
        random_number = random.randrange(0, len(words) - 1)
        return words[random_number]

    def choose_phrase(self) -> str:
        return ""


class GameState:
    MENU = "menu"
    GAME = "game"
    life_remaining = 1
    guessed_letters = []
    wrong_letters = []
    timeout = 0
    mode = "basic"
    mistakes = 0
