""" 
Assignment
Write a Python program that can do the following:

- You have $50

- You buy an item that is $15, that has a 3% tax

- Using the print()  Print how much money you have left, after purchasing the item.
"""
account = 50
item = 15
tax = 0.03

total = item + (item * tax)

account = account - total

print(f"You have ${account} left.")