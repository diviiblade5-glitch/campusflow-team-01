"""JSON storage and validation helpers for CampusFlow tickets."""

import json
from pathlib import Path

from campusflow.tickets import validate_ticket, calculate_priority

DEFAULT_PATH = Path("data/tickets.json")

VALID_STATUSES = {"open", "in_progress", "resolved"}
PRIORITIES = {"critical", "high", "medium", "low"}


def validate_saved_ticket(ticket):
    """Validate one complete ticket loaded from JSON."""

    if not isinstance(ticket, dict):
        raise ValueError("Each saved ticket must be a JSON object.")

    required_fields = {
        "id",
        "title",
        "category",
        "urgency",
        "affected_users",
        "priority",
        "status",
        "assigned_to",
        "notes",
    }

    if not required_fields.issubset(ticket):
        raise ValueError("A saved ticket is missing required fields.")

    ticket_id = ticket["id"]

    if (
        not isinstance(ticket_id, str)
        or len(ticket_id) < 2
        or not ticket_id.startswith("T")
        or not ticket_id[1:].isdigit()
        or int(ticket_id[1:]) < 1
    ):
        raise ValueError("A saved ticket has an invalid ticket ID.")

    details = validate_ticket(
        ticket["title"],
        ticket["category"],
        ticket["urgency"],
        ticket["affected_users"],
    )

    if details != {
       "title": ticket["title"],
       "category": ticket["category"],
       "urgency": ticket["urgency"],
       "affected_users": ticket["affected_users"],
    }:
      raise ValueError(
        f"Ticket {ticket_id} contains unnormalized details."
      )


    expected_priority = calculate_priority(
        details["urgency"],
        details["affected_users"],
    )

    if (
       not isinstance(ticket["priority"], str)
       or ticket["priority"] not in PRIORITIES
    ):
        raise ValueError(f"Ticket {ticket_id} has an invalid priority.")

    if ticket["priority"] != expected_priority:
        raise ValueError(
            f"Ticket {ticket_id} has an incorrect priority."
        )

    if (
       not isinstance(ticket["status"], str)
       or ticket["status"] not in VALID_STATUSES
    ):
       raise ValueError(f"Ticket {ticket_id} has an invalid status.")

    assigned_to = ticket["assigned_to"]

    if assigned_to is not None and (
        not isinstance(assigned_to, str) or not assigned_to.strip()
    ):
        raise ValueError(
            f"Ticket {ticket_id} has an invalid staff assignment."
        )

    if ticket["status"] == "in_progress" and assigned_to is None:
        raise ValueError(
            f"Ticket {ticket_id} is in progress but has no assignee."
        )

    notes = ticket["notes"]

    if not isinstance(notes, list):
        raise ValueError(f"Ticket {ticket_id} notes must be a list.")

    note_ids = set()

    for note in notes:
        if not isinstance(note, dict):
            raise ValueError(
                f"Ticket {ticket_id} contains an invalid note."
            )

        if set(note) != {"note_id", "author", "message"}:
            raise ValueError(
                f"Ticket {ticket_id} contains a malformed note."
            )

        note_id = note["note_id"]

        if (
            not isinstance(note_id, str)
            or len(note_id) < 2
            or not note_id.startswith("N")
            or not note_id[1:].isdigit()
            or int(note_id[1:]) < 1
        ):
            raise ValueError(
                f"Ticket {ticket_id} contains an invalid note ID."
            )

        if note_id in note_ids:
            raise ValueError(
                f"Ticket {ticket_id} contains duplicate note IDs."
            )

        note_ids.add(note_id)

        author = note["author"]
        message = note["message"]

        if not isinstance(author, str) or not author.strip():
            raise ValueError(
                f"Ticket {ticket_id} contains an invalid note author."
            )

        if (
            not isinstance(message, str)
            or not 5 <= len(message.strip()) <= 300
        ):
            raise ValueError(
                f"Ticket {ticket_id} contains an invalid note message."
            )

    return True


def validate_tickets(tickets):
    """Validate the entire ticket collection before returning it."""

    if not isinstance(tickets, list):
        raise ValueError("Ticket data must contain a JSON list.")

    ticket_ids = set()

    for ticket in tickets:
        validate_saved_ticket(ticket)

        ticket_id = ticket["id"]

        if ticket_id in ticket_ids:
            raise ValueError(f"Duplicate ticket ID: {ticket_id}")

        ticket_ids.add(ticket_id)

    return tickets


def save_tickets(tickets, path=DEFAULT_PATH):
    """Validate and save tickets to a JSON file."""

    validate_tickets(tickets)

    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(path=DEFAULT_PATH):
    """Load and validate saved tickets."""

    file_path = Path(path)

    if not file_path.exists():
        return []

    try:
        with file_path.open("r", encoding="utf-8") as file:
            tickets = json.load(file)

    except (json.JSONDecodeError, UnicodeDecodeError) as error:
        raise ValueError(
            f"Ticket data file contains invalid JSON: {file_path}"
        ) from error

    return validate_tickets(tickets)


def get_next_ticket_id(tickets):
    """Return the next numeric ticket ID."""

    numbers = []

    for ticket in tickets:
        ticket_id = ticket.get("id", "")

        if isinstance(ticket_id, str) and ticket_id.startswith("T"):
            suffix = ticket_id[1:]

            if suffix.isdigit():
                numbers.append(int(suffix))

    return max(numbers, default=0) + 1