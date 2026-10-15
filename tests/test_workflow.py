import unittest

from campusflow.workflow import (
    assign_ticket,
    update_status,
    get_priority_queue,
    generate_report,
    validate_note,
    add_note_to_ticket,
    add_note,
)


import tempfile
from pathlib import Path
from unittest.mock import patch

from campusflow.tickets import create_ticket
from campusflow.storage import save_tickets, load_tickets
from campusflow.workflow import add_note





def sample_ticket(ticket_id, priority="medium"):
    return {
        "id": ticket_id,
        "title": f"Test ticket {ticket_id}",
        "category": "Network",
        "urgency": "medium",
        "affected_users": 2,
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }


class TestTicketAssignment(unittest.TestCase):

    def test_open_ticket_can_start_work(self):
        ticket = sample_ticket("T001")
        assign_ticket(ticket, "Alex")
        update_status(ticket, "in_progress")
        self.assertEqual(ticket["status"], "in_progress")

    def test_empty_staff_name_rejected(self):
        ticket = sample_ticket("T001")

        with self.assertRaises(ValueError):
            assign_ticket(ticket, " ")

    def test_resolved_ticket_cannot_be_reassigned(self):
        ticket = sample_ticket("T001")
        ticket["status"] = "resolved"
        ticket["assigned_to"] = "Alex"

        original_ticket = ticket.copy()

        with self.assertRaises(ValueError):
            assign_ticket(ticket, "Jordan")

        self.assertEqual(ticket, original_ticket)



class TestStatusWorkflow(unittest.TestCase):
    def test_open_ticket_can_start_work(self):
        ticket = sample_ticket("T001")
        assign_ticket(ticket, "Alex")
        update_status(ticket, "in_progress")
        self.assertEqual(ticket["status"], "in_progress")


    def test_ticket_can_be_resolved(self):
        ticket = sample_ticket("T001")
        ticket["status"] = "in_progress"

        update_status(ticket, "resolved")

        self.assertEqual(ticket["status"], "resolved")

    def test_resolved_ticket_can_be_reopened(self):
        ticket = sample_ticket("T001")
        ticket["status"] = "resolved"

        update_status(ticket, "open")

        self.assertEqual(ticket["status"], "open")

    def test_invalid_transition_rejected(self):
        ticket = sample_ticket("T001")

        with self.assertRaises(ValueError):
            update_status(ticket, "resolved")

    def test_unassigned_ticket_cannot_start_work(self):
        ticket = sample_ticket("T001")
        original_ticket = ticket.copy()

        with self.assertRaises(ValueError):
            update_status(ticket, "in_progress")

        self.assertEqual(ticket, original_ticket)



class TestPriorityQueue(unittest.TestCase):

    def test_highest_priority_comes_first(self):
        tickets = [
            sample_ticket("T001", "low"),
            sample_ticket("T002", "critical"),
            sample_ticket("T003", "high"),
        ]

        queue = get_priority_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T002", "T003", "T001"],
        )


    def test_same_priority_uses_numeric_ticket_id_order(self):
        tickets = [
            sample_ticket("T010", "high"),
            sample_ticket("T002", "high"),
            sample_ticket("T001", "high"),
        ]

        queue = get_priority_queue(tickets)

        self.assertEqual(
            [ticket["id"] for ticket in queue],
            ["T001", "T002", "T010"],
        )



    def test_resolved_tickets_are_excluded(self):
        ticket = sample_ticket("T001")
        ticket["status"] = "resolved"

        queue = get_priority_queue([ticket])

        self.assertEqual(queue, [])


class TestReports(unittest.TestCase):

    def test_report_counts_status_and_priority(self):
        tickets = [
            sample_ticket("T001", "critical"),
            sample_ticket("T002", "high"),
        ]

        tickets[1]["status"] = "in_progress"

        report = generate_report(tickets)

        self.assertEqual(report["total"], 2)
        self.assertEqual(report["by_status"]["open"], 1)
        self.assertEqual(report["by_status"]["in_progress"], 1)
        self.assertEqual(report["by_priority"]["critical"], 1)
        self.assertEqual(report["by_priority"]["high"], 1)


    def test_report_counts_categories_and_resolution(self):
        tickets = [
            sample_ticket("T001", "critical"),
            sample_ticket("T002", "high"),
            sample_ticket("T003", "medium"),
        ]

        tickets[1]["category"] = "Hardware"
        tickets[1]["status"] = "in_progress"

        tickets[2]["category"] = "Software"
        tickets[2]["status"] = "resolved"

        report = generate_report(tickets)

        self.assertEqual(report["by_category"]["Network"], 1)
        self.assertEqual(report["by_category"]["Hardware"], 1)
        self.assertEqual(report["by_category"]["Software"], 1)
        self.assertEqual(report["by_category"]["Other"], 0)

        self.assertEqual(report["unresolved_count"], 2)
        self.assertEqual(report["resolved_count"], 1)
        self.assertAlmostEqual(
            report["resolution_percentage"], 33.333333, places=4
        )

    def test_empty_report_has_zero_resolution_percentage(self):
        report = generate_report([])

        self.assertEqual(report["total"], 0)
        self.assertEqual(report["unresolved_count"], 0)
        self.assertEqual(report["resolved_count"], 0)
        self.assertEqual(report["resolution_percentage"], 0.0)




class TestNoteValidation(unittest.TestCase):

    def test_valid_note_is_cleaned(self):
        note = validate_note("  Alex  ", "  Router restarted  ")

        self.assertEqual(note["author"], "Alex")
        self.assertEqual(note["message"], "Router restarted")

    def test_empty_author_rejected(self):
        with self.assertRaises(ValueError):
            validate_note("   ", "Router restarted")

    def test_non_text_message_rejected(self):
        with self.assertRaises(ValueError):
            validate_note("Alex", 12345)

    def test_short_message_rejected(self):
        with self.assertRaises(ValueError):
            validate_note("Alex", "Help")

    def test_long_message_rejected(self):
        with self.assertRaises(ValueError):
            validate_note("Alex", "a" * 301)


class TestPublicAddNote(unittest.TestCase):

    def test_add_note_saves_to_json(self):
        ticket = create_ticket(
            "Wi-Fi is not working",
            "Network",
            "high",
            12,
        )

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"

            save_tickets([ticket], path)

            with patch("campusflow.storage.DEFAULT_PATH", path):
                note = add_note(
                    "T001",
                    "Alex",
                    "Router restarted",
                )

            loaded_tickets = load_tickets(path)

        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(note["author"], "Alex")
        self.assertEqual(
            loaded_tickets[0]["notes"],
            [note],
        )



    def test_invalid_note_does_not_change_saved_data(self):
        ticket = create_ticket(
            "Wi-Fi is not working",
            "Network",
            "high",
            12,
        )

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            save_tickets([ticket], path)

            original_content = path.read_text(encoding="utf-8")

            with patch("campusflow.storage.DEFAULT_PATH", path):
                with self.assertRaises(ValueError):
                    add_note("T001", "   ", "Router restarted")

            current_content = path.read_text(encoding="utf-8")

        self.assertEqual(current_content, original_content)





if __name__ == "__main__":
    unittest.main()



class TestAddingNotes(unittest.TestCase):

    def test_first_note_gets_n001(self):
        ticket = sample_ticket("T001")
        ticket["notes"] = []

        note = add_note_to_ticket(
            [ticket], "T001", "Alex", "Router restarted"
        )

        self.assertEqual(note["note_id"], "N001")
        self.assertEqual(ticket["notes"], [note])

    def test_second_note_gets_n002(self):
        ticket = sample_ticket("T001")
        ticket["notes"] = []

        add_note_to_ticket([ticket], "T001", "Alex", "Router restarted")
        note = add_note_to_ticket(
            [ticket], "T001", "Grace", "Connection tested"
        )

        self.assertEqual(note["note_id"], "N002")

    def test_resolved_ticket_rejects_notes(self):
        ticket = sample_ticket("T001")
        ticket["status"] = "resolved"
        ticket["notes"] = []

        with self.assertRaises(ValueError):
            add_note_to_ticket(
                [ticket], "T001", "Alex", "Router restarted"
            )

        self.assertEqual(ticket["notes"], [])

    def test_missing_ticket_rejected(self):
        with self.assertRaises(ValueError):
            add_note_to_ticket(
                [], "T999", "Alex", "Router restarted"
            )


def test_invalid_ticket_id_rejected(self):
    ticket = sample_ticket("T001")
    ticket["notes"] = []

    for invalid_id in (None, 123, "   "):
        with self.subTest(ticket_id=invalid_id):
            with self.assertRaises(ValueError):
                add_note_to_ticket(
                    [ticket],
                    invalid_id,
                    "Alex",
                    "Router restarted",
                )

    self.assertEqual(ticket["notes"], [])


    def test_invalid_note_does_not_consume_id(self):
        ticket = sample_ticket("T001")
        ticket["notes"] = []

        with self.assertRaises(ValueError):
            add_note_to_ticket([ticket], "T001", "Alex", "Help")

        note = add_note_to_ticket(
            [ticket], "T001", "Alex", "Router restarted"
        )

        self.assertEqual(note["note_id"], "N001")