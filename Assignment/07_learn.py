"""
Functions Assignment
- Create a function that takes in 3 parameters(firstname, lastname, age) and

returns a dictionary based on those values
"""
def create_person(firstname, lastname, age):
    return {
        "firstname": firstname,
        "lastname": lastname,
        "age": age
    }

person = create_person("John", "Doe", 30)
print(person)