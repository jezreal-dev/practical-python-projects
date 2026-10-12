import time
from question_bank import QUESTION_BANK
from engine import get_topic_counts, filter_questions, prepare_quiz_deck, evaluate_answer, calculate_score

time_limit = 30.0  # seconds
option_letters = ["A", "B", "C", "D"]

class ActionCanceled(Exception):
    """Raised when the user cancels an action."""
    pass

def clear_screen() -> None:
    print("\033[H\033[2J", end="", flush=True)

# Prompts the user to select a topic from the question bank, returning the selected topic or None for all topics
def select_topic(question_bank) -> str | None:
    clear_screen()
    topic_counts = get_topic_counts(question_bank)
    topics = sorted(topic_counts.keys())
    print("Select a topic:")
    print(f"0. All Topics ({sum(topic_counts.values())} questions)")

    for i, topic in enumerate(topics, start=1):
        print(f"{i}. {topic} ({topic_counts[topic]} questions)")

    while True:
        try:
            user_input = input("Enter the number of your choice (or 'q' to cancel): ").strip()
            if user_input.lower() == 'q':
                raise ActionCanceled
            index = int(user_input)
            if index == 0:
                return None
            elif 1 <= index <= len(topics):
                return topics[index - 1]
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to cancel.")


# Evaluates the user's answer against the correct answer for a given question, returning True if correct, False otherwise
def select_difficulty() -> str | None:
    clear_screen()
    print("Select difficulty:")
    print("0. All")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")

    while True:
        try:
            user_input = input("Enter the number of your choice (or 'q' to cancel): ").strip()
            if user_input.lower() == 'q':
                raise ActionCanceled
            index = int(user_input)
            if index == 0:
                return None
            elif index == 1:
                return "easy"
            elif index == 2:
                return "medium"
            elif index == 3:
                return "hard"
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to cancel.")


# Prompts the user to select a limit for the number of questions in the quiz, returning the selected limit or a default value
def select_question_limit(available_count: int) -> int:
    clear_screen()
    print("Select question limit:")
    print("0. 15 questions")
    print("1. 25 questions")
    print("2. 50 questions")

    while True:
        try:
            user_input = input("Enter the number of your choice (or 'q' to cancel): ").strip()
            if user_input.lower() == 'q':
                raise ActionCanceled
            index = int(user_input)
            if index == 0:
                return 15
            elif index == 1:
                return 25
            elif index == 2:
                return 50
            else:
                print("Invalid selection. Please try again.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to cancel.")


# Prompts the user to select an answer option (A, B, C, D) or quit, returning the selected option and elapsed time
def prompt_answer_letter(options: list[str]) -> tuple[str, float] | None:
    start_time = time.monotonic()
    
    while True:
        raw = input("Your answer (A; B; C; D or 'q' to quit round): ").strip().upper()
        if raw == "Q":
            return None
        if raw in ["A", "B", "C", "D"]:
            elapsed = round(time.monotonic() - start_time, 2)
            index = ["A", "B", "C", "D"].index(raw)
            return (options[index], elapsed)
        print("Invalid choice. Please enter A, B, C, D, or 'q'.")


# Evaluates the user's answer against the correct answer for a given question, returning True if correct, False otherwise
def run_quiz_round(deck: list[dict], seen_ids: set[int]) -> None:
    correct_count = 0
    total_answered = 0
    total_time = 0.0

    for index, question in enumerate(deck, start=1):
        print(f"\nQuestion {index}/{len(deck)} | Topic: {question['topic']} | Difficulty: {question['difficulty'].capitalize()}")
        print(question["prompt"])

        for letter, option_text in zip(option_letters, question["options"]):
            print(f"{letter}. {option_text}")

        result = prompt_answer_letter(question["options"])
        if result is None:
            print("Ending round early...")
            break
        selected_option_text, elapsed = result
        seen_ids.add(question["id"])
        total_answered += 1
        total_time += elapsed

        if elapsed > time_limit:
            print(f"Time expired! ({elapsed}s > {time_limit}s). Correct answer: {question['answer']}")
        elif evaluate_answer(question, selected_option_text):
            correct_count += 1
            print(f"Correct! ({elapsed}s)")
        else:
            print(f"Incorrect! ({elapsed}s). Correct answer: {question['answer']}")

    if total_answered > 0:
        score = calculate_score(total_answered, correct_count)
        avg_time = round(total_time / total_answered, 2)
        print(f"\nFinal Scoreboard:")
        print(f"Total Questions Answered: {score['total']}")
        print(f"Correct Answers: {score['correct']}")
        print(f"Incorrect Answers: {score['incorrect']}")
        print(f"Percentage: {score['percentage']}%")
        print(f"Status: {'PASSED' if score['passed'] else 'FAILED'}")
        print(f"Average Time per Question: {avg_time} seconds")


def main():
    # question_bank = load_question_bank()
    seen_ids = set()

    while True:
        clear_screen()
        print("\n--- Quiz Menu ---")
        print("1. Start New Quiz Round")
        print("2. View Topic Breakdown")
        print(f"3. Reset Seen Questions History (currently {len(seen_ids)}/{len(QUESTION_BANK)} seen)")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            try:
                topic = select_topic(QUESTION_BANK)
                difficulty = select_difficulty()
                filtered_pool = filter_questions(QUESTION_BANK, topic=topic, difficulty=difficulty)
                if not filtered_pool:
                    print("No questions found for that filter combination.")
                    continue
                limit = select_question_limit(len(filtered_pool))
                deck = prepare_quiz_deck(filtered_pool, limit=limit, exclude_ids=seen_ids)
                run_quiz_round(deck, seen_ids)
            except ActionCanceled:
                print("Quiz setup canceled. Returning to main menu...")
        
        elif choice == "2":
            clear_screen()
            counts = get_topic_counts(QUESTION_BANK)
            print("\n--- Topic Breakdown ---")
            for topic, count in sorted(counts.items()):
                print(f"{topic}: {count} questions")
        
        elif choice == "3":
            # Implement reset seen questions history logic
            seen_ids.clear()
            print("Seen questions history reset.")
        
        elif choice == "4":
            print("Thank you for playing!")
            raise ActionCanceled
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")
        input("\nPress [Enter] to return to the main menu...")

if __name__ == "__main__":
    try:
        main()
    except ActionCanceled:
        print("Exiting the quiz application. Goodbye!")