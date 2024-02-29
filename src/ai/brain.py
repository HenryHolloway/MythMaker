from src.database.inventoryDB import fetchInventory, writeInventory
from src.database.characterDB import fetchCharacterCard, writeCharacterCard
from src.database.locationDB import *

from src.ai.textGeneration import *
from src.ai.imageGeneration import generateBackgroundImage, generateCharacterImage

import asyncio
import random

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

    prompt = "The following is a list of potential starting prompts for a text adventure game. Please follow the format and produce one more example for the list."

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




def changeInventory(conversation):
    oldInventory = fetchInventory()

    # Ensure oldInventory is a list of strings
    if oldInventory and isinstance(oldInventory[0], list):
        # If oldInventory is a list of lists, flatten it (example solution, adjust based on actual structure)
        oldInventory = [item for sublist in oldInventory for item in sublist]
    elif oldInventory and not all(isinstance(item, str) for item in oldInventory):
        # If oldInventory contains non-string elements, handle the error or convert them to strings
        print("Error: oldInventory contains non-string elements.")
        return False


    # Initialize variables to hold the most recent user and assistant responses
    user_response = ""
    assistant_response = ""

    # Iterate through the conversation to find the most recent user and assistant responses
    for message in reversed(conversation):
        if message["role"] == "user" and not user_response:
            user_response = message["content"]
        elif message["role"] == "assistant" and not assistant_response:
            assistant_response = message["content"]
        # Break the loop if both responses have been found
        if user_response and assistant_response:
            break

    
    prompt = "You are in charge of inventory management for an adventure game! The user currently has the following inventory items: "

    #check if oldInventory is empty
    if not oldInventory:
        prompt += "Inventory currently empty."

    else:
        prompt += ', '.join(oldInventory)
    
    if user_response != "":
        prompt += "\n\nMost recent user action: " + user_response
    
    prompt += "\nMost recent AI action: " + assistant_response + "\n\nPlease provide the updated contents of the user inventory after their turn. Think critically -- did the user consume or disperse any items? Did the AI give the user any items, or take any away? Please provide the updated inventory as a CSV formatted list. Your response should contain only inventory items and commas."

    conversation = [{"role": "user", "content": prompt}]

    response = send_message_and_static_response(conversation)
    print("Raw response: ", response["content"])

    # Scrape inventory from response
    newInventory = response["content"]
    if ":" in newInventory:
        newInventory = newInventory.split(":", 1)[1]
    newInventory = newInventory.strip().strip('\'"()[]{}')
    newInventory = newInventory.split('\n', 1)[0]
    print("newInventory ", newInventory)


    newInventory = newInventory.split(',')
    print("newInventory listified: ", newInventory)
    
    newInventory = [item.strip().title() for item in newInventory]
    
    print("newInventory after cleaning: ", newInventory)
    
    writeInventory(newInventory)

    if set(newInventory) != set(oldInventory):
        return newInventory
    else:
        return False


#check if currently talking to a character exists in character db
def checkCharacterInteraction(): # takes like last n messages as input or something
    pass #returns list of characters the character is currently interacting with or NULL if they aren't interacting with any


# creates a character and generates image, stores character in db
def createCharacter():
    pass


def rollDice(n, threshold):
    """
    Rolls a dice with 'n' sides and checks if the result is above a given threshold.
    
    Parameters:
    - n (int): The number of sides on the dice.
    - threshold (int): The threshold value to compare the roll against.
    
    Returns:
    - int: The number rolled.
    """
    roll_result = random.randint(1, n)
    return roll_result

def determineDiceRoll(conversation):
    """
    Determines if the user's most recent prompt and the last AI response require a dice roll to determine success.
    
    Parameters:
    - conversation (list): A list of dictionaries, where each dictionary represents a message in the conversation.
    
    Returns:
    - string: If successful, returns a string containing a description of the dice roll and outcome
    - bool: If unsuccessful, or if a dice roll is not required, returns False
    """
    if not conversation:
        return False  # No conversation to analyze
    
    # Extract the last user prompt and the last AI response
    user_response = None
    assistant_response = None
    for message in reversed(conversation):
        if message["role"] == "user" and user_response is None:
            user_response = message["content"]
        elif message["role"] == "assistant" and assistant_response is None:
            assistant_response = message["content"]
        if user_response and assistant_response:
            break
    
    
    prompt = "You are a game master AI for a text-based adventure game. You specialize in determining when dice-rolls are necessary for a user's turn. Dice rolls are required for various chance-based actions. Combat actions like attacking an enemy, defending against an attack,performing a stealth action, casting a spell, etc. Exploration Actions such as climbing a steep cliff, disarming a trap, unlocking a treasure chest, etc. Social interactions like persuading a guard to let you pass, bartering with a merchant, gathering information from a local, convincing an NPC to join your quest.\n\nThe following are the two most recent actions in the story:"

    prompt += "\nMost recent AI action: " + assistant_response

    prompt += "\n\nMost recent user action: " + user_response
    
    prompt += "\nPlease provide determine whether a dice roll is required, and if so, what number dice and threshold for success. You must respond in JSON format using the following template: {'reason':'What the user is rolling the dice to accomplish, e.g. unlock chest, convince guard. Usage: (User rolled a 2 while trying to REASON)', 'threshold':'the minimum number the user needs to roll for success', 'dice_size':'The highest number the user can roll'}. If you decide a dice roll is not necessary, leave the reason as 'NULL' and set n and threshold to -1."


    conversation = [{"role": "user", "content": prompt}]
    response = send_message_and_static_response(conversation, json=True)

    try:
        dice_roll_info = json.loads(response["content"])
        if dice_roll_info["reason"] != "NULL":
            n = int(dice_roll_info["dice_size"])
            threshold = int(dice_roll_info["threshold"])
            roll_result = rollDice(n, threshold)
            result_message = f"The user rolled a {roll_result} while trying to {dice_roll_info['reason'].lower()}. They needed a {dice_roll_info['threshold']}. They {'passed.' if roll_result >= threshold else 'failed.'}"
            return result_message
        else:
            return False
    except (ValueError, KeyError):
        return False


    

    



def processTurn():
    pass