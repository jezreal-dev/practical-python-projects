# Python Beginner-to-Medium Project Roadmap

A practical project-based roadmap for learning Python by building projects that are challenging enough to teach real programming skills without being overwhelming.

---

## How to Use This Roadmap

The projects are arranged progressively. Each project should introduce a few new concepts while reinforcing concepts learned previously.

### Recommended Learning Cycle

**Learn concept → Build feature → Get stuck → Research → Implement → Refactor → Add stretch feature**

Avoid following complete tutorials from start to finish. Instead, research specific problems when you get stuck.

For example:

> Instead of searching: "Build a Python expense tracker tutorial"

Search:

> "How to write JSON to a file in Python"

The goal is to learn how to solve problems, not copy complete solutions.

---

# Project Roadmap

| # | Project | Difficulty | Main Learning Areas |
|---|---|---|---|
| 1 | Expense Tracker | Beginner → Medium | Variables, lists, dictionaries, functions, loops, file handling |
| 2 | Quiz / Trivia Game | Beginner → Medium | Functions, conditionals, loops, dictionaries, scoring |
| 3 | Simple Banking System | Medium | OOP, functions, validation, state management |
| 4 | Library Management System | Medium | OOP, CRUD, data modeling, searching |
| 5 | To-Do CLI Application | Medium | JSON, file handling, CRUD, CLI interaction |
| 6 | Password Manager | Medium | File handling, dictionaries, modules, security concepts |
| 7 | Inventory Management System | Medium | OOP, CRUD, persistence, validation |
| 8 | Weather CLI Application | Medium | APIs, HTTP requests, JSON, error handling |
| 9 | Personal Finance Analyzer | Medium+ | CSV, data processing, calculations, modules |
| 10 | Command-Line Chat Application | Medium+ | Networking, sockets, client/server architecture |

---

# Stage 1 — Python Fundamentals

## Project 1: Expense Tracker

### Goal

Build a terminal application that allows a user to record and analyze personal expenses.

### Core Features

- Add an expense
- Specify amount
- Specify category
- Add a description
- View all expenses
- Calculate total spending
- Calculate spending by category
- Delete an expense
- Save expenses to a file
- Load expenses when the program starts

### Example Data Model

```python
{
    "amount": 5000,
    "category": "Food",
    "description": "Lunch"
}
```

### Learning Objectives

#### Python Fundamentals
- Variables
- Strings
- Integers and floats
- Lists
- Dictionaries
- `if/else`
- `for` and `while` loops

#### Functions
- Creating functions
- Parameters
- Return values
- Breaking a program into smaller functions

#### Data Structures
Learn how dictionaries and lists can represent real-world information.

#### File Handling
- Reading files
- Writing files
- Saving application data
- Loading application data

#### Problem Solving
Learn to answer questions such as:
- How should an expense be represented?
- How should totals be calculated?
- How can expenses be grouped by category?

### Stretch Goal

Store expenses as JSON instead of plain text and use Python's `json` module.

---

## Project 2: Quiz / Trivia Game

### Goal

Build a terminal-based quiz application that presents questions, accepts answers, calculates scores, and displays results.

### Core Features

- Display questions
- Display multiple-choice options
- Accept user answers
- Check answers
- Keep score
- Display final results
- Randomize questions

### Example Data Structure

```python
questions = [
    {
        "question": "What is 2 + 2?",
        "options": ["3", "4", "5", "6"],
        "answer": "4"
    }
]
```

### Learning Objectives

- Lists
- Dictionaries
- Loops
- Functions
- Conditionals
- String manipulation
- Randomization
- Input validation
- Program flow
- Separating data from program logic

### Key Concept

Learn to separate **data** from **logic** so that the program can operate on changing information without rewriting the core logic.

---

# Stage 2 — Structuring Programs

## Project 3: To-Do CLI Application

### Goal

Build a command-line task management application.

### Core Features

- Add task
- Delete task
- Mark task as completed
- Edit task
- View pending tasks
- View completed tasks
- Assign priority
- Add due dates
- Save tasks
- Load tasks

### Example Interface

```text
1. Add task
2. View tasks
3. Complete task
4. Edit task
5. Delete task
6. Filter tasks
7. Exit
```

### Learning Objectives

- JSON
- File persistence
- CRUD operations
- Functions
- Data structures
- Date/time handling
- Input validation
- Modular code organization

### Key Learning Outcome

Start thinking about how to structure an entire program rather than only solving individual coding problems.

---

## Project 4: Library Management System

### Goal

Build a system for managing a small library.

### Core Features

- Add books
- Remove books
- Search for books
- Register members
- Borrow books
- Return books
- View available books
- View borrowed books

### Suggested Data Model

```text
Book
├── title
├── author
├── ISBN
└── available

Member
├── name
├── member_id
└── borrowed_books
```

### Learning Objectives

- Object-oriented programming
- Data modeling
- Lists and dictionaries
- Functions
- Searching
- CRUD operations
- Relationships between objects
- Validation
- State management

### Key Learning Outcome

Begin thinking like a software developer by modeling real-world entities and their relationships.

---

# Stage 3 — Object-Oriented Programming

## Project 5: Simple Banking System

### Goal

Build a command-line banking application.

### Core Features

- Create an account
- Login
- Deposit money
- Withdraw money
- Check balance
- Transfer money
- View transaction history
- Exit

### Example Interface

```text
===== BANK =====

1. Create Account
2. Login
3. Deposit
4. Withdraw
5. Transfer
6. Transaction History
7. Exit
```

### Suggested Classes

```python
class Account:
    ...

class Bank:
    ...
```

### Learning Objectives

- Classes
- Objects
- Attributes
- Methods
- Constructors
- Encapsulation concepts
- Object interaction
- Validation
- Managing application state

### Key Learning Outcome

Learn to model real-world entities as objects.

For example, an account can contain:

- Account number
- Owner
- Balance
- Transactions

And provide behaviors such as:

- `deposit()`
- `withdraw()`
- `transfer()`

---

## Project 6: Inventory Management System

### Goal

Build software for managing inventory for a small shop.

### Product Model

```text
Product
├── ID
├── Name
├── Price
├── Quantity
└── Category
```

### Core Features

- Add product
- Remove product
- Update product
- Search product
- Sell product
- Restock product
- View inventory
- Calculate inventory value
- Find low-stock products

### Learning Objectives

- Object-oriented programming
- CRUD operations
- Data modeling
- File persistence
- Functions
- Error handling
- Searching and filtering
- Calculations
- Application structure

### Key Learning Outcome

Understand how real business software can be modeled and organized.

---

# Stage 4 — External Data and APIs

## Project 7: Weather CLI Application

### Goal

Build a terminal application that retrieves weather information from a weather API.

### Example Interaction

```text
Enter city: Ibadan
```

### Example Output

```text
Ibadan Weather

Temperature: 27°C
Humidity: 72%
Condition: Cloudy
Wind: 10 km/h
```

### Learning Objectives

- HTTP requests
- APIs
- JSON
- External data
- API keys
- Environment variables
- Error handling
- Reading API documentation

### Key Learning Outcome

Move from programs that only use locally created data to programs that communicate with external systems.

---

## Project 8: Personal Finance Analyzer

### Goal

Build a program that analyzes a CSV file containing financial transactions.

### Example Input

```text
Date,Category,Amount
2026-08-01,Food,5000
2026-08-02,Transport,2500
2026-08-03,Food,3000
```

### Questions Your Program Should Answer

- How much did I spend?
- Which category costs the most?
- What is my average daily spending?
- Which month had the highest spending?
- What percentage went to food?
- What were my biggest transactions?

### Learning Objectives

- CSV files
- Data processing
- `datetime`
- Aggregation
- Sorting
- Filtering
- Functions
- Modules

### Stretch Goal

After implementing the first version with standard Python, rebuild the analysis using **Pandas**.

---

# Stage 5 — Medium+ Projects

## Project 9: Password Manager

### Goal

Build a local password-management application for learning purposes.

### Core Features

- Add credentials
- Search credentials
- Delete credentials
- Generate passwords
- Save credentials locally
- Retrieve credentials

### Learning Objectives

- File handling
- JSON
- Modules
- Random password generation
- Data structures
- Error handling
- Basic security concepts
- Hashing
- Encryption concepts
- Environment variables

### Important Note

Treat your first version as a learning project, not as a production-ready password manager. Real password managers require careful security engineering.

---

## Project 10: Command-Line Chat Application

### Goal

Build a simple client/server chat application.

### Basic Architecture

```text
             Server
            /  |             /   |             /    |         Client A Client B Client C
```

Multiple clients should be able to connect to the server and exchange messages.

### Learning Objectives

- Networking
- Sockets
- Client/server architecture
- Concurrency
- Threads
- Message handling
- Error handling
- Basic system architecture

### Key Learning Outcome

Understand how different programs communicate with one another over a network.

---

# Recommended Learning Progression

## Stage 1 — Python Fundamentals

1. Expense Tracker
2. Quiz / Trivia Game

↓

## Stage 2 — Structuring Programs

3. To-Do CLI Application
4. Library Management System

↓

## Stage 3 — Object-Oriented Programming

5. Banking System
6. Inventory Management System

↓

## Stage 4 — Working With External Data

7. Weather API
8. Personal Finance Analyzer

↓

## Stage 5 — Bigger Systems

9. Password Manager
10. Chat Application

---

# Project Difficulty Progression

```text
                    ┌──────────────────────┐
                    │  Python Fundamentals │
                    └──────────┬───────────┘
                               │
                  Expense Tracker / Quiz
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Program Structure    │
                    └──────────┬───────────┘
                               │
                 To-Do / Library System
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Object-Oriented Code │
                    └──────────┬───────────┘
                               │
                Banking / Inventory System
                               │
                               ▼
                    ┌──────────────────────┐
                    │ External Systems     │
                    └──────────┬───────────┘
                               │
                   APIs / Data Analysis
                               │
                               ▼
                    ┌──────────────────────┐
                    │ Medium+ Applications │
                    └──────────┬───────────┘
                               │
                   Chat / Security Projects
```

---

# Rules for Getting the Most From Each Project

## 1. Don't Build Everything From a Tutorial

Try to solve the problem yourself first.

When you get stuck, research the **specific concept** you're missing.

Good:

> How do I save a Python dictionary to JSON?

Less useful:

> Complete Python expense tracker tutorial.

---

## 2. Don't Look for the Perfect Solution Immediately

Getting stuck is part of the learning process.

Try:

1. Understand the problem.
2. Break it into smaller problems.
3. Attempt a solution.
4. Read error messages.
5. Search for the specific concept you don't understand.
6. Implement the solution.
7. Refactor your code.

---

## 3. Build the Minimum Version First

Don't start with every feature.

For example, for the Expense Tracker:

### Version 1

- Add expense
- View expenses
- Calculate total

### Version 2

- Delete expenses
- Categories
- Filtering

### Version 3

- Save to file
- Load from file

### Version 4

- JSON
- Better validation
- Better CLI

### Version 5

- Stretch features

This prevents the project from becoming overwhelming.

---

# Recommended First Project

If you are **just starting Python**, begin with:

## Expense Tracker

It provides an excellent balance between difficulty and learning.

You will encounter:

**Variables → Data Structures → Conditions → Loops → Functions → File Handling → JSON → Error Handling → Program Structure**

without immediately throwing you into advanced concepts.

Once you can build that project largely by yourself, move to the Quiz Game and then the To-Do application.

---

# Core Learning Philosophy

The objective isn't to finish 10 projects.

The objective is to progressively develop the ability to:

```text
Understand a problem
       ↓
Break it into smaller problems
       ↓
Choose appropriate data structures
       ↓
Design the program
       ↓
Write the code
       ↓
Debug errors
       ↓
Research unknown concepts
       ↓
Refactor
       ↓
Add new functionality
```

That process is what turns Python knowledge into actual programming ability.
