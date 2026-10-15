"""Ticket searching and filtering for CampusFlow."""

PRIORITY_ORDER = {
    "critical": 0,
    "high": 1,
    "medium": 2,
    "low": 3,
}


def search_tickets(tickets,title="",category=None,status=None,priority=None,):

    """Search tickets using a title and optional combined filters."""

    if not isinstance(title, str):
        raise ValueError("Search title must be text.")

    title_query = title.strip().casefold()
    results = []

    for ticket in tickets:
        if title_query and title_query not in ticket["title"].casefold():
            continue

        if category and ticket["category"].casefold() != category.strip().casefold():
            continue

        if status and ticket["status"].casefold() != status.strip().casefold():
            continue

        if priority and ticket["priority"].casefold() != priority.strip().casefold():
            continue

        results.append(ticket)

    return sorted(
        results,
        key=lambda ticket: (
            PRIORITY_ORDER.get(ticket["priority"], 99),
            ticket["id"],
        ),
    )


def format_search_result(ticket):
    """Return the required fields for displaying one search result."""

    return {
        "id": ticket["id"],
        "title": ticket["title"],
        "category": ticket["category"],
        "priority": ticket["priority"],
        "status": ticket["status"],
        "assigned_to": ticket.get("assigned_to"),
    }
