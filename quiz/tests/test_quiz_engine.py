import pytest
from engine import (
    QuizError,
    InvalidQuestionError,
    InvalidSelectionError,
    validate_question,
    evaluate_answer,
    calculate_score,
)

# --- Helper Fixture or Sample Data ---

@pytest.fixture
def sample_question():
    return {
        "id": 1,
        "topic": "Geography",
        "difficulty": "easy",
        "prompt": "What is the capital of France?",
        "options": ["London", "Berlin", "Paris", "Madrid"],
        "answer": "Paris"
    }

# --- 1. Question Validation Tests ---

def test_validate_question_valid(sample_question):
    # Arrange: Take a valid question dictionary.
    question = sample_question

    # Act & Assert: Call validate_question(question) -> should not raise any error.
    validate_question(question)

def test_validate_question_empty_difficulty_fails(sample_question):
    # Arrange: Copy valid question, set "difficulty" to "".
    question = sample_question.copy()
    question["difficulty"] = ""
    # Act & Assert: Use pytest.raises(InvalidQuestionError) when calling validate_question.
    with pytest.raises(InvalidQuestionError):
        validate_question(question)

def test_validate_question_empty_prompt_fails(sample_question):
    # Arrange: Copy valid question, set "prompt" to "   ".
    question = sample_question.copy()
    question["prompt"] = "   "
    # Act & Assert: Use pytest.raises(InvalidQuestionError) when calling validate_question.
    with pytest.raises(InvalidQuestionError):
        validate_question(question)


def test_validate_question_empty_topic_fails(sample_question):
    # Arrange: Copy valid question, set "topic" to "".
    question = sample_question.copy()
    question["topic"] = ""
    # Act & Assert: Use pytest.raises(InvalidQuestionError) when calling validate_question.
    with pytest.raises(InvalidQuestionError):
        validate_question(question)


def test_validate_question_fewer_than_four_options_fails(sample_question):
    # Arrange: Copy valid question, set "options" to ["Paris", "London", "Berlin"] (only 3).
    question = sample_question.copy()
    question["options"] = ["Paris", "London", "Berlin"]
    # Act & Assert: Use pytest.raises(InvalidQuestionError) when calling validate_question.
    with pytest.raises(InvalidQuestionError):
        validate_question(question)


def test_validate_question_answer_not_in_options_fails(sample_question):
    # Arrange: Copy valid question, set "answer" to "Rome" (not in the 4 options).
    question = sample_question.copy()
    question["answer"] = "Rome"
    # Act & Assert: Use pytest.raises(InvalidQuestionError) when calling validate_question.
    with pytest.raises(InvalidQuestionError):
        validate_question(question)

# --- 2. Answer Evaluation Tests ---


def test_evaluate_answer_correct_exact_and_case_insensitive(sample_question):
    # Arrange: Take valid question (where answer is "Paris").
    question = sample_question

    # Act & Assert:
    assert evaluate_answer(question, "Paris") is True
    assert evaluate_answer(question, "  paris ") is True

def test_evaluate_answer_incorrect(sample_question):
    # Arrange: Take valid question.
    question = sample_question

    # Act & Assert:
    assert evaluate_answer(question, "London") is False

def test_evaluate_answer_empty_input_fails(sample_question):
    # Arrange: Take valid question.
    question = sample_question

    # Act & Assert:
    with pytest.raises(InvalidSelectionError):
        evaluate_answer(question, "   ")

# --- 3. Score Calculation Tests ---

def test_calculate_score_passing_and_failing():
    # Act & Assert (Passing case):
    result_pass = calculate_score(total_questions=10, correct_answers=8)
    assert result_pass["total"] == 10
    assert result_pass["correct"] == 8
    assert result_pass["incorrect"] == 2
    assert result_pass["percentage"] == 80.0
    assert result_pass["passed"] is True

#  Act & Assert (Failing case):
    result_fail = calculate_score(total_questions=10, correct_answers=3)
    assert result_fail["percentage"] == 30.0
    assert result_fail["passed"] is False

def test_calculate_score_invalid_inputs_fail():
    # Act & Assert:
    # 1. Zero total questions:
    #    Use pytest.raises(QuizError) -> calculate_score(0, 0)
    with pytest.raises(QuizError):
        calculate_score(0, 0)

    # 2. Negative correct answers:
    #    Use pytest.raises(QuizError) -> calculate_score(5, -1)
    with pytest.raises(QuizError):
        calculate_score(5, -1)

    # 3. Correct answers greater than total:
    #    Use pytest.raises(QuizError) -> calculate_score(5, 6)
    with pytest.raises(QuizError):
        calculate_score(5, 6)