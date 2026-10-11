import unittest

from campusflow.workflow import (
    assign_ticket,
    update_status,
    get_priority_queue,
    generate_report,
)


def sample_ticket(ticket_id, priority="medium"):
    return {
        "id": ticket_id,
        "title": f"Test ticket {ticket_id}",
        "priority": priority,
        "status": "open",
        "assigned_to": None,
    }


class TestTicketAssignment(unittest.TestCase):

    def test_assign_staff_member(self):
        ticket = sample_ticket("T001")

        assign_ticket(ticket, "Alex")

        self.assertEqual(ticket["assigned_to"], "Alex")

    def test_empty_staff_name_rejected(self):
        ticket = sample_ticket("T001")

        with self.assertRaises(ValueError):
            assign_ticket(ticket, " ")


class TestStatusWorkflow(unittest.TestCase):

    def test_open_ticket_can_start_work(self):
        ticket = sample_ticket("T001")

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


if __name__ == "__main__":
    unittest.main()