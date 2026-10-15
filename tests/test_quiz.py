import unittest

from campusflow.quiz import QUESTIONS, score_answers, run_quiz


class TestEngineeringQuiz(unittest.TestCase):

    def test_quiz_has_six_questions(self):
        self.assertEqual(len(QUESTIONS), 6)

    def test_all_correct_answers_score_six(self):
        answers = [q["answer"] for q in QUESTIONS]
        self.assertEqual(score_answers(answers), 6)

    def test_all_wrong_answers_score_zero(self):
        self.assertEqual(score_answers(["X"] * 6), 0)

    def test_partial_score(self):
        answers = [q["answer"] for q in QUESTIONS]
        answers[0] = "X"
        self.assertEqual(score_answers(answers), 5)

    def test_empty_answers_score_zero(self):
        self.assertEqual(score_answers([]), 0)

    def test_invalid_choice_is_rejected_and_retried(self):
        answers = iter([
            "X",
            "B", "An unassigned ticket cannot start work",
            "C", "An empty report should return zero",
            "D", "C", "A", "B",
        ])
        messages = []

        score, explanations = run_quiz(
            input_fn=lambda prompt: next(answers),
            print_fn=messages.append,
        )

        self.assertIn(
            "Invalid choice. Enter A, B, C, or D.",
            messages,
        )
        self.assertEqual(score, 6)
        self.assertEqual(len(explanations), 2)


if __name__ == "__main__":
    unittest.main()
