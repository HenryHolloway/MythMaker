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
    
    examples = [
    "You stand before the mouth of a gaping cave, hidden by the thick underbrush at the mountain's base. The air is cool and carries a faint, musty odor that wafts from the darkness ahead. Moss and small flowers cluster around the rocks, making the entrance almost inviting, despite the unknown lying within. Your torch flickers as a gentle breeze caresses your face, and the sound of dripping water echoes from the depths. In your leather satchel, you find a flint and steel, a length of rope, a small dagger, and a crust of bread. What would you like to do?",
    
    "The grandeur of the royal court unfolds before you as you step through the towering, ornate doors. Vaulted ceilings adorned with gold leaf and magnificent chandeliers loom overhead, casting a warm glow over the bustling assembly of nobles, knights, and emissaries. The king, seated upon his majestic throne at the far end of the hall, notices your arrival and gestures subtly for you to approach. Murmurs fill the air, and many eyes turn to follow your progress down the long, red carpet. Clasped in your hand is a sealed parchment bearing the royal seal, a gift of fine silk in your sack, and a ring of introduction from a distant land. What would you like to do?",
    
    "Surrounded by the towering, ancient trees of the enchanted forest, you are bathed in a kaleidoscope of light filtering through the leaves, painting the world in hues of green and gold. The air is alive with the whispers of the forest; the songs of birds, the rustle of hidden creatures, and the gentle hum of magic. Ahead, a clear, sparkling stream cuts through the woods, dancing over rocks and under bridges made from intertwining branches. To your right, a narrow path veers off, disappearing into clusters of luminescent flowers and thickets of berry-laden bushes. Tucked in your cloak, you find a map of unknown lands, a compass that doesn’t point north, and a flask of enchanted water that promises to heal. What would you like to do?",
    
    "As you tread the dusty, cobblestone streets of the bustling city, a cacophony of sounds fills your ears; the clattering of horse hooves, the lively banter of market vendors, and the distant tolling of a church bell. The scent of spices and roasting meat wafts from the food stalls, while beggars and street performers jostle for space at your feet. Ahead, you can see the imposing city gates, guarded by armed soldiers in shiny armor. Beyond them lies the unknown world beyond the city walls, a land of mystery and adventure. Within your coat pocket, you find a handful of copper coins, a tin whistle said to call upon the city's unseen protectors, and a worn leather-bound journal filled with notes and sketches. What would you like to do?",
    
    "You find yourself standing on the edge of an arid desert, with nothing but rolling sand dunes stretching out as far as the eye can see. The scorching sun beats down upon your back, and the air is thick with dust and heat. In the distance, a shimmering mirage teases you, enticing you to venture forth into the unforgiving sands. To your left, an ancient, weather-beaten caravan lays scattered across the desert floor, its inhabitants nowhere to be seen. Strapped to your back is a water skin, nearly empty, alongside a curved scimitar, a compass, and a wide-brimmed hat to shield you from the sun's merciless rays. What would you like to do?",
    
    "In the tranquil depths of a subterranean ocean, you glide through the inky blackness, illuminated by the delicate glow of bioluminescent creatures that flit about your path like fireflies. The gentle current carries you along, and you marvel at the strange, alien forms of marine life that surround you; giant jellyfish with tentacles as long as your arm, schools of iridescent fish darting through kelp forests, and the occasional glimpse of a massive, unseen beast lurking in the shadows. Clipped to your belt, a waterproof pouch contains a mysterious, ancient key, a small knife with a handle carved from bone, and a crystal that pulses softly with its own inner light. What would you like to do?",
    
    "You awake in a dimly lit, cobweb-filled room, your memory foggy and your body aching from some unremembered ordeal. The only light comes from a flickering candle on the table beside you, casting eerie shadows across the dusty floor. A heavy, iron door stands before you, adorned with ancient symbols and locked fast by rusted chains. An unsettling silence hangs in the air, broken only by the distant sound of dripping water. On the floor beside you, there's a backpack containing a scroll of ancient lore, a lockpick set, and a potion of strength. What would you like to do?",
    
    "Standing atop a rickety wooden tower that pierces the sky, you feel the cool wind whipping through your hair as the world below stretches out before you. The sun sets in a fiery blaze over the horizon, casting long shadows across the rolling hills and sparkling rivers below. A sense of exhilaration fills your chest as you consider the endless possibilities that lay within your grasp. Tied around your waist, a satchel reveals an assortment of provisions; a spyglass, a bundle of arrows, and a map marked with a location labeled 'The Lost City.' What would you like to do?",
    
    "Stranded on a desolate island with nothing but your wits and a few basic supplies, you find yourself at the mercy of nature's whims. The relentless sun beats down upon you while the ocean roars in the distance, reminding you that escape may not be an easy task. Yet, amidst this desolation, there is beauty to be found; lush vegetation, crystal-clear streams, and even occasional visits from curious wildlife. Clutched in your fist, a survival knife, a fire starter, a small fishing net, and a journal for documenting the island's secrets. What would you like to do?"]

    #basically just generate one more!

    prompt = "Please generate another item for this list."

    # Iterate through each string in the list
    for index, example in enumerate(examples, start=1):
        # Print each string with its number in front
        prompt += (f"\n\n\n{example}")


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


def checkInventoryChangeUser(user_input):
    prompt = "The following is a user prompt for an adventure game:\n" + user_input + "\n\nDoes the user acquire any items or disperse any items? This includes money. Answer only with yes or no."

    conversation = [{"role": "user", "content": prompt}]

    # This line directly calls the function with the provided inputs.
    response = send_message_and_static_response(conversation)

    if 'yes' in response:
        return true
    if 'no' in response:
        return false


def changeInventoryUser(conversation):
    user_input = conversation[-1]['content']

    if checkInventoryChangeUser(user_input):
        oldInventory = fetchInventory()

        prompt = "You are in charge of inventory management for an adventure game! The user currently has the following inventory items: " + oldInventory + "\n\nPlease provide the updated contents of the user inventory after their turn. User's turn:" + user_input + "Please provide the inventory as a CSV; your response should contain only inventory items and commas"


        conversation = [{"role": "user", "content": prompt}]

        response = send_message_and_static_response()

        #scrape inventory from response
        newInventory = response.split(',')

        writeInventory(newInventory)




def checkInventoryChangeAI(ai_message):
    prompt = "The following is a prompt for an adventure game:\n" + ai_message + "\n\nDoes the user acquire any items or disperse any items? This includes money. Answer only with yes or no."

    conversation = [{"role": "user", "content": prompt}]

    # This line directly calls the function with the provided inputs.
    response = send_message_and_static_response(conversation)

    if 'yes' in response:
        return true
    if 'no' in response:
        return false


def changeInventoryAI(conversation):
    ai_message = conversation[-1]['content']

    if checkInventoryChangeUser(user_input):
        oldInventory = fetchInventory()

        prompt = "You are in charge of inventory management for an adventure game! The user currently has the following inventory items: " + oldInventory + "\n\nPlease provide the updated contents of the user inventory after their turn. User's turn:" + ai_message + "Please provide the inventory as a CSV; your response should contain only inventory items and commas"


        conversation = [{"role": "user", "content": prompt}]

        response = send_message_and_static_response()

        #scrape inventory from response
        newInventory = response.split(',')

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