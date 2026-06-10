import json


def read_file_data(file):

    try:

        with open(file, 'r') as read_file:
            return json.load(read_file)

    except FileNotFoundError:
        print(f"Error: The file '{file}' does not exist.")

    except json.JSONDecodeError as e:
        print(f"Error: Failed decoding JSON in '{file}': {e}")

    return None


def add_file_data(file, identifyer, data):
    try:

        with open(file, 'r') as json_file:
            file_data = json.load(json_file)

        file_data[identifyer] = data

        with open(file, 'w') as json_file:
            json.dump(file_data, json_file, indent=4)

        print("Data added to file "+file+".")

    except FileNotFoundError:
        print(f"Error: The file '{file}' does not exist.")

    except json.JSONDecodeError as e:
        print(f"Error: Failed decoding JSON in '{file}': {e}")

    return None

def is_positive_integer(number):
    return number.isnumeric() and int(number) > 0
