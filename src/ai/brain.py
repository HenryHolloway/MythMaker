from src.database.inventoryDB import fetchInventory, writeInventory
from src.database.characterDB import fetchCharacterCard, writeCharacterCard
from src.database.locationDB import *

from src.ai.textGeneration import *
from src.ai.imageGeneration import generateBackgroundImage, generateCharacterImage

import asyncio

#this will handle prompting the LLM for story, inventory checks, image generation etc.

#TO DO logging. verbose with print

async def generateAdventureStart(message_callback):
    print("Called function generateAdventureStart in module brain")

    #TO DO add inventory specifics to these templates.
    
    examples = ["You stand before the mouth of a gaping cave, hidden by the thick underbrush at the mountain's base. The air is cool and carries a faint, musty odor that wafts from the darkness ahead. Moss and small flowers cluster around the rocks, making the entrance almost inviting, despite the unknown lying within. Your torch flickers as a gentle breeze caresses your face, and the sound of dripping water echoes from the depths. What would you like to do?",

    "The grandeur of the royal court unfolds before you as you step through the towering, ornate doors. Vaulted ceilings adorned with gold leaf and magnificent chandeliers loom overhead, casting a warm glow over the bustling assembly of nobles, knights, and emissaries. The king, seated upon his majestic throne at the far end of the hall, notices your arrival and gestures subtly for you to approach. Murmurs fill the air, and many eyes turn to follow your progress down the long, red carpet. What would you like to do?",

    "Surrounded by the towering, ancient trees of the enchanted forest, you are bathed in a kaleidoscope of light filtering through the leaves, painting the world in hues of green and gold. The air is alive with the whispers of the forest; the songs of birds, the rustle of hidden creatures, and the gentle hum of magic. Ahead, a clear, sparkling stream cuts through the woods, dancing over rocks and under bridges made from intertwining branches. To your right, a narrow path veers off, disappearing into clusters of luminescent flowers and thickets of berry-laden bushes. What would you like to do?",

    "As you tread the dusty, cobblestone streets of the bustling city, a cacophony of sounds fills your ears; the clattering of horse hooves, the lively banter of market vendors, and the distant tolling of a church bell. The scent of spices and roasting meat wafts from the food stalls, while beggars and street performers jostle for space at your feet. Ahead, you can see the imposing city gates, guarded by armed soldiers in shiny armor. Beyond them lies the unknown world beyond the city walls, a land of mystery and adventure. What do you choose to do?",
        
    "You find yourself standing on the edge of an arid desert, with nothing but rolling sand dunes stretching out as far as the eye can see. The scorching sun beats down upon your back, and the air is thick with dust and heat. In the distance, a shimmering mirage teases you, enticing you to venture forth into the unforgiving sands. To your left, an ancient, weather-beaten caravan lays scattered across the desert floor, its inhabitants nowhere to be seen. What do you decide to do?",

    "In the tranquil depths of a subterranean ocean, you glide through the inky blackness, illuminated by the delicate glow of bioluminescent creatures that flit about your path like fireflies. The gentle current carries you along, and you marvel at the strange, alien forms of marine life that surround you; giant jellyfish with tentacles as long as your arm, schools of iridescent fish darting through kelp forests, and the occasional glimpse of a massive, unseen beast lurking in the shadows. What will be your next action?",

    "You awake in a dimly lit, cobweb-filled room, your memory foggy and your body aching from some unremembered ordeal. The only light comes from a flickering candle on the table beside you, casting eerie shadows across the dusty floor. A heavy, iron door stands before you, adorned with ancient symbols and locked fast by rusted chains. An unsettling silence hangs in the air, broken only by the distant sound of dripping water. What is your first course of action?",

    "Standing atop a rickety wooden tower that pierces the sky, you feel the cool wind whipping through your hair as the world below stretches out before you. The sun sets in a fiery blaze over the horizon, casting long shadows across the rolling hills and sparkling rivers below. A sense of exhilaration fills your chest as you consider the endless possibilities that lay within your grasp. What will be your next action?",

    "Stranded on a desolate island with nothing but your wits and a few basic supplies, you find yourself at the mercy of nature's whims. The relentless sun beats down upon you while the ocean roars in the distance, reminding you that escape may not be an easy task. Yet, amidst this desolation, there is beauty to be found; lush vegetation, crystal-clear streams, and even occasional visits from curious wildlife. What will you do first?"]

    #basically just generate one more!

    prompt = "Please generate a 10th item for this list:\n"

    # Iterate through each string in the list
    for index, example in enumerate(examples, start=1):
        # Print each string with its number in front
        prompt += (f"{index}. {example}")


    conversation = [{"role": "user", "content": prompt}]


    await send_message_and_stream_response(conversation, message_callback)

    



def generateLocation():
    pass

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
        #get inventory from the database
        #convert inventory to string

        invString = inventory.toString()

        prompt = "You are in charge of inventory management for an adventure game! The user currently has the following inventory items: " + invString + "\n\nPlease provide the updated contents of the user inventory after their turn. User's turn:" + user_input

        response = generateText(prompt)

        #parse response to list and validate

        writeInventory(newInventory)


#check if currently talking to a character exists in character db
def checkCharacterInteraction(): # takes like last n messages as input or something
    pass #returns list of characters the character is currently interacting with or NULL if they aren't interacting with any


# creates a character and generates image, stores character in db
def createCharacter():
    pass


def rollDice(n): #rolls a dice, random number between 1 and n inclusive
    pass


def processTurn():
    pass