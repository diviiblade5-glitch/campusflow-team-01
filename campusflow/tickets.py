"""Ticket validation, priority calculation, and creation."""

CATEGORIES = {"Network", "Hardware", "Software", "Other"}
URGENCIES = {"low", "medium", "high"}


def validate_ticket(title, category, urgency, affected_users):
    """Validate and normalize ticket information."""

    if not isinstance(title, str) or not title.strip():
        raise ValueError("Ticket title cannot be empty.")

    if not isinstance(category, str):
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    category = category.strip().capitalize()

    if category not in CATEGORIES:
        raise ValueError("Category must be Network, Hardware, Software, or Other.")

    if not isinstance(urgency, str):
        raise ValueError("Urgency must be low, medium, or high.")

    urgency = urgency.strip().lower()

    if urgency not in URGENCIES:
        raise ValueError("Urgency must be low, medium, or high.")

    if isinstance(affected_users, bool) or not isinstance(affected_users, int):
        raise ValueError("Affected users must be a whole number.")

    if affected_users <= 0:
        raise ValueError("Affected users must be greater than zero.")

    return {
        "title": title.strip(),
        "category": category,
        "urgency": urgency,
        "affected_users": affected_users,
    }


def calculate_priority(urgency, affected_users):
    """Calculate priority according to the assignment rules."""

    if urgency == "high" and affected_users >= 10:
        return "critical"
    elif urgency == "high" or affected_users >= 10:
        return "high"
    elif urgency == "medium" or affected_users >= 3:
        return "medium"
    else:
        return "low"


def create_ticket(title, category, urgency, affected_users, next_id=1):
    """Validate ticket information and create a ticket dictionary."""

    details = validate_ticket(title, category, urgency, affected_users)

    return {
        "id": f"T{next_id:03d}",
        **details,
        "priority": calculate_priority(
            details["urgency"],
            details["affected_users"],
        ),
        "status": "open",
        "assigned_to": None,
        "notes": [],
    }