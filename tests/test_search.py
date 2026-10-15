import unittest

from campusflow.search import search_tickets, format_search_result


def sample_tickets():
    return [
        {
            "id": "T001",
            "title": "Wi-Fi connection problem",
            "category": "Network",
            "priority": "high",
            "status": "open",
            "assigned_to": None,
        },
        {
            "id": "T002",
            "title": "Keyboard broken",
            "category": "Hardware",
            "priority": "critical",
            "status": "in_progress",
            "assigned_to": "Alex",
        },
        {
            "id": "T003",
            "title": "Wi-Fi password reset",
            "category": "Network",
            "priority": "medium",
            "status": "open",
            "assigned_to": None,
        },
    ]


class TestTicketSearch(unittest.TestCase):

    def test_title_search_is_case_insensitive(self):
        results = search_tickets(sample_tickets(), title="WI-FI")
        self.assertEqual(len(results), 2)

    def test_category_filter(self):
        results = search_tickets(sample_tickets(), category="Network")
        self.assertEqual(len(results), 2)

    def test_status_filter(self):
        results = search_tickets(sample_tickets(), status="open")
        self.assertEqual(len(results), 2)

    def test_priority_filter(self):
        results = search_tickets(sample_tickets(), priority="critical")
        self.assertEqual([ticket["id"] for ticket in results], ["T002"])

    def test_filters_combine(self):
        results = search_tickets(
            sample_tickets(),
            title="wi-fi",
            category="Network",
            status="open",
            priority="medium",
        )
        self.assertEqual([ticket["id"] for ticket in results], ["T003"])

    def test_results_sorted_by_priority(self):
        results = search_tickets(sample_tickets())
        self.assertEqual(
            [ticket["id"] for ticket in results],
            ["T002", "T001", "T003"],
        )

    def test_no_matches_returns_empty_list(self):
        results = search_tickets(sample_tickets(), title="printer")
        self.assertEqual(results, [])

    def test_search_does_not_modify_tickets(self):
        tickets = sample_tickets()
        original = [ticket.copy() for ticket in tickets]

        search_tickets(tickets, title="Wi-Fi")

        self.assertEqual(tickets, original)

    def test_display_fields(self):
        result = format_search_result(sample_tickets()[0])

        self.assertEqual(
            set(result),
            {"id", "title", "category", "priority", "status", "assigned_to"},
        )


if __name__ == "__main__":
    unittest.main()
