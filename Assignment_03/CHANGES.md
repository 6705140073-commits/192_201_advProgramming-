# Assignment 03 — CHANGES

**Name:** Sai Lin Thant Maung 
  **Student ID:** 6705140073

## 1 · What I changed

| # | Code smell in the original | What I changed it to | OOP concept applied | How I verified behaviour was unchanged |
|---|---|---|---|---|
| 1 | Product information was stored as tuples | Created a `Product` class with name, price, and category | Classes / Encapsulation | Ran `python Assignment_03.py` → PASS |
| 2 | Customer tiers used many `if/elif` statements | Created `Customer`, `Silver`, `Gold`, and `Platinum` classes | Inheritance / Polymorphism | Ran the self-test → PASS |
| 3 | Order items were stored as tuples | Created an `OrderItem` class with product and quantity | Composition | Ran the self-test → PASS |
| 4 | Calculations were inside one large function | Separated subtotal, discount, tax, total, and points into methods | Separation of responsibilities | Ran `python Assignment_03.py` → PASS |
| 5 | There were magic numbers in the calculations | Added named constants such as `TAX_RATE`, `BULK_RATE`, and `POINTS_DIVISOR` | Clean code / Encapsulation | Ran the self-test → PASS |
| 6 | The original code used a global tax variable | Removed the global variable from the refactored section | Encapsulation | Ran the self-test → PASS |

## 2 · Short reflection

The change I found most useful was polymorphism. I created different classes for Silver, Gold, and Platinum customers instead of using many `if/elif` statements. This made the discount and points calculations easier for me to understand. I also separated the calculations into different methods, which made the code less confusing. The main thing I had to be careful about was keeping the original tax, discount, quantity, points, and receipt output exactly the same.

## 3 · Prompt log (Level 2 — required)

| # | My prompt to the AI | What it suggested | Accept / reject / edited | How I checked it |
|---|---|---|---|---|
| 1 | "Explain this Assignment 03 and guide me step by step." | Explained the OOP requirements and what needed to be changed | Accept | Checked the instructions and followed the steps |
| 2 | "How can I change the customer tier if/elif into classes?" | Suggested a Customer base class and Silver, Gold, and Platinum subclasses | Edited | Ran the self-test → PASS |
| 3 | "Help me separate the calculation methods." | Suggested separate subtotal, discount, tax, total, and points methods | Accept | Ran the program → PASS |
| 4 | "Check if my refactored code keeps the same behaviour." | Explained how to use the built-in self-test | Accept | `python Assignment_03.py` → PASS |

**Ownership statement.** By submitting, I confirm that I understand and can explain the code I submitted, and that this prompt log reflects my actual AI use.

## 4 · Before-you-submit checklist

- [yes] `python Assignment_03.py` prints **PASS**.
- [yes] No product tuples are used in the refactored section.
- [yes] Order items are objects.
- [yes] Customer tiers use classes.
- [yes] No `if tier == ...` chains are used.
- [yes] Calculation methods return values.
- [yes] Receipt printing is separate from calculations.
- [yes] Magic numbers are replaced with named constants.
- [yes] The refactored section has no leftover global tax variable.
- [yes] Constructors validate important values.
- [yes] The change table and reflection are completed.
- [yes] The prompt log is included.