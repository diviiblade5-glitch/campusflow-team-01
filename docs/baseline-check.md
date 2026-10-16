# CampusFlow Baseline Check

<<<<<<< HEAD
## Purpose

This document separates the original application baseline from
the checks performed after implementing validation and notes.

The original baseline should reflect the application at the audited
commit before the new features were introduced. Results must be
recorded from actual test runs and manual checks.

## Environment

- Language: Python 3
- Interface: Command-line interface
- Persistence: JSON
- Automated testing: `unittest`

## Original Baseline

The original baseline results have not yet been recorded in this
document. They must be verified against the original audited commit
rather than inferred from the updated application.

Record the following after checking out the appropriate commit in
a safe, separate worktree:

| Check | Result | Evidence |
|---|---|---|
| Original automated tests | Pending verification | Test output |
| Create a ticket | Pending verification | Input and output |
| Invalid ticket input | Pending verification | Input and output |
| Load saved tickets | Pending verification | Input and output |
|Formal audit findings | Not available | The team was not audited before time ran out |
| Check | Result | Evidence |
|---|---|---|
| Original automated tests | PASS | 25 tests passed at commit `89e1dcc` |
| Create a ticket | PASS | Created T001 with high priority |
| Invalid affected-users input | PASS | Rejected zero with a validation error |
| Load saved tickets | PASS | Restarted and loaded one saved ticket |
| Priority queue | PASS | Displayed T001 as an unresolved ticket |
| Improvements identified by the audit | Pending verification | Audit findings |

## Current Development Checks

The following results were recorded after implementing validation,
workflow improvements, notes, and JSON persistence.

| Check | Result | Evidence |
|---|---|---|
| Ticket validation tests | PASS | `tests/test_tickets.py` |
| Priority calculation tests | PASS | `tests/test_tickets.py` |
| Ticket workflow tests | PASS | `tests/test_workflow.py` |
| Note validation tests | PASS | `tests/test_workflow.py` |
| JSON persistence tests | PASS | `tests/test_storage.py` |
| Manual note display | PASS | Viewed notes for T001 |
| Full automated test suite | PASS | 61 tests passed |
| Note persistence after restart | PASS | Added N005, saved, restarted, and verified all five notes |

## Commands

Run the test suite with:

```bash
python3 -m unittest discover -s tests -v
=======
## Existing functionality
- Ticket creation and validation.
- Ticket assignment and status workflow.
- Priority queue.
- Search by title with optional category, status, and priority filters.
- Ticket reports, including resolution percentage.
- JSON ticket storage.

## Verification
Command:
`python3 -m unittest discover -s tests -v`

Latest observed result: 43 tests passed.

Command:
`python3 -m py_compile main.py campusflow/quiz.py`

Latest observed result: completed without errors.

## Outstanding work
- Confirm and integrate the ticket notes implementation.
- Verify the complete CLI manually.
- Complete the required peer review and Git integration.
- Verify the learning log and final submission details.
>>>>>>> 34f314e98ddcee8ac0a058d03c5116c4c13fd717


## Implementation Progress and Verification

### Features Implemented

- Ticket creation with input validation and automatic ticket IDs.
- Ticket priority calculation based on urgency and affected users.
- Ticket assignment with staff-name validation.
- Ticket status workflow supporting open, in_progress, and resolved.
- Protection against starting work on unassigned tickets.
- Priority queue that excludes resolved tickets and sorts tickets by priority.
- Ticket reports covering status, priority, categories, and resolution statistics.
- Ticket notes with validation, unique note IDs, and restrictions on resolved tickets.
- JSON persistence for saving and loading tickets.
- Validation of saved ticket data to reject invalid records.
- Ticket searching with title, category, status, and priority filters.
- Engineering knowledge quiz with answer validation and scoring.

### Testing and Verification

- Automated test suite executed using Python's unittest framework.
- Total tests passed: 81.
- Test failures: 0.
- Python compilation check completed successfully.
- Git whitespace check completed successfully using `git diff --check`.

### Documentation

- Updated the AI learning log.
- Updated the design decisions document.
- Added and maintained automated tests for ticket validation, workflow,
  persistence, reporting, searching, notes, and the engineering quiz.

### Remaining Submission Tasks

- Review the final changes before committing.
- Commit and push the verified changes to the feature branch.
- Confirm that the GitHub pull request contains the latest changes.
- Verify the required peer review, approval, and merge evidence.
- Prepare to explain the implementation and demonstrate the application
  during the engineering audit.