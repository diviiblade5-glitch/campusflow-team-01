Interaction #1 — Python exceptions

Problem: I wanted to understand how Python handles invalid input.
Initial understanding: Write what you understood before this experiment.
Prompt to AI: I asked for a small example explaining try, except, and ValueError.
Experiment: I converted "25" and "hello" to integers inside separate exception-handling blocks.
Verification: Record the output you actually observed.
Decision: Explain whether the experiment confirmed your understanding.
What I can now explain: Describe in your own words why the second conversion fails and how except handles it.




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