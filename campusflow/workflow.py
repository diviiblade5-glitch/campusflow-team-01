"""Ticket assignment, status workflow, priority queue, and reports."""


VALID_STATUSES = {"open", "in_progress", "resolved"}


def validate_note(author, message):
    """Validate and normalize note author and message."""

    if not isinstance(author, str) or not author.strip():
        raise ValueError("Note author cannot be empty.")

    if not isinstance(message, str):
        raise ValueError("Note message must be text.")

    message = message.strip()

    if not 5 <= len(message) <= 300:
        raise ValueError(
            "Note message must contain between 5 and 300 characters."
        )

    return {
        "author": author.strip(),
        "message": message,
    }


def add_note_to_ticket(tickets, ticket_id, author, message):
    """Validate and add a note to an existing ticket."""

    if not isinstance(ticket_id, str) or not ticket_id.strip():
        raise ValueError("Ticket ID cannot be empty.")

    wanted_id = ticket_id.strip().upper()

    ticket = next(
        (
            item for item in tickets
            if item.get("id", "").upper() == wanted_id
        ),
        None,
    )

    if ticket is None:
        raise ValueError(f"Ticket {wanted_id} was not found.")

    if ticket["status"] not in {"open", "in_progress"}:
        raise ValueError("Notes can only be added to open or in-progress tickets.")

    details = validate_note(author, message)

    notes = ticket.setdefault("notes", [])
    next_number = max(
        (
            int(note["note_id"][1:])
            for note in notes
            if isinstance(note.get("note_id"), str)
            and note["note_id"].startswith("N")
            and note["note_id"][1:].isdigit()
        ),
        default=0,
    ) + 1

    note = {
        "note_id": f"N{next_number:03d}",
        **details,
    }

    notes.append(note)
    return note


def add_note(ticket_id, author, message):
    """Add a note to a saved ticket and persist the change."""

    from campusflow import storage

    tickets = storage.load_tickets(storage.DEFAULT_PATH)

    note = add_note_to_ticket(
        tickets,
        ticket_id,
        author,
        message,
    )

    storage.save_tickets(tickets, storage.DEFAULT_PATH)

    return note




def assign_ticket(ticket, staff_member):
    """Assign a ticket to a staff member."""

    if ticket["status"] == "resolved":
        raise ValueError("Reopen the ticket before changing its assignment.")

    if not isinstance(staff_member, str) or not staff_member.strip():
        raise ValueError("Staff member name cannot be empty.")

    ticket["assigned_to"] = staff_member.strip()
    return ticket


def update_status(ticket, new_status):
    """Update a ticket's status."""

    if not isinstance(new_status, str) or new_status not in VALID_STATUSES:
        raise ValueError("Invalid ticket status.")

    current_status = ticket["status"]

    if new_status == "in_progress" and not ticket.get("assigned_to"):
        raise ValueError("Assign the ticket before starting work.")

    allowed_transitions = {
        "open": {"in_progress"},
        "in_progress": {"open", "resolved"},
        "resolved": {"open"},
     }

    if new_status not in allowed_transitions[current_status]:
        raise ValueError(
            f"Cannot change status from {current_status} to {new_status}."
        )

    ticket["status"] = new_status
    return ticket


def get_priority_queue(tickets):
    """Return unresolved tickets from highest to lowest priority."""

    priority_order = {
        "critical": 0,
        "high": 1,
        "medium": 2,
        "low": 3,
    }

    unresolved = [
        ticket for ticket in tickets
        if ticket["status"] != "resolved"
    ]

    return sorted(
        unresolved,
        key=lambda ticket: (
            priority_order[ticket["priority"]],
            ticket["id"],
        ),
    )

def generate_report(tickets):
    """Summarize tickets by status, priority, and category."""

    categories = ("Network", "Hardware", "Software", "Other")
    priorities = ("critical", "high", "medium", "low")

    report = {
        "total": len(tickets),
        "by_status": {status: 0 for status in VALID_STATUSES},
        "by_priority": {priority: 0 for priority in priorities},
        "by_category": {category: 0 for category in categories},
        "unresolved_count": 0,
        "resolved_count": 0,
        "unresolved": 0,
        "resolved": 0,
        "resolution_percentage": 0.0,
    }

    for ticket in tickets:
        status = ticket["status"]
        priority = ticket["priority"]
        category = ticket["category"]

        report["by_status"][status] += 1
        report["by_priority"][priority] += 1
        report["by_category"][category] += 1

        if status == "resolved":
            report["resolved_count"] += 1
            report["resolved"] += 1
        else:
            report["unresolved_count"] += 1
            report["unresolved"] += 1

    if report["total"] > 0:
        report["resolution_percentage"] = (
            report["resolved_count"] / report["total"]
        ) * 100

    return report
