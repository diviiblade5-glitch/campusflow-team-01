"""Ticket assignment, status workflow, priority queue, and reports."""


VALID_STATUSES = {"open", "in_progress", "resolved"}


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
    """Summarize tickets by status and priority."""

    report = {
        "total": len(tickets),
        "by_status": {
            status: 0 for status in VALID_STATUSES
        },
        "by_priority": {
            priority: 0
            for priority in ("critical", "high", "medium", "low")
        },
    }

    for ticket in tickets:
        report["by_status"][ticket["status"]] += 1
        report["by_priority"][ticket["priority"]] += 1

    return report
