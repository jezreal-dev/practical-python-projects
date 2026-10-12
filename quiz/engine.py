from typing import Any


class QuizError(ValueError):
    """Base exception for all quiz domain violations."""
    pass

class InvalidQuestionError(QuizError):
    """Raised when a question record violates schema invariants (server-side data error)."""
    pass

class InvalidSelectionError(QuizError):
    """Raised when a user provides an empty or invalid answer selection (client-side error)."""
    pass


# Validates the structure and content of a question dictionary
def validate_question(question: dict[str, Any]) -> None:
    prompt = question.get("prompt", "")
    topic = question.get("topic", "")
    difficulty = question.get("difficulty", "")
    options = question.get("options", [])
    answer = question.get("answer", "")

    if not isinstance(prompt, str) or not prompt.strip():
        raise InvalidQuestionError("Question prompt cannot be empty.")
    
    if not isinstance(topic, str) or not topic.strip():
        raise InvalidQuestionError("Question topic cannot be empty.")
    
    if not isinstance(difficulty, str) or not difficulty.strip():
        raise InvalidQuestionError("Question difficulty cannot be empty.")

    if not isinstance(options, list) or len(options) < 4:
        raise InvalidQuestionError("Question must have at least 4 options.")
    
    for opt in options:
        if not isinstance(opt, str) or not opt.strip():
            raise InvalidQuestionError("All options must be non-empty strings.")
    if answer not in options:
        raise InvalidQuestionError("Correct answer must be one of the provided options.")


# Evaluates the user's answer against the correct answer
def evaluate_answer(question: dict, user_answer: str) -> bool:
    validate_question(question)
    if not isinstance(user_answer, str) or not user_answer.strip():
        raise InvalidSelectionError("User answer cannot be empty.")

    return user_answer.strip().casefold() == question["answer"].strip().casefold()


# Calculates the score based on total questions and correct answers
def calculate_score(total_questions: int, correct_answers: int) -> dict[str, Any]:
    if total_questions <= 0:
        raise QuizError("Total questions must be greater than Zero")
    if correct_answers < 0 or correct_answers > total_questions:
        raise QuizError("Correct answers must be between 0 and total_questions.")

    percentage = round((correct_answers / total_questions) * 100, 2)
    return {
        "total": total_questions,
        "correct": correct_answers,
        "incorrect": total_questions - correct_answers,
        "percentage": percentage,
        "passed": percentage >= 50.0,
    }