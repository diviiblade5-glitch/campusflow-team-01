import unittest

from campusflow.quiz import QUESTIONS, score_answers


class TestEngineeringQuiz(unittest.TestCase):
    def test_quiz_has_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)

    def test_all_correct_answers_score_six(self):
        answers = [question["answer"] for question in QUESTIONS]
        self.assertEqual(score_answers(answers), 6)

    def test_all_wrong_answers_score_zero(self):
        answers = [
            next(letter for letter in question["options"]
                 if letter != question["answer"])
            for question in QUESTIONS
        ]
        self.assertEqual(score_answers(answers), 0)

    def test_partial_score(self):
        answers = [question["answer"] for question in QUESTIONS]
        answers[0] = next(
            letter for letter in QUESTIONS[0]["options"]
            if letter != QUESTIONS[0]["answer"]
        )
        self.assertEqual(score_answers(answers), 5)

    def test_empty_answers_score_zero(self):
        self.assertEqual(score_answers([]), 0)


if __name__ == "__main__":
    unittest.main()
