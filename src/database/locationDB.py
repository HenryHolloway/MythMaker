#we are going to user src/database/location.json as our database

def existingLocation(location):
    with open('src/database/location.json', 'r') as file:
        data = json.load(file)
        if location in data:
            return True
        else:
            return False


# takes location json object, appends it to location.json if it isn't in the databse
def addLocation(location):
    if existingLocation(location):
        return
    with open('src/database/location.json', 'r') as file:
        data = json.load(file)
        data.append(location)
    with open('src/database/location.json', 'w') as file:
        file.write(data)




def resetLocationDB():
    with open('src/database/location.json', 'w') as file:
        file.write('{}')  # Resetting the file to an empty JSON object

