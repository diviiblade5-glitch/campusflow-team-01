try:
    affected_users = int(input("How many users are affected? "))

    if affected_users <= 0:
        print("Error: affected users must be greater than zero.")
    else:
        print("Valid number:", affected_users)





        

except ValueError:
    print("Error: please enter a whole number.")

    from campusflow.tickets import validate_ticket_data

# Test valid information.
validate_ticket_data("Wi-Fi not working", "NETWORK", "HIGH", 15)
print("Test 1 passed: valid ticket information.")

# Test an empty title.
try:
    validate_ticket_data("", "Network", "high", 5)
except ValueError as error:
    print("Test 2 passed:", error)

# Test zero affected users.
try:
    validate_ticket_data("Broken keyboard", "Hardware", "medium", 0)
except ValueError as error:
    print("Test 3 passed:", error)

# Test invalid urgency.
try:
    validate_ticket_data("Broken keyboard", "Hardware", "urgent", 5)
except ValueError as error:
    print("Test 4 passed:", error)