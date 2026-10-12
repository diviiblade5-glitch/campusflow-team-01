"""JSON storage helpers for CampusFlow tickets."""

import json
from pathlib import Path

DEFAULT_PATH = Path("data/tickets.json")


def save_tickets(tickets, path=DEFAULT_PATH):
    """Save a list of tickets to a JSON file."""
    file_path = Path(path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    with file_path.open("w", encoding="utf-8") as file:
        json.dump(tickets, file, indent=4)


def load_tickets(path=DEFAULT_PATH):
    """Load tickets from JSON, returning an empty list if the file is absent."""
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

    if not isinstance(tickets, list):
        raise ValueError("Ticket data must contain a JSON list.")

    if not all(isinstance(ticket, dict) for ticket in tickets):
        raise ValueError("Each saved ticket must be a JSON object.")

    return tickets


def get_next_ticket_id(tickets):
    """Return the next numeric ticket ID, even after tickets are reloaded."""
    numbers = []

    for ticket in tickets:
        ticket_id = ticket.get("id", "")

        if isinstance(ticket_id, str) and ticket_id.startswith("T"):
            suffix = ticket_id[1:]
            if suffix.isdigit():
                numbers.append(int(suffix))

    return max(numbers, default=0) + 1
