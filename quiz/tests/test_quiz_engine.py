import pytest
from engine import (
    QuizError,
    InvalidQuestionError,
    InvalidSelectionError,
    filter_questions,
    get_topic_counts,
    prepare_quiz_deck,
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


# --- Helper Fixture for Question Bank ---

@pytest.fixture
def sample_bank():
    return [
        {"id": 1, "topic": "Python", "difficulty": "easy", "prompt": "Q1?", "options": ["A", "B", "C", "D"], "answer": "A"},
        {"id": 2, "topic": "Python", "difficulty": "hard", "prompt": "Q2?", "options": ["A", "B", "C", "D"], "answer": "B"},
        {"id": 3, "topic": "System Design", "difficulty": "medium", "prompt": "Q3?", "options": ["A", "B", "C", "D"], "answer": "C"},
        {"id": 4, "topic": "Cognitive Thinking", "difficulty": "hard", "prompt": "Q4?", "options": ["A", "B", "C", "D"],"answer": "D"}
    ]


# --- 4. Topic Count & Filtering Tests ---

def test_get_topic_counts(sample_bank):
    # Act:
    counts = get_topic_counts(sample_bank)

    # Assert:
    assert counts["Python"] == 2
    assert counts["System Design"] == 1
    assert counts["Cognitive Thinking"] == 1


def test_filter_questions_by_topic_and_difficulty(sample_bank):
    # Act & Assert 1 (Topic filter - case and whitespace insensitive):
    py_questions = filter_questions(sample_bank, topic="  python ")
    assert len(py_questions) == 2

    # Act & Assert 2 (Difficulty filter):
    hard_questions = filter_questions(sample_bank, difficulty="HARD")
    assert len(hard_questions) == 2

    # Act & Assert 3 (Combined topic + difficulty filter):
    combined = filter_questions(sample_bank, topic="Python", difficulty="hard")
    assert len(combined) == 1
    assert combined[0]["id"] == 2


def test_filter_questions_empty_filter_fails(sample_bank):
    # Act & Assert 1 (Empty topic string):
    with pytest.raises(QuizError):
        filter_questions(sample_bank, topic="   ")

    # Act & Assert 2 (Empty difficulty string):
    with pytest.raises(QuizError):
        filter_questions(sample_bank, difficulty="")


# --- 5. Deck Preparation & Anti-Repetition Tests ---

def test_prepare_quiz_deck_limit_seeding_and_immutability(sample_bank):
    # Arrange:
    original_ids = [q["id"] for q in sample_bank]

    # Act:
    deck_a = prepare_quiz_deck(sample_bank, limit=2, seed=42) 
    deck_b = prepare_quiz_deck(sample_bank, limit=2, seed=42)

    # Assert:
    assert len(deck_a) == 2
    assert deck_a == deck_b
    assert [q["id"] for q in sample_bank] == original_ids


def test_prepare_quiz_deck_excludes_seen_questions_first(sample_bank):
    # Arrange:
    seen_ids = {1, 2, 3}

    # Act 1 (Request only 1 question - should pick the only unseen question, ID 4):
    deck_unseen = prepare_quiz_deck(sample_bank, limit=1, seed=10, exclude_ids=seen_ids)

    # Assert 1:
    assert len(deck_unseen) == 1
    assert deck_unseen[0]["id"] == 4

    # Act 2 (Request 3 questions - should place ID 4 first, then backfill from seen_ids):
    deck_backfill = prepare_quiz_deck(sample_bank, limit=3, seed=10, exclude_ids=seen_ids)

    # Assert 2:
    assert len(deck_backfill) == 3
    assert deck_backfill[0]["id"] == 4


def test_prepare_quiz_deck_invalid_limit_fails(sample_bank):
    # Act & Assert:
    with pytest.raises(QuizError):
        prepare_quiz_deck(sample_bank, limit=0)

    with pytest.raises(QuizError):
        prepare_quiz_deck(sample_bank, limit=-5)