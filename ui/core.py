import random
words = []

def setup(mode):
    if mode == "basic":
        word = choose_word()
    elif mode == "intermediate":
        phrase = choose_phrase()


def choose_word() -> str:
    if words == []:
        with open("./../datasets/cleaned_data.txt", "r") as f:
            for data in f:
                words.append(data.strip())  
    random_number = random.randrange(0, len(words) - 1)
    return words[random_number]

def choose_phrase() -> str:
    return ""