"""
Loops Assignment
Given: my_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]

- Create a while loop that prints all elements of the my_list variable 3 times.

- When printing the elements, use a for loop to print the elements

- However, if the element of the for loop is equal to Monday, continue without printing
"""
my_list = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
# for i in range(3):
#     for element in my_list:
#         if element == "Monday":
#             continue 
#         print(element)
i = 0
while i < 3:
    for element in my_list:
        if element == "Monday":
            print("--------------------------------")
            continue
        print(element)
    i += 1