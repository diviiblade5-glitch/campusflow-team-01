"""Tests for CampusFlow JSON storage and validation."""

import json
import tempfile
import unittest
from pathlib import Path

from campusflow.tickets import create_ticket
from campusflow.storage import (
    validate_saved_ticket,
    validate_tickets,
    save_tickets,
    load_tickets,
    get_next_ticket_id,
)


def make_ticket(next_id=1):
    """Create a valid ticket for storage tests."""
    return create_ticket(
        "Wi-Fi is not working",
        "Network",
        "high",
        12,
        next_id=next_id,
    )


class TestSavedTicketValidation(unittest.TestCase):

    def test_valid_ticket_is_accepted(self):
        ticket = make_ticket()
        self.assertTrue(validate_saved_ticket(ticket))

    def test_missing_field_is_rejected(self):
        ticket = make_ticket()
        del ticket["title"]

        with self.assertRaises(ValueError):
            validate_saved_ticket(ticket)

    def test_invalid_ticket_id_is_rejected(self):
        ticket = make_ticket()
        ticket["id"] = "INVALID"

        with self.assertRaises(ValueError):
            validate_saved_ticket(ticket)

    def test_invalid_status_is_rejected(self):
        ticket = make_ticket()
        ticket["status"] = "waiting"

        with self.assertRaises(ValueError):
            validate_saved_ticket(ticket)

    def test_incorrect_priority_is_rejected(self):
        ticket = make_ticket()
        ticket["priority"] = "low"

        with self.assertRaises(ValueError):
            validate_saved_ticket(ticket)

    def test_in_progress_ticket_without_assignee_is_rejected(self):
        ticket = make_ticket()
        ticket["status"] = "in_progress"

        with self.assertRaises(ValueError):
            validate_saved_ticket(ticket)

    def test_duplicate_note_ids_are_rejected(self):
        ticket = make_ticket()

        ticket["notes"] = [
            {
                "note_id": "N001",
                "author": "Alex",
                "message": "Router restarted",
            },
            {
                "note_id": "N001",
                "author": "Grace",
                "message": "Connection tested",
            },
        ]

        with self.assertRaises(ValueError):
            validate_saved_ticket(ticket)

    def test_invalid_note_message_is_rejected(self):
        ticket = make_ticket()
        ticket["notes"] = [
            {
                "note_id": "N001",
                "author": "Alex",
                "message": "Help",
            },
        ]

        with self.assertRaises(ValueError):
            validate_saved_ticket(ticket)


    def test_non_text_priority_is_rejected(self):
        ticket = make_ticket()
        ticket["priority"] = []

        with self.assertRaises(ValueError):
            validate_saved_ticket(ticket)



    def test_non_text_status_is_rejected(self):
        ticket = make_ticket()
        ticket["status"] = []

        with self.assertRaises(ValueError):
            validate_saved_ticket(ticket)



class TestTicketCollectionValidation(unittest.TestCase):

    def test_duplicate_ticket_ids_are_rejected(self):
        first = make_ticket(1)
        second = make_ticket(1)

        with self.assertRaises(ValueError):
            validate_tickets([first, second])

    def test_non_list_collection_is_rejected(self):
        with self.assertRaises(ValueError):
            validate_tickets({"id": "T001"})

    def test_invalid_ticket_in_collection_is_rejected(self):
        first = make_ticket(1)
        second = make_ticket(2)
        second["status"] = "waiting"

        with self.assertRaises(ValueError):
            validate_tickets([first, second])


class TestStoragePersistence(unittest.TestCase):

    def test_saved_ticket_can_be_loaded(self):
        ticket = make_ticket()

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"

            save_tickets([ticket], path)
            loaded = load_tickets(path)

        self.assertEqual(loaded, [ticket])

    def test_notes_survive_saving_and_loading(self):
        ticket = make_ticket()
        ticket["notes"].append({
            "note_id": "N001",
            "author": "Alex",
            "message": "Router restarted",
        })

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"

            save_tickets([ticket], path)
            loaded = load_tickets(path)

        self.assertEqual(loaded[0]["notes"], ticket["notes"])

    def test_malformed_json_is_rejected(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            path.write_text("{broken json", encoding="utf-8")

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_duplicate_ids_are_rejected_when_loading(self):
        first = make_ticket(1)
        second = make_ticket(1)

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"
            path.write_text(
                json.dumps([first, second]),
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                load_tickets(path)

    def test_next_ticket_id_continues_after_loading(self):
        ticket = make_ticket(7)

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"

            save_tickets([ticket], path)
            loaded = load_tickets(path)

        self.assertEqual(get_next_ticket_id(loaded), 8)



    def test_failed_load_does_not_change_existing_tickets(self):
        existing_tickets = [make_ticket(1)]
        original_tickets = existing_tickets.copy()

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"

            path.write_text(
                '{"id": "T002", "status": "invalid"}',
                encoding="utf-8",
            )

            with self.assertRaises(ValueError):
                loaded = load_tickets(path)
                existing_tickets[:] = loaded

        self.assertEqual(existing_tickets, original_tickets)


    def test_invalid_tickets_do_not_overwrite_existing_file(self):
        valid_ticket = make_ticket(1)

        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "tickets.json"

            save_tickets([valid_ticket], path)
            original_content = path.read_text(encoding="utf-8")

            invalid_ticket = make_ticket(2)
            invalid_ticket["priority"] = "low"

            with self.assertRaises(ValueError):
                save_tickets([invalid_ticket], path)

            current_content = path.read_text(encoding="utf-8")

            self.assertEqual(current_content, original_content)


if __name__ == "__main__":
    unittest.main()