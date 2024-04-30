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

    "In the heart of a lush, verdant forest lies the hidden village of Elmsbrook, nestled among the ancient trees. The gentle rustling of leaves overhead fills the air as you approach the quaint settlement, its cobblestone streets lined with charming cottages and bustling shops. A faint scent of woodsmoke hangs in the atmosphere, mingling with the crisp aroma of fresh blooms. You hear laughter and lively conversation spilling out from a nearby tavern as you enter town.\nAs you venture further into Elmsbrook, a grizzled old traveler beckons to you, his worn leather pack filled with odd trinkets and mysterious artifacts. He whispers of an ancient legend that speaks of a hidden treasure buried deep within the forest by an ancient wizard long ago. The reward for those brave enough to seek it out? Unimaginable wealth beyond measure. With the traveler's cryptic clues in hand, you now find yourself at the crossroads of your destiny.\nYou have a leather pack slung over your shoulder. Within it lies:\n- A shortsword with an emerald hilt\n- An enchanted dagger\n- A quiver with 50 magical arrows\n- A ring of protection\nWhat would you like to do?",

    "You stand on the bustling streets of Zephyria, a vibrant city pulsating with energy. Towering skyscrapers cast long shadows across the cobblestone roads as they stretch towards the azure sky overhead. The air is filled with the tantalizing aroma of exotic spices and the lively chatter of market vendors hawking their wares. Music fills your ears as street performers play melodious tunes on a variety of instruments, while street acrobats dazzle passersby with their mesmerizing feats of agility and strength.\nSuddenly, you hear whispers of a secret society known only as The Elysian Order, rumored to possess unimaginable power and influence within the city's underbelly. Some say they guard a long-lost artifact capable of bringing about untold prosperity or devastating doom - depending on whose side you stand on. It is said that only those pure of heart can hope to uncover its secrets.\nFeeling an undeniable pull towards this enigmatic mystery, you find yourself drawn into a labyrinthine web of deception and intrigue as you navigate the treacherous streets of Zephyria. Your backpack contains: \n- A handaxe crafted by skilled elven blacksmiths\n- Twenty-two gold coins\n- A set of leather armor covered in mystical runes\n- A charm that attracts animals and small creatures\nWhat would you like to do?",

    "Welcome to the remote, isolated village of Icehaven, nestled high atop a snowy mountain peak. This frozen fortress is home to a tight-knit community of hardy souls who have braved harsh elements and treacherous terrain for generations. The chill of winter's icy grip permeates every corner of the village as you make your way through its narrow, winding streets.\nAs you approach the village square, you notice an old woman hunched over in the shadows, her gnarled hands clutching a worn parchment tightly to her chest. She whispers of a prophecy foretelling that one day, a traveler will come seeking the power hidden within the mountains' depths - a power capable of changing the fate of all who dwell on this frigid earth.\nAs you listen intently to the old woman's words, your heart swells with determination as you realize that destiny has chosen you for this noble quest. You feel the weight of the leather pack hanging by your side, its contents echoing the purpose you have undertaken on this journey. Within it lies:\n- A frost-encrusted axe \n- 12 polished stones \n- A flask of warming elixir \n- A trusty dagger hidden within a sheath\nWhat would you like to do?",
    
    
    "You stand at the edge of a vast, deserted beach, the warm sand shifting beneath your feet as you take in the breathtaking view of the azure ocean stretching out before you. The salty breeze rustles through your hair as you listen to the distant crash of waves against the shoreline. In the distance, you spot a small, uninhabited island shrouded in mist and mystery.\nRumors speak of an ancient temple buried deep within its verdant foliage, guarded by dangerous creatures and deadly traps. Within its hallowed halls lies a priceless artifact known as the Emerald Eye - said to grant eternal wisdom and boundless power to those who possess it. As you gaze longingly at the island, the call of adventure beckons you forth, urging you to embark on this perilous journey in pursuit of untold riches and unimaginable knowledge.\nYou feel the weight of the leather pack hanging by your side, its contents echoing the purpose you have undertaken on this journey. Within it lies:\n- A gleaming silver compass \n- 12 ornate vials filled with powerful potions \n- An enchanted map depicting the hidden path through the island's perilous depths \n- A mysterious key that some say can unlock the secret chamber housing the Emerald Eye\nWhat would you like to do?",
    
    "In the heart of a sprawling, lush jungle lies the enchanted village of Emberglade, where the sounds of exotic birdsong and distant howls fill the air. The vibrant foliage creates an ethereal canopy overhead as you traverse the winding paths leading to the center of this magical settlement.\nAs you approach the village square, you come across a wise old shaman who speaks of an ancient prophecy foretelling that one day, a chosen hero will arise to bring balance and harmony back to the jungle's inhabitants. This hero is said to possess extraordinary powers granted by the spirits themselves - abilities that could tip the scales between order and chaos for all living things.\nAs you listen intently to the shaman's words, your heart swells with determination as you realize that destiny has chosen you for this noble quest. You feel the weight of the leather pack hanging by your side, its contents echoing the purpose you have undertaken on this journey. Within it lies:\n- A golden staff adorned with intricate carvings \n- 12 luminescent crystals said to hold untold magical properties \n- A flask of life-giving elixir \n- An ancient scroll detailing the secrets of Emberglade's enigmatic spirit guardians\nWhat would you like to do?"]


    #basically just generate one more!

    prompt = "The following is a list of potential starting prompts for a text adventure game. Please follow the format and produce one more example for the list. NEVER WRITE TWO NEWLINES IN A ROW."

    # Iterate through each string in the list
    for index, example in enumerate(examples, start=1):
        # Print each string with its number in front
        prompt += (f"```{example}```")


    conversation = [{"role": "user", "content": prompt}]

    await send_message_and_stream_response(conversation, message_callback)

    
async def generateNextTurn(conversation, callback, n=50):
    # Select the last n messages from the conversation for context
    recent_conversation = conversation[-n:]
    conversation_context = " ".join([f"{message['role']}: {message['content']}" for message in recent_conversation])
    
    # Craft the prompt with specific instructions
    prompt = f"You are a dungeon master for a text-adventure game. You are in charge of the high-level decision making and world management. You are also required to 'switch' from DM mode and roleplay as the NPCs as required. The following is the most recent part of the game's story:\n{conversation_context}\n\nBased on the latest action taken by the user and the results of their dice throw (if applicable), describe the immediate consequences of their action. If the user failed their dice throw, they should face the full consequences of failing that action. If the user is engaging with an NPC, you are to roleplay as that NPC. Do not make any decisions for the character. Simply provide a detailed explaination of what happens as a result of the user's last action, keeping in mind the game's tone and themes. NEVER make a decision on behalf of the user or tell the user how their character is feeling. Your response should be one, detailed paragraph, but may be longer if dialogue and action must occur in the same role."
    
    # Add the prompt to the conversation for the LLM to process
    conversation_with_prompt = [{"role": "user", "content": prompt}]
    
    # Send the updated conversation to the LLM and stream the response to the callback
    await send_message_and_stream_response(conversation_with_prompt, callback)

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


def updateLocation(conversation, callback):
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


    prompt = "The following is a transcript from a text-adventure role-playing game. You are in charge of creating images of locations! Your job is to analyze the most recent gameplay and generate a prompt for stable diffusion that describes the location, to serve as a background image for the game.\Come up with a prompt to create a background image for this scene:\n\n"


    prompt += assistant_response + "\n"


    prompt += "Remember not to include characters or actions. You are creating BACKGROUND images. Format your response as such: {'location_description':'a detailed text description representing the current in-game location'}"

    conversation = [{"role": "user", "content": prompt}]

    response = send_message_and_static_response(conversation, json=True)
    print("Raw response: ", response["content"])

    response_content = json.loads(response["content"])

    location_change = response_content.get('location_change', 'False') == 'True'
    location_description = response_content.get('location_description', '')

    # Assuming generateBackgroundImage is a function from src/ai/imageGeneration.py that takes a prompt and returns a path to the generated image
    image_path = generateBackgroundImage(location_description)
    print(f"Location changed to: {location_description}. Background image updated at {image_path}.")

    callback(image_path)


    return


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

    
    prompt = "You are in charge of inventory management for an adventure game! Your last record of the user's inventory is as follows: "

    #check if oldInventory is empty
    if not oldInventory:
        prompt += "Inventory currently empty."

    else:
        prompt += ', '.join(oldInventory)
    
    if user_response != "":
        prompt += "\n\nMost recent user action: " + user_response
    else:
        prompt += "It's a new game. You must load the inventory into memory."
    
    prompt += "\nMost recent AI action: " + assistant_response + "\n\nPlease provide the updated contents of the user inventory after their turn. Think critically -- what happened in the last turn? Remember, anything and everything that is handed to or taken from the player must be accounted for. Your job isn't to pass judgement, you are simply an incredibly dilligent and accurate record keeper. Provide a JSON-formatted response following this template: {'justification':'<why you think the inventory changed. be specific, use chain-of-thought reasoining.>','Item 1':'<SHORT ITEM NAME>', Item 2:'<SHORT ITEM NAME>', etc. }. You don't need to keep any information other than the short name of the item. Follow the template exactly, replacing only the information between <>. If you believe the inventory did not change, just say {'justification':'<Your justification for why the inventory did not change, or why the inventory did change>'}"




    conversation = [{"role": "user", "content": prompt}]

    response = send_message_and_static_response(conversation, json=True)
    print("Raw response: ", response["content"])

    # Scrape inventory from response
    response_content = json.loads(response["content"])

    # Extract inventory items from the response content
    newInventory = [value for key, value in response_content.items() if key.lower().startswith('item')]
    print("newInventory listified: ", newInventory)
    
    newInventory = [item.strip().title().replace("'S ", "'s ") for item in newInventory]
    print("newInventory after cleaning: ", newInventory)
    
    writeInventory(newInventory)

    if set(newInventory) != set(oldInventory):
        return newInventory
    else:
        return False


#check if currently talking to a character exists in character db
def checkCharacterInteraction(): # takes like last n messages as input or something
    pass #returns list of characters the character is currently interacting with or NULL if they aren't interacting with any



# TO DO: Character Modifiers
def rollDice(threshold, dice_size):
    roll_result = random.randint(1, dice_size)
    return roll_result

def determineDiceRoll(conversation):
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
    
    
    prompt = "You are a game master AI for a text-based adventure game. You specialize in determining when dice-rolls are necessary for a user's turn. Dice rolls are required for certain difficult chance-based actions. Combat actions like attacking an enemy, defending against an attack, performing a stealth action, casting a spell, etc. Exploration Actions such as climbing a steep cliff, disarming a trap, unlocking a treasure chest, etc. Social interactions like persuading a guard to let you pass, bartering with a merchant, gathering information from a local, convincing an NPC to join your quest.\n\nThe following are the two most recent actions in the story:"

    prompt += "\nMost recent AI action: " + assistant_response

    prompt += "\n\nMost recent user action: " + user_response
    
    prompt += "\nPlease determine whether a dice roll is required, and if so, what dice and threshold for success. Ability checks are for situations where a character's success or failure isn't guaranteed. If anyone can easily accomplish a task, don't ask for an ability check. You must respond in JSON format using the following template: {'reason':'What the user is rolling the dice to accomplish. Usage: (User rolled a 2 while trying to REASON)', 'threshold':'the minimum number the user needs to roll for success', 'dice_size':'The highest number the user can roll'}. If you decide a dice roll is not necessary, leave the reason as 'NULL' and set threshold and dice_size to -1."


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