import random
import threading
import time

words = []
phrases = []

MENU = "menu"
GAME = "game"
GAMEOVER = "gameover"
life_remaining = 6
guessed_letters = []
wrong_letters = []
mistakes = 0
current_word = ""
word_state = []
timeout = 0

timer = None


def setup(mode):
    global current_word
    global word_state

    start_timer(15)

    if mode == "basic":
        current_word = choose_word()
    elif mode == "intermediate":
        current_word = choose_phrase()

    if word_state == []:
        for i in current_word:
            word_state.append("_")


def choose_word() -> str:
    if words == []:
        with open("./datasets/cleaned_data.txt", "r") as f:
            for data in f:
                words.append(data.strip())
    random_number = random.randrange(0, len(words))
    return words[random_number]


def choose_phrase() -> str:
    if phrases == []:
        with open("./datasets/phrases.txt", "r") as f:
            for data in f:
                phrases.append(data.strip())
    random_number = random.randrange(0, len(phrases))
    return phrases[random_number]


def guess_letters(letter):
    global word_state
    global guessed_letters
    global life_remaining

    reset_timer(15)

    word_state = []

    guessed_letters.append(letter)

    if letter not in current_word.upper():
        life_remaining -= 1

    for i in current_word.upper():
        if i in guessed_letters:
            word_state.append(i)
        else:
            word_state.append("_")

    print("From Core: ", word_state)


def reduce_life():
    global life_remaining
    life_remaining -= 1


def start_timer(seconds):
    global timer, timeout

    if timer:
        timer.cancel()
    timeout = seconds
    countdown()


def countdown():
    global timer, timeout
    print(timeout)

    timeout -= 1
    if timeout >= 1:
        timer = threading.Timer(1.0, countdown)
        timer.start()
    else:
        reduce_life()


def game_over():
    global timeout, guessed_letters, mistakes, current_word, word_state, life_remaining

    timeout = 0
    guessed_letters = []
    mistakes = 0
    current_word = ""
    word_state = []
    life_remaining = 6

def reset_timer(seconds):
    start_timer(seconds)
