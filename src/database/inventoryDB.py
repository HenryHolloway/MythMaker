#we are going to user src/database/inventory.csv as our database


def fetchInventory():
    try:
        with open('src/database/inventory.csv', 'r') as file:
            inventory = file.readlines()
        return [item.strip().split(',') for item in inventory]
    except FileNotFoundError:
        print("File not found. Creating a new inventory file.")
        with open('src/database/inventory.csv', 'w') as file:
            file.write('')
        return []


def writeInventory(inventory):
    print("Opening inventory.csv for writing.")
    with open('src/database/inventory.csv', 'w') as file:
        print("Writing inventory items to the file.")
        inventoryLine = ','.join(inventory)
        print(f"Writing inventory line: {inventoryLine}")
        file.write(inventoryLine)
        print("Finished writing inventory to file.")


def resetInventoryDB():
    with open('src/database/inventory.csv', 'w') as file:
        file.write('')
