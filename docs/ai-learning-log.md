## Interaction #1 — Python Exceptions

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




## Interaction #2 — Input Validation

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



## Interaction #3 — Debugging a CLI Integration Bug

### Problem

After Engineer A's and Engineer B's work was integrated, the
CampusFlow command-line menu displayed duplicate option numbers.

The menu showed both "Add a follow-up note" and "Search tickets"
as option 7. It also showed both "View ticket notes" and
"Engineering Understanding Check" as option 8.

The menu advertised only 10 options even though the application
had 12 distinct actions.

### My Initial Understanding

I understood that the menu needed to include the new search and
quiz features, but I needed to investigate why the numbering was
inconsistent and whether the selection logic matched the displayed
options.

### Prompt to AI

Help me investigate the duplicate menu numbering after integrating
two developers' work. Explain how the printed menu and the input
selection logic can become inconsistent, and how to verify the fix.

### Useful AI Guidance

AI explained that printing a menu and handling a user's selection
are separate operations. Python can print duplicate option numbers
without raising an error, so the application may start normally
even when the menu is confusing or incorrect.

AI also recommended inspecting the relevant code and checking
the menu numbering against the selection conditions.

### My Investigation

I inspected the menu output and examined the Git diff for
`main.py`.

The diff showed that the input prompt had been changed from
accepting options 1-10 to accepting options 1-12. It also showed
inconsistent numbering in the selection conditions and repeated
search-related statements.

### Correction

I corrected the menu numbering so that each of the 12 actions
has a unique number. I also updated the input prompt to accept
options 1-12 and aligned the relevant selection conditions
with the corrected numbering.

### Verification

I manually displayed the menu and confirmed that it showed
12 uniquely numbered options.

I tested the exit option and confirmed that the application
saved the tickets and displayed a goodbye message.

I then ran the automated test suite:

`python3 -m unittest discover -s tests -v`

Result: 81 tests passed.

The automated tests provide evidence that the tested quiz,
search, storage, ticket validation, notes, priority queue,
reporting, and workflow behaviours passed.

However, passing unit tests alone does not prove that every
CLI menu option works correctly. Each menu option should also
be tested manually or through dedicated CLI tests.

### What I Learned

I learned that a successful Git merge does not guarantee that
the integrated application behaves correctly.

When multiple developers modify shared files, the team must
check that the new code works with the existing code. For a
CLI menu, this means keeping the displayed options and the
selection logic synchronized.

I also learned to use Git diffs to investigate what changed
instead of guessing which edit caused a problem.

### Prevention

In future integrations, I will:

1. Inspect changes to shared files before merging.
2. Keep menu numbering and selection conditions synchronized.
3. Check for duplicated statements after resolving changes.
4. Run the full automated test suite after integration.
5. Test the CLI menu options to verify that each invokes
   the correct feature.

### Critical Evaluation of AI Assistance

AI suggested that inconsistent menu numbering and duplicated
statements could result from integration changes. I checked
the actual Git diff and menu output to investigate these
suggestions rather than accepting them without evidence.

The investigation supported the conclusion that the integrated
code contained inconsistent numbering and repeated statements.
However, I did not establish the exact edit or commit that
introduced each problem.

This taught me to use AI as a debugging aid while relying
on code inspection and test results to verify conclusions.