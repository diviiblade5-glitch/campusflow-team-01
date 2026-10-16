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