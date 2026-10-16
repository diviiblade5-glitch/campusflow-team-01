"""Ticket assignment, workflow, reporting, and follow-up notes."""

from campusflow import storage


VALID_STATUSES = {"open", "in_progress", "resolved"}

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}

VALID_CATEGORIES = {"Network", "Hardware", "Software", "Other"}


def assign_ticket(ticket, staff_member):
    """Assign an open or in-progress ticket to a staff member."""
    if not isinstance(staff_member, str) or not staff_member.strip():
        raise ValueError("Staff member name cannot be empty.")

    if ticket.get("status") == "resolved":
        raise ValueError("A resolved ticket cannot be reassigned.")

    ticket["assigned_to"] = staff_member.strip()
    return ticket


def update_status(ticket, new_status):
    """Update a ticket's status using the allowed workflow transitions."""
    if not isinstance(new_status, str):
        raise ValueError("Ticket status must be text.")

    new_status = new_status.strip().lower()

    if new_status not in VALID_STATUSES:
        raise ValueError(f"Invalid ticket status: {new_status}")

    current_status = ticket.get("status")

    if current_status not in VALID_STATUSES:
        raise ValueError(f"Invalid current ticket status: {current_status}")

    if current_status == new_status:
        return ticket

    if current_status == "open" and new_status == "in_progress":
        if not ticket.get("assigned_to"):
            raise ValueError(
                "A ticket must be assigned before work can begin."
            )

    elif current_status == "in_progress" and new_status == "resolved":
        pass

    elif current_status == "resolved" and new_status == "open":
        pass

    else:
        raise ValueError(
            f"Invalid status transition: {current_status} -> {new_status}"
        )

    ticket["status"] = new_status
    return ticket


def get_priority_queue(tickets):
    """Return unresolved tickets ordered by priority and numeric ticket ID."""
    unresolved_tickets = [
        ticket
        for ticket in tickets
        if ticket.get("status") != "resolved"
    ]

    def sort_key(ticket):
        priority = PRIORITY_ORDER.get(
            ticket.get("priority", "").lower(),
            len(PRIORITY_ORDER),
        )

        ticket_id = ticket.get("id", "")
        numeric_id = "".join(
            character for character in ticket_id if character.isdigit()
        )

        return (
            priority,
            int(numeric_id) if numeric_id else float("inf"),
        )

    return sorted(unresolved_tickets, key=sort_key)


def generate_report(tickets):
    """Generate ticket totals grouped by status, priority, and category."""
    report = {
        "total": len(tickets),
        "by_status": {
            "open": 0,
            "in_progress": 0,
            "resolved": 0,
        },
        "by_priority": {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
        },
        "by_category": {
            category: 0 for category in VALID_CATEGORIES
        },
        "unresolved_count": 0,
        "resolved_count": 0,
        "resolution_percentage": 0.0,
    }

    for ticket in tickets:
        status = ticket.get("status", "open")
        priority = ticket.get("priority", "").lower()
        category = ticket.get("category", "")

        if status in report["by_status"]:
            report["by_status"][status] += 1

        if priority in report["by_priority"]:
            report["by_priority"][priority] += 1

        if category in report["by_category"]:
            report["by_category"][category] += 1

        if status == "resolved":
            report["resolved_count"] += 1
        else:
            report["unresolved_count"] += 1

    if report["total"] > 0:
        report["resolution_percentage"] = (
            report["resolved_count"] / report["total"]
        ) * 100

    return report


def validate_note(author, message):
    """Validate and clean a follow-up note."""
    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be empty.")

    if not isinstance(message, str):
        raise ValueError("Note message must be text.")

    author = author.strip()
    message = message.strip()

    if not message:
        raise ValueError("Note message cannot be empty.")

    if len(message) < 5:
        raise ValueError("Note message must contain at least 5 characters.")

    if len(message) > 300:
        raise ValueError("Note message cannot exceed 300 characters.")

    return {
        "author": author,
        "message": message,
    }


def add_note_to_ticket(tickets, ticket_id, author, message):
    """Validate and add a note to a ticket in the supplied ticket list."""
    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID cannot be empty.")

    wanted_id = ticket_id.strip().upper()

    ticket = next(
        (
            item
            for item in tickets
            if isinstance(item.get("id"), str)
            and item["id"].upper() == wanted_id
        ),
        None,
    )

    if ticket is None:
        raise ValueError(f"Ticket {wanted_id} was not found.")

    if ticket.get("status") == "resolved":
        raise ValueError("Cannot add notes to a resolved ticket.")

    cleaned_note = validate_note(author, message)

    notes = ticket.setdefault("notes", [])

    if not isinstance(notes, list):
        raise ValueError("Ticket notes must be stored as a list.")

    note_number = len(notes) + 1

    existing_ids = {
        note.get("note_id")
        for note in notes
        if isinstance(note, dict)
    }

    while f"N{note_number:03d}" in existing_ids:
        note_number += 1

    note = {
        "note_id": f"N{note_number:03d}",
        "author": cleaned_note["author"],
        "message": cleaned_note["message"],
    }

    notes.append(note)
    return note


def add_note(ticket_id, author, message):
    """Add a note to a saved ticket and persist the updated ticket list."""
    cleaned_note = validate_note(author, message)

    tickets = storage.load_tickets(storage.DEFAULT_PATH)

    # Add the note only after its author and message have been validated.
    note = add_note_to_ticket(
        tickets,
        ticket_id,
        cleaned_note["author"],
        cleaned_note["message"],
    )

    storage.save_tickets(tickets, storage.DEFAULT_PATH)
    return note