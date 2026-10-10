import unittest

from campusflow.tickets import (
    calculate_priority,
    create_ticket,
    validate_ticket,
)


class TestTicketValidation(unittest.TestCase):

    def test_valid_ticket(self):
        ticket = validate_ticket(
            "Wi-Fi not working",
            "network",
            "HIGH",
            5,
        )

        self.assertEqual(ticket["title"], "Wi-Fi not working")
        self.assertEqual(ticket["category"], "Network")
        self.assertEqual(ticket["urgency"], "high")
        self.assertEqual(ticket["affected_users"], 5)

    def test_empty_title_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("", "Network", "high", 5)

    def test_invalid_category_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("Broken laptop", "Furniture", "low", 1)

    def test_invalid_urgency_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("Broken laptop", "Hardware", "urgent", 1)

    def test_zero_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("Broken laptop", "Hardware", "low", 0)

    def test_negative_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("Broken laptop", "Hardware", "low", -2)

    def test_non_integer_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("Broken laptop", "Hardware", "low", 2.5)

    def test_boolean_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("Broken laptop", "Hardware", "low", True)


    def test_whitespace_only_title_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("   ", "Network", "high", 5)

    def test_numeric_string_users_rejected(self):
        with self.assertRaises(ValueError):
            validate_ticket("Wi-Fi issue", "Network", "high", "5")        


class TestPriorityCalculation(unittest.TestCase):

    def test_critical_priority(self):
        self.assertEqual(calculate_priority("high", 10), "critical")

    def test_high_urgency_with_few_users(self):
        self.assertEqual(calculate_priority("high", 2), "high")

    def test_many_users_with_low_urgency(self):
        self.assertEqual(calculate_priority("low", 10), "high")

    def test_medium_priority(self):
        self.assertEqual(calculate_priority("low", 3), "medium")

    def test_low_priority(self):
        self.assertEqual(calculate_priority("low", 2), "low")


class TestTicketCreation(unittest.TestCase):

    def test_ticket_created_with_expected_defaults(self):
        ticket = create_ticket(
            "Projector broken",
            "hardware",
            "medium",
            4,
        )

        self.assertEqual(ticket["id"], "T001")
        self.assertEqual(ticket["priority"], "medium")
        self.assertEqual(ticket["status"], "open")
        self.assertIsNone(ticket["assigned_to"])


if __name__ == "__main__":
    unittest.main()