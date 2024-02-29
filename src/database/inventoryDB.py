#we are going to user src/database/inventory.csv as our database


def fetchInventory():
    with open('src/database/inventory.csv', 'r') as file:
        inventory = file.readlines()
    return [item.strip().split(',') for item in inventory]


def writeInventory(inventory):
    with open('src/database/inventory.csv', 'w') as file:
        for item in inventory:
            file.write(','.join(item) + '\n')


def resetInventoryDB():
    with open('src/database/inventory.csv', 'w') as file:
        file.write('')
