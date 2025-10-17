"""
String Assignment
String Assignment. (This can be tricky so feel free to watch solution so we can do it together)

- Ask the user how many days until their birthday

- Using the print()function. Print an approx. number of weeks until their birthday

- 1 week is = to 7 days.
"""
days = int(input("How many days until your birthday? "))
weeks = round(days / 7, 2)
print(f"You have {weeks} weeks until your birthday.")