import random
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


# Returns a dictionary with counts of questions per topic
def get_topic_counts(question_bank: list[dict[str, Any]]) -> dict[str, int]:
    counts = {}
    for question in question_bank:
        validate_question(question)
        topic = question["topic"].strip()
        counts[topic] = counts.get(topic, 0) + 1
    return counts


# Filters questions based on topic and difficulty, returning a list of matching questions
def filter_questions(
    question_bank: list[dict[str, Any]], 
    topic: str | None = None, 
    difficulty: str | None = None
) -> list[dict[str, Any]]:
    if topic is not None and (not isinstance(topic, str) or not topic.strip()):
        raise QuizError("Topic filter cannot be an empty string.")
    if difficulty is not None and (not isinstance(difficulty, str) or not difficulty.strip()):
        raise QuizError("Difficulty filter cannot be an empty string.")

    filtered = []
    for quest in question_bank:
        validate_question(quest)

        if topic is not None:
            if quest["topic"].strip().casefold() != topic.strip().casefold():
                continue

        if difficulty is not None:
            if quest["difficulty"].strip().casefold() != difficulty.strip().casefold():
                continue
        filtered.append(quest)
    return filtered


# Prepares a quiz deck by shuffling the question bank and applying an optional limit
def prepare_quiz_deck(
    question_bank: list[dict[str, Any]],
    limit: int | None = None,
    exclude_ids: set[int] | None = None,
    seed: int | None = None,
) -> list[dict[str, Any]]:
    if limit is not None and limit <= 0:
        raise QuizError("Question limit must be greater than zero.")
    for quest in question_bank:
        validate_question(quest)

    excluded = exclude_ids or set()
    unseen = [quest for quest in question_bank if quest.get("id") not in excluded]
    seen = [quest for quest in question_bank if quest.get("id") in excluded]

    rng = random.Random(seed)
    rng.shuffle(unseen)
    rng.shuffle(seen)

    deck = unseen + seen

    if limit is not None:
        return deck[:limit]
    return deck



