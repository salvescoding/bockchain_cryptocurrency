name = "Sergio"
age = 34


def my_information():
    print(f"My name is {name}, and I am {age} years old")


def full_name(first_name, last_name):
    print(f"Full name: {first_name} {last_name} ")


def calculate_decades(age):
    print(f"You have lived {age[0]} decades")


def user_input():
    return input("> ")


my_information()
print("First name:")
first = user_input()
print("Last name:")
last = user_input()
full_name(first, last)
print("Type your age:")
decades = user_input()
calculate_decades(decades)
