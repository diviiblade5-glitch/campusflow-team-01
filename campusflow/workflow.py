"""Ticket assignment, status workflow, priority queue, and reports."""


VALID_STATUSES = {"open", "in_progress", "resolved"}


def assign_ticket(ticket, staff_member):
    """Assign a ticket to a staff member."""

    if not isinstance(staff_member, str) or not staff_member.strip():
        raise ValueError("Staff member name cannot be empty.")

    ticket["assigned_to"] = staff_member.strip()
    return ticket


def update_status(ticket, new_status):
    """Update a ticket's status."""

    if new_status not in VALID_STATUSES:
        raise ValueError("Invalid ticket status.")

    current_status = ticket["status"]

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
    """Generate ticket statistics for CampusFlow."""

    statuses = ("open", "in_progress", "resolved")
    priorities = ("critical", "high", "medium", "low")
    categories = ("Network", "Hardware", "Software", "Other")

    report = {
        "total": len(tickets),
        "by_status": {status: 0 for status in statuses},
        "by_priority": {priority: 0 for priority in priorities},
        "by_category": {category: 0 for category in categories},
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
            report["resolved"] += 1
        else:
            report["unresolved"] += 1

    if report["total"] > 0:
        report["resolution_percentage"] = round(
            report["resolved"] / report["total"] * 100,
            2,
        )

    return report
