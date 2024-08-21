#we are going to use src/database/inventory.json as our database

import json

def fetchInventory():
    try:
        with open('src/database/inventory.json', 'r') as file:
            inventory = json.load(file)
        return inventory
    except FileNotFoundError:
        print("File not found. Creating a new inventory file.")
        with open('src/database/inventory.json', 'w') as file:
            json.dump({}, file)
        return {}
    except json.JSONDecodeError:
        print("Error decoding JSON. Returning empty inventory.")
        return {}


def writeInventory(inventory):
    print("Opening inventory.json for writing.")
    with open('src/database/inventory.json', 'w') as file:
        print("Writing inventory items to the file.")
        json.dump(inventory, file, indent=4)
        print("Finished writing inventory to file.")


def resetInventoryDB():
    with open('src/database/inventory.json', 'w') as file:
        json.dump({}, file)
