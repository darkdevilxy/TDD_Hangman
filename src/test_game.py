import unittest
import time
import threading
import core  # assume your code is saved in core.py


class TestWordcore(unittest.TestCase):

    def setUp(self):
        core.words = ["python", "hangman", "test"]
        core.phrases = ["machine learning", "data science"]
        core.game_over()  # reset state before each test

    def test_choose_word(self):
        word = core.choose_word()
        self.assertIn(word, core.words)

    def test_choose_phrase(self):
        phrase = core.choose_phrase()
        self.assertIn(phrase, core.phrases)

    def test_setup_basic(self):
        core.setup("basic")
        self.assertIn(core.current_word, core.words)
        self.assertEqual(len(core.word_state), len(core.current_word))
        self.assertTrue(all(ch == "_" for ch in core.word_state))

    def test_setup_intermediate(self):
        core.setup("intermediate")
        self.assertIn(core.current_word, core.phrases)
        self.assertEqual(len(core.word_state), len(core.current_word))
        self.assertTrue(all(ch == "_" or ch == " " for ch in core.word_state))

    def test_guess_correct_letter(self):
        core.current_word = "PYTHON"
        core.word_state = ["_", "_", "_", "_", "_", "_"]
        core.guessed_letters = []
        core.guess_letters("P")

        self.assertIn("P", core.word_state)

    def test_guess_wrong_letter(self):
        core.current_word = "PYTHON"
        core.word_state = ["_", "_", "_", "_", "_", "_"]
        core.life_remaining = 6
        core.guessed_letters = []

        core.guess_letters("Z")
        self.assertEqual(core.life_remaining, 5)

    def test_timer_reduces_life(self):
        core.life_remaining = 6
        core.start_timer(1)  # short timer for test
        time.sleep(2)  # wait until timer expires
        self.assertEqual(core.life_remaining, 5)

    def test_reset_core(self):
        core.current_word = "PYTHON"
        core.life_remaining = 3
        core.word_state = ["P", "_", "_"]
        core.guessed_letters = ["P"]

        core.game_over()

        self.assertEqual(core.life_remaining, 6)
        self.assertEqual(core.current_word, "")
        self.assertEqual(core.word_state, [])
        self.assertEqual(core.guessed_letters, [])


if __name__ == "__main__":
    unittest.main()
