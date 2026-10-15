Interaction #1 — Python Exceptions

**Problem:**
I wanted to understand how Python handles invalid input and how
`try`, `except`, and `ValueError` work together.

**My initial understanding:**
I knew that `int()` could convert text containing a whole number
into an integer, but I wanted to understand what happens when the
text cannot be converted.

**Prompt to AI:**
Explain Python's `try`, `except`, and `ValueError` using a small
example that converts valid and invalid text into integers.

**Useful AI guidance:**
The `try` block contains code that might raise an exception.
The `except ValueError` block handles an invalid conversion so
the program can respond instead of terminating unexpectedly.

**My independent experiment:**
I wrote `experiment_exceptions.py`. The program tries to convert
`"25"` and `"hello"` into integers, using separate exception
handling blocks.

**Verification result:**
When I ran the experiment, `"25"` was converted into the integer
25. Converting `"hello"` raised a `ValueError`, and the exception
handler printed an error message.

**Decision:**
The experiment confirmed that valid numeric text can be converted
into an integer, while invalid numeric text needs to be handled.

**What I can now explain without AI:**
The `try` block attempts an operation that could fail. If converting
the text raises `ValueError`, Python runs the matching `except`
block. This allows the program to handle invalid input gracefully.

**Related file:** `experiment_exceptions.py`




Interaction #2 — Input Validation

**Problem:**  
I wanted to understand how to validate the number of users affected by a ticket.

**My initial understanding:**  
I knew that Python could convert input into an integer, but I wanted to understand how to reject invalid numbers and values that break our project requirements.

**Prompt to AI:**  
How can I validate the number of users affected by a ticket, making sure the input is a whole number greater than zero?

**Useful AI guidance:**  
`try/except ValueError` catches errors when Python cannot convert the input into an integer. An `if` statement checks the business rule that the number of affected users must be greater than zero.

**My independent experiment:**  
I created `experiment_validation.py` and tested five inputs: 5, 0, -3, hello, and 2.5. I predicted that positive integers would be accepted, zero and negative numbers would be rejected, and text or decimal input would produce an error message.

**Verification result:**  
I ran the program and confirmed that all five inputs behaved as expected.

**Decision:**  
The experiment confirmed that input conversion and business-rule validation are different tasks. Both are necessary to validate the affected-users field correctly.

**What I can now explain without AI:**  
The `try` block attempts to convert the input into an integer. The `except ValueError` block handles input that cannot be converted. The `if` statement checks whether the converted number is greater than zero.

**Related file:** `experiment_validation.py`