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
    "Your journey to the caverns of Algorath begins as you stand before the entrance, with tales of ancient magic and untold riches fueling your resolve. The land is split by an eternal twilight, casting long shadows and brilliant hues across the landscape. Your objective is clear, but the path is yours to choose. In your leather satchel, you find: \n- A Whispering Blade \n- 12 Obsidian Coins \n- A lantern that burns without oil \n- A parchment with cryptic inscriptions. \nWhat would you like to do?",
    
    "Welcome to Erendorn, a bustling city where the arcane and the mundane intertwine under the watchful eyes of the Archmages. As you navigate through the crowded streets, whispers of power struggles and dark secrets reach your ears. Your destiny awaits, but how you reach it is yet to be written. In your possessions, you discover: \n- An Archmage's Wand \n- 15 Gold Coins \n- A miniature mechanical bird \n- A sealed envelope with a mysterious insignia. \nWhat would you like to do?",
    
    "The mystic forests of Fae'lyn envelop you, a realm where the ancient trees are said to be guardians of powerful secrets. The air is thick with magic, and every leaf and stone seems to watch your every move. Paths both hidden and visible stretch before you, inviting exploration. Among your belongings are: \n- A Bow of the Verdant Guardian \n- 10 Luminous Coins \n- A scroll of the woodland path \n- A flask of moonwell water. \nWhat would you like to do?",
    
    "Zephyr, the merchant city, teems with life, its streets a testament to the wealth and diversity it harbors. Here, fortunes can be made or lost with a single deal, and your wits will be your greatest asset. Adventure calls from every corner, promising both peril and reward. In your coat pocket, you find: \n- A Merchant's Cane \n- 18 Zephyrian Coins \n- A ledger capturing debts owed to you \n- A cloak woven with threads of concealment. \nWhat would you like to do?",
    
    "The Searing Expanse stretches before you, a vast desert of rolling dunes and scorching sun. Legends tell of ancient cities buried beneath the sands, awaiting discovery by those brave enough to face the desert's wrath. Your journey across the sands will be demanding, yet potentially rewarding. Your gear includes: \n- A Sunforged Scimitar \n- 14 Sunswept Gems \n- A sunshade cloak \n- A serpent charm. \nWhat would you like to do?",
    
    "Beneath the tranquil surface of Mirror Lake lies a world of wonder and danger, illuminated by the glow of bioluminescent creatures. The lake's depths are uncharted, hiding secrets in the dark water. Your exploration will reveal the mysteries that lie beneath. You carry: \n- A Trident of Currents \n- 16 Pearl Coins \n- A waterproof satchel with a map of underwater caverns \n- A potion for breathing under the depths. \nWhat would you like to do?",
    
    "The echoes of your footsteps fill the air as you awaken in the forgotten halls of Castle Moragath. The castle, shrouded in mystery and darkness, calls to those with the courage to uncover its secrets. What lies within these walls is a tale yet to be told, and your story begins now. In your grasp, you find: \n- A Torchbearer's Halberd \n- 10 Shadow Shillings \n- A locket that glows faintly \n- A tome filled with lost lore. \nWhat would you like to do?",
    
    "High above the land, atop the Eagle's Cradle, the world appears vast and unending. The winds carry tales of distant lands and forgotten cities, beckoning you to explore the unknown. The sky is both a map and a mystery, and your adventure is just beginning. Tied around your waist, you have: \n- A Windwhisper Crossbow \n- 20 Stormfeather Tokens \n- A spyglass that sees beyond horizons \n- Gauntlets that steady your aim. \nWhat would you like to do?",
    
    "The Emerald Exile, a dense jungle teeming with life and peril, stands before you as the ultimate test of survival and ingenuity. Ancient ruins lie hidden under the canopy, home to treasures and traps alike. Your journey through the jungle will be filled with challenges, both seen and unseen. You are equipped with: \n- A Vine-Tangled Staff \n- 11 Jade Coins \n- A camouflaged tarp \n- A trapping kit. \nWhat would you like to do?"]


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
        return True
    if 'no' in response:
        return False




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

    
    prompt = "You are in charge of inventory management for an adventure game! Our last record of the user's inventory is as follows: "

    #check if oldInventory is empty
    if not oldInventory:
        prompt += "Inventory currently empty."

    else:
        prompt += ', '.join(oldInventory)
    
    if user_response != "":
        prompt += "\n\nMost recent user action: " + user_response
    
    prompt += "\nMost recent AI action: " + assistant_response + "\n\nPlease provide the updated contents of the user inventory after their turn. Think critically -- what happened in the last turn? Remember, anything and everything that is handed to or taken from the player must be accounted for. Your job isn't to pass judgement, you are simply an incredibly dilligent and accurate record keeper. Provide a JSON-formatted response following this template: {'justification':'why you think the inventory changed or did not change. be specific, use chain-of-thought reasoining.','inventory':'Formatted as Item 1,Item 2,Item 3 or NULL' }"

    conversation = [{"role": "user", "content": prompt}]

    response = send_message_and_static_response(conversation, json=True)
    print("Raw response: ", response["content"])

    # Scrape inventory from response
    newInventory = json.loads(response["content"])["inventory"]
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


def rollDice(threshold, dice_size):
    """
    Rolls a dice with 'n' sides and checks if the result is above a given threshold.
    
    Parameters:
    - n (int): The number of sides on the dice.
    - threshold (int): The threshold value to compare the roll against.
    
    Returns:
    - int: The number rolled.
    """
    roll_result = random.randint(1, dice_size)
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
    
    prompt += "\nPlease provide determine whether a dice roll is required, and if so, what number dice and threshold for success. You must respond in JSON format using the following template: {'reason':'What the user is rolling the dice to accomplish, e.g. unlock chest, convince guard. Usage: (User rolled a 2 while trying to REASON)', 'threshold':'the minimum number the user needs to roll for success', 'dice_size':'The highest number the user can roll'}. If you decide a dice roll is not necessary, leave the reason as 'NULL' and set threshold and dice_size to -1."


    conversation = [{"role": "user", "content": prompt}]
    response = send_message_and_static_response(conversation, json=True)

    try:
        dice_roll_info = json.loads(response["content"])
        if dice_roll_info["reason"] != "NULL":
            threshold = int(dice_roll_info["threshold"])
            dice_size = int(dice_roll_info["dice_size"])
            roll_result = rollDice(threshold, dice_size)
            result_message = f"The user rolled a {roll_result} on a {dice_size}-sided dice while trying to {dice_roll_info['reason'].lower()}. They needed a {threshold}. They {'passed.' if roll_result >= threshold else 'failed.'}"
            return result_message
        else:
            return False
    except (ValueError, KeyError):
        return False


    

    



def processTurn():
    pass