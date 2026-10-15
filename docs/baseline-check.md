# CampusFlow Baseline Check

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