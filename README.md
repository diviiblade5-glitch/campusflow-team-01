# CampusFlow

CampusFlow is a Python command-line helpdesk application for
creating and managing campus support tickets.

## Features

- Create tickets with validated input.
- Calculate ticket priority automatically.
- Assign tickets to staff members.
- Update ticket status and reopen resolved tickets.
- View the priority queue.
- Generate ticket reports.
- Add follow-up notes to tickets.
- View notes associated with a ticket.
- Save and load tickets using JSON.

## Requirements

- Python 3
- Python standard library

No third-party packages are required for the current CLI.

## Run the Application

From the project root, run:

```bash
python3 main.py
```

Follow the numbered menu to manage tickets.

## Run the Tests

Run all automated tests with:

```bash
python3 -m unittest discover -s tests -v
```

## Ticket Priorities

Priority is calculated using urgency and the number of affected users.

The rules are evaluated in this order:

- **Critical:** High urgency and at least 10 affected users.
- **High:** High urgency or at least 10 affected users, unless the
  ticket already qualifies as critical.
- **Medium:** Medium urgency or at least 3 affected users, unless the
  ticket qualifies for a higher priority.
- **Low:** All other valid combinations.

## Ticket Notes

Notes are associated with individual tickets.

Each note contains:

- `note_id`
- `author`
- `message`

Authors cannot be blank. Messages must contain between 5 and
300 characters after trimming surrounding whitespace.

Notes can be added to open or in-progress tickets. Resolved tickets
must be reopened before receiving new notes.

## JSON Storage

Tickets are stored in:

`data/tickets.json`

The storage format is a JSON list containing ticket objects.
Each ticket contains its ticket fields and a `notes` list.

The application starts with an empty collection if the storage file
does not exist. Invalid saved data should be rejected rather than
silently accepted.

## Project Structure

- `main.py` — command-line interface.
- `campusflow/tickets.py` — ticket validation, creation, and priority.
- `campusflow/workflow.py` — assignment, status changes, and notes.
- `campusflow/storage.py` — JSON persistence and saved-data validation.
- `tests/` — automated tests.
- `docs/` — project documentation and learning records.

## Development Notes

This project uses Python's built-in `unittest` framework and standard
library modules. See the `docs/` folder for development records.