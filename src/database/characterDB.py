from src.ai.imageGeneration import generateCharacterImage

def writeCharacterCard(character_json):
    import json
    # Assuming a file path for the database
    db_path = "characterDB.json"
    with open(db_path, 'a') as db_file:
        db_file.write(character_json + '\n')

def fetchCharacterCard(character_name):
    import json
    # Assuming a file path for the database
    db_path = "characterDB.json"
    with open(db_path, 'r') as db_file:
        for line in db_file:
            character = json.loads(line)
            if character['name'] == character_name:
                return json.dumps(character, indent=4)
    return None

def resetCharacterDB():
    # Assuming a file path for the database
    db_path = "characterDB.json"
    open(db_path, 'w').close()

def createCharacter(name, level, physical_description):
    import json
    import random

    # Generate attributes
    attributes = {
        "Strength": random.randint(1, 20),
        "Dexterity": random.randint(1, 20),
        "Constitution": random.randint(1, 20),
        "Intelligence": random.randint(1, 20),
        "Wisdom": random.randint(1, 20),
        "Charisma": random.randint(1, 20)
    }

    # Convert attributes to modifiers
    for attribute, value in attributes.items():
        # D&D 5e rules: Modifier = (Attribute - 10) // 2
        attributes[attribute] = (value - 10) // 2

    # Generate character image path
    image_path = generateCharacterImage(physical_description)

    # Compile character information into a dictionary
    character = {
        "name": name,
        "level": level,
        "physical_description": physical_description,
        "attributes": attributes,
        "image_path": image_path
    }

    # Convert dictionary to JSON
    character_json = json.dumps(character, indent=4)

    # Store or return the character JSON
    return character_json