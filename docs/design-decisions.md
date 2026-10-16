# CampusFlow Design Decisions

## 1. Standard Python Data Structures

**Decision:** Represent tickets and notes using dictionaries and lists.

**Reason:** These structures are suitable for the project because
tickets contain several named fields, while a ticket can have
multiple notes.

## 2. Centralized Ticket Validation

**Decision:** Validate ticket input before creating a ticket.

**Reason:** This prevents invalid titles, categories, urgency values,
and affected-user counts from entering the application.

## 3. Calculated Priority

**Decision:** Calculate priority from urgency and affected-user count.

**Reason:** This keeps priority consistent with the project rules
instead of relying on a user to choose it manually.

## 4. JSON Persistence

**Decision:** Store tickets in JSON.

**Reason:** JSON is readable, supported by Python's standard library,
and allows ticket information to survive application restarts.

The current storage format is a JSON list of ticket objects.
Each ticket includes a notes list.

## 5. Validate Before Saving

**Decision:** Validate the complete ticket collection before writing
it to the JSON file.

**Reason:** Invalid ticket data should not overwrite a valid saved
collection.

## 6. Notes Belong to Tickets

**Decision:** Store notes inside their corresponding ticket.

**Reason:** This keeps each note associated with the ticket it
describes and allows notes to be saved and loaded with that ticket.

Each note has an ID, author, and message. Note IDs are generated
separately for each ticket.

## 7. Separate Business Logic from CLI Interaction

**Decision:** Keep ticket operations in the `campusflow` package and
use `main.py` for command-line interaction.

**Reason:** Separating the logic from the interface makes the
functions easier to test and reuse.

## 8. Automated Testing

**Decision:** Use Python's built-in `unittest` framework.

**Reason:** It allows the project to test validation, priority,
workflow, note handling, and persistence without third-party
testing frameworks.

## 9. Validate Saved Data Before Loading

**Decision:** Validate the complete collection of tickets when loading
data from JSON.

**Reason:** Validating only new user input is not enough. Saved files
can contain missing fields, duplicate IDs, invalid priorities, or
malformed notes.

The application rejects invalid saved collections rather than
accepting data that violates the ticket rules. A failed load must
not replace an existing valid collection.

A missing data file is treated as a fresh start. Malformed JSON or
invalid ticket data produces a clear error.

## 10. Ticket Workflow and Assignment Rules

**Decision:** Restrict ticket status changes to the defined workflow.

**Reason:** Tickets should follow a predictable lifecycle. An open
ticket can enter `in_progress` only when it has an assignee. A
resolved ticket must be explicitly reopened before further work.

Resolved tickets cannot be reassigned or receive new notes until
they are reopened.

These rules prevent invalid operations from changing ticket data.

## 11. Follow-Up Note Validation

**Decision:** Validate note authors and messages before adding notes.

**Reason:** Every note needs an identifiable author and a useful
message. Authors cannot be blank, and trimmed messages must contain
between 5 and 300 characters.

Each ticket maintains its own note sequence, starting at `N001`.
Rejected notes must not consume note IDs or modify the ticket.

## 12. Priority Queue Ordering

**Decision:** Sort unresolved tickets by priority and then by the
numeric portion of their ticket IDs.

**Reason:** Critical tickets should appear before high, medium, and
low priority tickets. When priorities are equal, numeric ID ordering
provides predictable results, such as `T002` before `T010`.

Resolved tickets are excluded from the priority queue.

The queue is a view of the tickets and should not change their
stored order or modify ticket information.

## 13. Read-Only Search and Combined Filters

**Decision:** Search tickets using a case-insensitive title substring
and optional category, status, and priority filters.

**Reason:** Case-insensitive matching makes searches easier to use.
Combining filters with AND means a result must satisfy every supplied
condition.

Search returns matching tickets without changing the original
collection. This keeps searching separate from ticket modification.

## 14. Ticket Reporting

**Decision:** Calculate reports from the current ticket collection.

**Reason:** Counts by status, priority, and category help users
understand the current helpdesk workload.

The report also includes unresolved tickets and the resolution
percentage. An empty collection produces a resolution percentage
of zero instead of causing a division-by-zero error.

Reopened tickets are counted according to their current status.

## 15. Engineering Understanding Check

**Decision:** Keep the quiz questions, answer choices, and scoring
separate from the main CLI interaction.

**Reason:** Separating quiz logic makes scoring easier to test and
reduces the amount of quiz-specific logic inside the menu.

Invalid choices are rejected and the user is prompted again.
The final score reflects the answers actually submitted.

## 16. Automated Tests

**Decision:** Use focused unit tests to verify both successful
operations and rejected operations.

**Reason:** Testing only successful cases would not prove that
validation and workflow restrictions work correctly.

The test suite covers valid and invalid input, priority calculation,
ticket lifecycle, notes, search, reporting, and JSON persistence.

Tests also verify that rejected operations do not corrupt existing
data.

## 17. Safe Startup After a Loading Error

**Decision:** Stop normal application startup when saved ticket data
cannot be loaded and validated.

**Reason:** Silently starting with an empty collection after a load
failure could lead to valid saved data being overwritten when the
application exits.

A clear error allows the problem to be corrected before the
application continues.




## CLI Menu Integration Bug: Duplicate Options and Numbering

### Problem

After integrating Engineer A's and Engineer B's work, the
CampusFlow CLI menu displayed duplicate option numbers.

The affected options included:

- Option 7: Add a follow-up note.
- Option 8: View ticket notes.
- Option 7: Search tickets.
- Option 8: Engineering Understanding Check.

The menu also advertised only 10 options even though the application
had 12 distinct actions.

The search-related section of the menu-selection code also contained
repeated statements, including calls to `search_existing_tickets()`
and duplicate "Tickets saved." messages.

### Cause

The integration required changes to the shared `main.py` file,
including the printed menu and the code that handles user selections.

The code review revealed inconsistent option numbering and repeated
search-related statements. This suggests the integration was not
fully reconciled and tested after the new features were added.

A successful Git merge does not guarantee that the combined
application is logically correct.

### Resolution

We corrected the menu so that every action has a unique number
from 1 to 12.

The corrected numbering is:

1. Create a ticket
2. View all tickets
3. Assign a ticket
4. Update ticket status
5. View priority queue
6. Generate ticket report
7. Add a follow-up note
8. View ticket notes
9. Search tickets
10. Engineering Understanding Check
11. Save tickets
12. Exit

We also updated the input prompt to request an option from 1 to 12
and aligned the relevant selection conditions with the new numbering.

### Prevention

To reduce the risk of similar integration bugs:

1. Review changes to shared files such as `main.py` before merging.
2. Update the displayed menu and selection logic together.
3. Check that every menu option has a unique number.
4. Remove duplicated statements introduced during integration.
5. Test every menu option after combining feature branches.
6. Run the automated test suite after integration.
7. Ask the other developer to review shared-file changes before
   approving the final pull request.

### Verification

The corrected menu was manually displayed in the terminal and
showed all 12 options with unique numbering.

The exit option was also tested, and the application displayed
a goodbye message after saving tickets.

Further integration testing should verify that every option
invokes the correct feature and that existing functionality
continues to work.

### Lesson Learned

Integration is not complete merely because Git reports that a
merge succeeded. The team must also inspect the combined code,
test the application's behaviour, and verify that new features
work correctly alongside existing ones.