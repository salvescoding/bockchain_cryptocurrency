# Write a short Python script which queries the user for input (infinite loop with exit possibility) and writes the input to a file.
#  Add another option to your user interface: The user should be able to output the data stored in the file in the terminal.
# Store user input in a list (instead of directly adding it to the file) and write that list to the file – both with pickle and json.
# Adjust the logic to load the file content to work with pickled/ json data.
import json
import pickle
file_text = []


def load_data():
    global file_text
    with open('file.b', mode='rb') as f:
        # file_content = f.readlines()
        # Loads in JSON format
        # file_text = json.loads(file_content[0])
        # Loads in binary format
        file_content = pickle.loads(f.read())
        file_text = file_content['data']


# load_data()


def save_data(user_input):
    with open('file.b', mode='wb') as f:
        print(file_text)
        # Save in JSON format
        # f.write(json.dumps(file_text))
        # Store it in binary format
        binary_data = {
            'data': file_text
        }
        f.write(pickle.dumps(binary_data))


def print_data():
    for line in file_text:
        print(line)
        print(30 * '-')


def check_input(user_input):
    return user_input in ['1', '2', 'Q']


running = True

while running:
    print('Press 1 to print the file content')
    print('Press 2 to save the content to the file')
    print('Press Q to quit')
    user_input = input('Please add some content to the file: \n >  ')
    if not check_input(user_input):
        file_text.append(user_input)
    print(f'This is your list content at the moment: {file_text} ')
    if user_input == 'Q':
        running = False
    elif user_input == '1':
        print_data()
    elif user_input == '2':
        save_data(file_text)
else:
    print('Thank you!')
