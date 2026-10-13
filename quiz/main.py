import json
from pathlib import Path
import time
from engine import get_topic_counts, filter_questions, prepare_quiz_deck, evaluate_answer, calculate_score, load_question_bank

time_limit = 30.0  # seconds
option_letters = ["A", "B", "C", "D"]
Questions_file = Path(__file__).parent / "questions.json"


class ActionCanceled(Exception):
    """Raised when the user cancels an action."""
    pass


def clear_screen() -> None:
    print("\033[H\033[2J", end="", flush=True)


def select_topic(question_bank) -> str | None:
    clear_screen()
    topic_counts = get_topic_counts(question_bank)
    topics = sorted(topic_counts.keys())
    print("=== Select a Topic ===")
    print(f"0. All Topics ({sum(topic_counts.values())} questions)")

    for i, topic in enumerate(topics, start=1):
        print(f"{i}. {topic} ({topic_counts[topic]} questions)")

    while True:
        try:
            user_input = input("\nEnter choice number (or 'q' to cancel): ").strip()
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


def select_question_limit(available_count: int) -> int:
    clear_screen()
    print("=== Select Question Count ===")
    print(f"Available questions in pool: {available_count}\n")
    print("1. 15 questions")
    print("2. 25 questions")
    print("3. 50 questions")
    print(f"4. All ({available_count} questions)")

    while True:
        try:
            user_input = input("\nEnter choice (1-4, or 'q' to cancel): ").strip()
            if user_input.lower() == 'q':
                raise ActionCanceled
            if user_input == "1":
                return min(15, available_count)
            elif user_input == "2":
                return min(25, available_count)
            elif user_input == "3":
                return min(50, available_count)
            elif user_input == "4":
                return available_count
            else:
                print("Invalid selection. Please choose 1, 2, 3, or 4.")
        except ValueError:
            print("Invalid input. Please enter a number or 'q' to cancel.")


def prompt_answer_letter(options: list[str]) -> tuple[str, float] | None:
    start_time = time.monotonic()

    while True:
        raw = input("Your answer (A / B / C / D, or 'q' to quit round): ").strip().upper()
        if raw == "Q":
            return None
        if raw in ["A", "B", "C", "D"]:
            elapsed = round(time.monotonic() - start_time, 2)
            index = ["A", "B", "C", "D"].index(raw)
            return (options[index], elapsed)
        print("Invalid choice. Please enter A, B, C, D, or 'q'.")


def run_quiz_round(deck: list[dict], seen_ids: set[int]) -> None:
    correct_count = 0
    total_answered = 0
    total_time = 0.0

    for index, question in enumerate(deck, start=1):
        clear_screen()
        print(f"=== Question {index}/{len(deck)} | Topic: {question['topic']} | Difficulty: {question['difficulty'].capitalize()} ===")
        print(f"\n{question['prompt']}\n")

        for letter, option_text in zip(option_letters, question["options"]):
            print(f"  {letter}) {option_text}")
        print()

        result = prompt_answer_letter(question["options"])
        if result is None:
            print("\nEnding round early...")
            input("Press [Enter] to see results...")
            break

        selected_option_text, elapsed = result
        seen_ids.add(question["id"])
        total_answered += 1
        total_time += elapsed

        print()
        if elapsed > time_limit:
            print(f"⏰ Time expired! ({elapsed}s > {time_limit}s). Correct answer: {question['answer']}")
        elif evaluate_answer(question, selected_option_text):
            correct_count += 1
            print(f"✅ Correct! ({elapsed}s)")
        else:
            print(f"❌ Incorrect! ({elapsed}s). Correct answer: {question['answer']}")

        if index < len(deck):
            input("\nPress [Enter] for next question...")

    if total_answered > 0:
        clear_screen()
        score = calculate_score(total_answered, correct_count)
        avg_time = round(total_time / total_answered, 2)
        print("========================================")
        print("            FINAL SCOREBOARD            ")
        print("========================================")
        print(f"Total Questions Answered: {score['total']}")
        print(f"Correct Answers:          {score['correct']}")
        print(f"Incorrect Answers:        {score['incorrect']}")
        print(f"Percentage:               {score['percentage']}%")
        print(f"Status:                   {'PASSED' if score['passed'] else 'FAILED'}")
        print(f"Average Time per Question:{avg_time} seconds")
        print("========================================")


def main():
    question_bank = load_question_bank(Questions_file)
    seen_ids = set()

    while True:
        clear_screen()
        print("========================================")
        print("           QUIZ & TRIVIA GAME           ")
        print("========================================")
        print("1. Start New Quiz Round")
        print("2. View Topic Breakdown")
        print(f"3. Reset Seen Questions History ({len(seen_ids)}/{len(question_bank)} seen)")
        print("4. Exit")
        print("========================================")

        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            try:
                topic = select_topic(question_bank)
                filtered_pool = filter_questions(question_bank, topic=topic)
                if not filtered_pool:
                    print("No questions found for that topic.")
                    input("\nPress [Enter] to return to the main menu...")
                    continue
                limit = select_question_limit(len(filtered_pool))
                deck = prepare_quiz_deck(filtered_pool, limit=limit, exclude_ids=seen_ids)
                run_quiz_round(deck, seen_ids)
            except ActionCanceled:
                print("\nQuiz setup canceled. Returning to main menu...")
        
        elif choice == "2":
            clear_screen()
            counts = get_topic_counts(question_bank)
            print("=== Topic Breakdown ===")
            for t, count in sorted(counts.items()):
                print(f"  {t}: {count} questions")
            print(f"\nTotal: {sum(counts.values())} questions across {len(counts)} topics.")

        elif choice == "3":
            seen_ids.clear()
            print("\nSeen questions history reset.")

        elif choice == "4":
            print("\nThank you for playing!")
            raise ActionCanceled

        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")

        input("\nPress [Enter] to return to the main menu...")


if __name__ == "__main__":
    try:
        main()
    except ActionCanceled:
        print("\nExiting the quiz application. Goodbye!")
