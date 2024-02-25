#this will handle prompting the LLM for story, inventory checks, image generation etc.

#TO DO logging. verbose with print

def checkLocationChange(user_input):
    prompt = "The following is a user prompt for an adventure game:\n" + user_input + "\n\nDoes the user change location? Answer only with yes or no."

    #TO DO loop in textGeneration when done
    response = 'no'

    if 'yes' in response:
        return true
    if 'no' in response:
        return false


def checkInventoryChange(user_input):
    prompt = "The following is a user prompt for an adventure game:\n" + user_input + "\n\nDoes the user aquire any items or disperse any items? This includes money. Answer only with yes or no."

    #TO DO loop in textGeneration when done
    response = 'no'

    if 'yes' in response:
        return true
    if 'no' in response:
        return false


def changeInventory(user_input):
    if checkInventoryChange(user_input):
        inventory = ['Item 1', 'Item 2']

        #convert inventory to string

        invString = inventory.toString()

        prompt = "You are in charge of inventory management for an adventure game! The user currently has the following inventory items: " + invString + "\n\nPlease provide the updated contents of the user inventory after their turn. User's turn:" + user_input

        response = newInvString

#check if currently talking to a character exists in character db
def checkCharacterInteraction(): # takes like last n messages as input or something
    pass #returns list of characters the character is currently interacting with or NULL if they aren't interacting with any

# we need to check if the character exists in the db and im not sure where that should happen exactly

# creates a character and generates image, stores character in db
def createCharacter():
    pass



def processTurn():
    pass