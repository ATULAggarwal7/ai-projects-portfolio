# Python Coding Guidelines

## 1. Naming Convention

Use snake_case for:

- variables
- functions

Correct:

get_user_data()
calculate_total_price()

Incorrect:

getUserData()

---

## 2. Function Length

Functions should not exceed **50 lines**.

---

## 3. Docstrings

Every function must include a docstring explaining its purpose.

Example:

def get_user_data():
    """
    Fetch user data from database
    """

---

## 4. Code Readability

Code should be:

- readable
- self explanatory
- use meaningful variable names

Avoid:

x = 5

Prefer:

user_count = 5

---

## 5. Avoid Global Variables

Global variables should be avoided.

---

## 6. Single Responsibility

Each function should do **one task only**.