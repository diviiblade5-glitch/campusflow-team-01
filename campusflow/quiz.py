"""Engineering Understanding Check for CampusFlow."""


QUESTIONS = [
    {
        "question": "An unassigned open ticket is moved to in_progress. What should happen?",
        "options": {
            "A": "Accept the change",
            "B": "Reject the change without modifying the ticket",
            "C": "Resolve the ticket",
            "D": "Assign a random staff member",
        },
        "answer": "B",
    },
    {
        "question": "What is the resolution percentage when there are zero tickets?",
        "options": {
            "A": "100%",
            "B": "Undefined; crash the program",
            "C": "0%",
            "D": "50%",
        },
        "answer": "C",
    },
    {
        "question": "How should combined search filters behave?",
        "options": {
            "A": "Match any supplied filter",
            "B": "Ignore the title",
            "C": "Use only the last filter",
            "D": "Require every supplied filter to match",
        },
        "answer": "D",
    },
    {
        "question": "Can a note be added to a resolved ticket?",
        "options": {
            "A": "Yes, at any time",
            "B": "Only if the message is short",
            "C": "No, reopen the ticket first",
            "D": "Only if the author is an administrator",
        },
        "answer": "C",
    },
    {
        "question": "A JSON file contains duplicate ticket IDs. What should loading do?",
        "options": {
            "A": "Reject the file and preserve current in-memory tickets",
            "B": "Delete all tickets",
            "C": "Silently keep the duplicate IDs",
            "D": "Rename tickets randomly",
        },
        "answer": "A",
    },
    {
        "question": "A pull request changes validation but adds no negative tests. What is the best review response?",
        "options": {
            "A": "Approve immediately",
            "B": "Request focused tests and an explanation of the behavior",
            "C": "Delete the validation",
            "D": "Ignore the change",
        },
        "answer": "B",
    },
]


def score_answers(answers):
    """Return the number of correct answers."""
    return sum(
        answer == question["answer"]
        for question, answer in zip(QUESTIONS, answers)
    )


def run_quiz(input_fn=input, print_fn=print):
    """Run the quiz, retry invalid choices, and collect two explanations."""
    answers = []
    explanations = []

    for index, question in enumerate(QUESTIONS, start=1):
        print_fn(f"\nQuestion {index}: {question['question']}")
        for letter, option in question["options"].items():
            print_fn(f"  {letter}. {option}")

        while True:
            answer = input_fn("Your answer (A/B/C/D): ").strip().upper()
            if answer in question["options"]:
                break
            print_fn("Invalid choice. Enter A, B, C, or D.")

        answers.append(answer)

        if index <= 2:
            explanation = input_fn(
                "Briefly explain your reasoning: "
            ).strip()
            explanations.append({
                "question": index,
                "answer": answer,
                "explanation": explanation,
            })

    score = score_answers(answers)
    print_fn(f"\nQuiz score: {score}/6")

    print_fn("\nExplanations for mentor discussion:")
    for item in explanations:
        print_fn(
            f"Q{item['question']} ({item['answer']}): "
            f"{item['explanation']}"
        )

    return score, explanations
