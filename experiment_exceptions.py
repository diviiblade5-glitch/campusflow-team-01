try:
    number = int("25")
    print("Number:", number)
except ValueError:
    print("That is not a valid integer.")

try:
    number = int("hello")
    print("Number:", number)
except ValueError:
    print("That is not a valid integer.")