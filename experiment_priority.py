def calculate_priority(urgency, affected_users):
    if urgency == "high" and affected_users >= 10:
        return "critical"

    elif urgency == "high" or affected_users >= 10:
        return "high"

    elif urgency == "medium" or affected_users >= 3:
        return "medium"

    else:
        return "low"


print(calculate_priority("high", 15))
print(calculate_priority("high", 2))
print(calculate_priority("medium", 12))
print(calculate_priority("low", 4))
print(calculate_priority("low", 2))