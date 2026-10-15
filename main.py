"""CampusFlow application entry point. Run with: python3 main.py"""

from campusflow.tickets import create_ticket
from campusflow.workflow import (
    assign_ticket, update_status, get_priority_queue, generate_report,
)
from campusflow.search import search_tickets
from campusflow.quiz import run_quiz
from campusflow.storage import load_tickets, save_tickets, get_next_ticket_id

DATA_FILE = "data/tickets.json"


def find_ticket(tickets, ticket_id):
    """Find a ticket by ID without case sensitivity."""
    wanted_id = ticket_id.strip().upper()
    return next(
        (ticket for ticket in tickets
         if ticket.get("id", "").upper() == wanted_id),
        None,
    )


def print_ticket(ticket):
    """Display the details of one ticket."""
    print(f"\nTicket ID: {ticket.get('id', 'N/A')}")
    print(f"Title: {ticket.get('title', 'N/A')}")
    print(f"Category: {ticket.get('category', 'N/A')}")
    print(f"Urgency: {ticket.get('urgency', 'N/A')}")
    print(f"Affected users: {ticket.get('affected_users', 'N/A')}")
    print(f"Priority: {ticket.get('priority', 'N/A')}")
    print(f"Status: {ticket.get('status', 'open')}")
    print(f"Assigned to: {ticket.get('assigned_to') or 'Unassigned'}")


def display_tickets(tickets):
    """Display all tickets."""
    if not tickets:
        print("No tickets found.")
        return
    for ticket in tickets:
        print_ticket(ticket)


def save_current_tickets(tickets):
    """Save tickets to the JSON data file."""
    try:
        save_tickets(tickets, DATA_FILE)
    except (OSError, TypeError, ValueError) as error:
        print(f"Could not save tickets: {error}")


def create_new_ticket(tickets):
    """Prompt for ticket details and create a validated ticket."""
    print("\n--- Create a Ticket ---")
    title = input("Enter ticket title: ").strip()
    category = input(
        "Enter category (Network, Hardware, Software, Other): "
    ).strip()
    urgency = input("Enter urgency (low, medium, high): ").strip().lower()

    try:
        affected_users = int(input("Enter number of users affected: ").strip())
        ticket = create_ticket(
            title, category, urgency, affected_users,
            next_id=get_next_ticket_id(tickets),
        )
    except (ValueError, TypeError) as error:
        print(f"Ticket was not created: {error}")
        return

    tickets.append(ticket)
    save_current_tickets(tickets)
    print("\nTicket created successfully!")
    print_ticket(ticket)


def assign_existing_ticket(tickets):
    """Assign a found ticket to a staff member."""
    print("\n--- Assign a Ticket ---")
    if not tickets:
        print("No tickets are available to assign.")
        return

    ticket_id = input("Enter ticket ID (for example, T001): ")
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
        print(f"Ticket {ticket_id.strip().upper()} was not found.")
        return

    staff_member = input("Enter staff member's name: ")
    try:
        assign_ticket(ticket, staff_member)
        save_current_tickets(tickets)
        print("Ticket assigned successfully.")
        print_ticket(ticket)
    except ValueError as error:
        print(f"Could not assign ticket: {error}")


def change_ticket_status(tickets):
    """Update a found ticket using the workflow's allowed transitions."""
    print("\n--- Update Ticket Status ---")
    if not tickets:
        print("No tickets are available to update.")
        return

    ticket_id = input("Enter ticket ID (for example, T001): ")
    ticket = find_ticket(tickets, ticket_id)
    if ticket is None:
        print(f"Ticket {ticket_id.strip().upper()} was not found.")
        return

    new_status = input(
        "Enter new status (open, in_progress, resolved): "
    ).strip().lower()
    if new_status == "in progress":
        new_status = "in_progress"

    try:
        update_status(ticket, new_status)
        save_current_tickets(tickets)
        print("Ticket status updated successfully.")
        print_ticket(ticket)
    except (ValueError, KeyError) as error:
        print(f"Could not update ticket status: {error}")


def show_priority_queue(tickets):
    """Display unresolved tickets from highest to lowest priority."""
    print("\n--- Priority Queue (Unresolved Tickets) ---")
    display_tickets(get_priority_queue(tickets))
def search_existing_tickets(tickets):
    """Search tickets by title and optional filters."""
    print("\n--- Search Tickets ---")

    title = input("Enter title keyword (or press Enter for all): ").strip()
    category = input(
        "Category filter (Network, Hardware, Software, Other; Enter to skip): "
    ).strip()
    status = input(
        "Status filter (open, in_progress, resolved; Enter to skip): "
    ).strip()
    priority = input(
        "Priority filter (critical, high, medium, low; Enter to skip): "
    ).strip()

    try:
        results = search_tickets(
            tickets,
            title=title,
            category=category or None,
            status=status or None,
            priority=priority or None,
        )
    except (ValueError, KeyError) as error:
        print(f"Search failed: {error}")
        return

    if not results:
        print("No matching tickets found.")
        return

    print(f"\nFound {len(results)} matching ticket(s):")
    for ticket in results:
        print(
            f"{ticket['id']} | {ticket['title']} | "
            f"{ticket['category']} | {ticket['priority']} | "
            f"{ticket['status']} | "
            f"Assigned to: {ticket.get('assigned_to') or 'Unassigned'}"
        )

def show_report(tickets):
    """Display ticket statistics."""
    report = generate_report(tickets)

    print("\n--- Ticket Report ---")
    print(f"Total tickets: {report['total']}")

    print("\nTickets by status:")
    for status, count in report["by_status"].items():
        print(f"  {status.replace('_', ' ').title()}: {count}")

    print("\nTickets by priority:")
    for priority, count in report["by_priority"].items():
        print(f"  {priority.title()}: {count}")

    print("\nTickets by category:")
    for category, count in report["by_category"].items():
        print(f"  {category}: {count}")

    print(f"\nUnresolved tickets: {report['unresolved']}")
    print(f"Resolved tickets: {report['resolved']}")
    print(f"Resolution percentage: {report['resolution_percentage']:.2f}%")

def show_menu():
    """Print the main menu."""
    print("\n========== CAMPUSFLOW ==========")
    print("1. Create a ticket")
    print("2. View all tickets")
    print("3. Assign a ticket")
    print("4. Update ticket status")
    print("5. View priority queue")
    print("6. Generate ticket report")
    print("7. Search tickets")
    print("8. Engineering Understanding Check")
    print("9. Save tickets")
    print("10. Exit")
    print("================================")

def main():
    """Load saved tickets and run the menu."""
    try:
        tickets = load_tickets(DATA_FILE)
    except (OSError, ValueError) as error:
        print(f"Could not load saved tickets: {error}")
        print("Starting with an empty ticket list.")
        tickets = []

    print("Welcome to CampusFlow!")
    print(f"Loaded {len(tickets)} ticket(s).")

    while True:
        show_menu()
        choice = input("Choose an option (1-10): ").strip()

        if choice == "1":
            create_new_ticket(tickets)
        elif choice == "2":
            print("\n--- All Tickets ---")
            display_tickets(tickets)
        elif choice == "3":
            assign_existing_ticket(tickets)
        elif choice == "4":
            change_ticket_status(tickets)
        elif choice == "5":
            show_priority_queue(tickets)
        elif choice == "6":
            show_report(tickets)
        elif choice == "7":
            search_existing_tickets(tickets)
        elif choice == "8":
            run_quiz()
        elif choice == "9":
            save_current_tickets(tickets)
            print("Save requested.")
        elif choice == "10":
            save_current_tickets(tickets)
            print("Tickets saved. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 10.")


if __name__ == "__main__":
    main()
