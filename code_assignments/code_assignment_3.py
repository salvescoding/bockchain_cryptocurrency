import copy
persons =[
    {
        'name': 'Clinton',
        'age': 35,
        'hobbies': ['Golf', 'Swim', 'Travel']
    },
    {
        'name': 'John',
        'age': 65,
        'hobbies': ['Cars', 'Sleep']
    },
    {
        'name': 'Cortney',
        'age': 25,
        'hobbies': ['Dance', 'Drink']
    }
]
names = [el['name'] for el in persons]
print(all([el for el in persons if el['age'] > 20]))
copy_persons = copy.deepcopy(persons)
copy_persons[0]['name'] = "Sergio"
a, b, c = persons

print(names)
print(copy_persons)
print(persons)
print(a)
print(b)
print(c)
