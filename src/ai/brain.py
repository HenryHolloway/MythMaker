from src.database.inventoryDB import fetchInventory, writeInventory
from src.database.characterDB import fetchCharacterCard, writeCharacterCard
from src.database.locationDB import *

from src.ai.textGeneration import *
from src.ai.imageGeneration import generateBackgroundImage, generateCharacterImage

import asyncio
import random

#this will handle prompting the LLM for story, inventory checks, image generation etc.

#TO DO logging. verbose with print

async def generateAdventureStart(message_callback:callable) -> None:
    """
    Generate the starting point of an adventure.

    This function generates the initial setting and context for an adventure
    game. It uses predefined examples to create a prompt for the AI model to 
    generate a new adventure start. The generated prompt is then sent to the 
    AI model, and the response is streamed back using the provided callback 
    function.

    Args:
        message_callback (callable): A callback function to handle each part 
                                     of the response. It should accept three 
                                     arguments: sender (str), message (str), 
                                     and done (bool).

    Returns:
        None
    """
    print("Called function generateAdventureStart in module brain")

    #TO DO add inventory specifics to these templates.
    
    examples = [

    "In the heart of a lush, verdant forest lies the hidden village of Elmsbrook, nestled among the ancient trees. The gentle rustling of leaves overhead fills the air as you approach the quaint settlement, its cobblestone streets lined with charming cottages and bustling shops. A faint scent of woodsmoke hangs in the atmosphere, mingling with the crisp aroma of fresh blooms. You hear laughter and lively conversation spilling out from a nearby tavern as you enter town.\nAs you venture further into Elmsbrook, a grizzled old traveler beckons to you, his worn leather pack filled with odd trinkets and mysterious artifacts. He whispers of an ancient legend that speaks of a hidden treasure buried deep within the forest by an ancient wizard long ago. The reward for those brave enough to seek it out? Unimaginable wealth beyond measure. With the traveler's cryptic clues in hand, you now find yourself at the crossroads of your destiny. What would you like to do? Inventory contents: {\"Shortsword\": 1,\"Gold Coins\": 50,\"Healing Potion\": 2,\"Map of Elmsbrook\": 1}",

    "You stand on the bustling streets of Zephyria, a vibrant city pulsating with energy. Towering skyscrapers cast long shadows across the cobblestone roads as they stretch towards the azure sky overhead. The air is filled with the tantalizing aroma of exotic spices and the lively chatter of market vendors hawking their wares. Music fills your ears as street performers play melodious tunes on a variety of instruments, while street acrobats dazzle passersby with their mesmerizing feats of agility and strength.\nSuddenly, you hear whispers of a secret society known only as The Elysian Order, rumored to possess unimaginable power and influence within the city's underbelly. Some say they guard a long-lost artifact capable of bringing about untold prosperity or devastating doom - depending on whose side you stand on. It is said that only those pure of heart can hope to uncover its secrets.\nFeeling an undeniable pull towards this enigmatic mystery, you find yourself drawn into a labyrinthine web of deception and intrigue as you navigate the treacherous streets of Zephyria. What would you like to do? Inventory contents: {\"Handaxe\": 1,\"Silver Coins\": 30,\"Invisibility Cloak\": 1,\"Zephyria City Map\": 1}",

    "Welcome to the remote, isolated village of Icehaven, nestled high atop a snowy mountain peak. This frozen fortress is home to a tight-knit community of hardy souls who have braved harsh elements and treacherous terrain for generations. The chill of winter's icy grip permeates every corner of the village as you make your way through its narrow, winding streets.\nAs you approach the village square, you notice an old woman hunched over in the shadows, her gnarled hands clutching a worn parchment tightly to her chest. She whispers of a prophecy foretelling that one day, a traveler will come seeking the power hidden within the mountains' depths - a power capable of changing the fate of all who dwell on this frigid earth.\nAs you listen intently to the old woman's words, your heart swells with determination as you realize that destiny has chosen you for this noble quest. You feel the weight of the leather pack hanging by your side, its contents echoing the purpose you have undertaken on this journey. What would you like to do? Inventory contents: {\"Frost-Encrusted Axe\": 1,\"Silver Coins\": 40,\"Warm Fur Cloak\": 1,\"Icehaven Map\": 1}",
    
    
    "You stand at the edge of a vast, deserted beach, the warm sand shifting beneath your feet as you take in the breathtaking view of the azure ocean stretching out before you. The salty breeze rustles through your hair as you listen to the distant crash of waves against the shoreline. In the distance, you spot a small, uninhabited island shrouded in mist and mystery.\nRumors speak of an ancient temple buried deep within its verdant foliage, guarded by dangerous creatures and deadly traps. Within its hallowed halls lies a priceless artifact known as the Emerald Eye - said to grant eternal wisdom and boundless power to those who possess it. As you gaze longingly at the island, the call of adventure beckons you forth, urging you to embark on this perilous journey in pursuit of untold riches and unimaginable knowledge. What would you like to do? Inventory contents: {\"Cutlass\": 1,\"Gold Coins\": 20,\"Healing Herbs\": 3,\"Island Map\": 1}",
    
    "In the heart of a sprawling, lush jungle lies the enchanted village of Emberglade, where the sounds of exotic birdsong and distant howls fill the air. The vibrant foliage creates an ethereal canopy overhead as you traverse the winding paths leading to the center of this magical settlement.\nAs you approach the village square, you come across a wise old shaman who speaks of an ancient prophecy foretelling that one day, a chosen hero will arise to bring balance and harmony back to the jungle's inhabitants. This hero is said to possess extraordinary powers granted by the spirits themselves - abilities that could tip the scales between order and chaos for all living things.\nAs you listen intently to the shaman's words, your heart swells with determination as you realize that destiny has chosen you for this noble quest. You feel the weight of the leather pack hanging by your side, its contents echoing the purpose you have undertaken on this journey. What would you like to do? Inventory contents: {\"Golden Staff\": 1,\"Gold Coins\": 15,\"Healing Potion\": 2,\"Emberglade Map\": 1}",
    
    # modern environments
    "In the year 2018, in the heart of a bustling town, you find yourself standing in front of a modern coffee shop. The sun is setting, casting a golden hue over the urban landscape. The air is filled with the comforting aroma of freshly brewed coffee mixed with the distant hum of traffic. As people rush by, you notice a flyer pinned to a nearby community board. It reads: 'Mysterious Disappearance of Local Historian - Last Seen at the Old Museum on Oak Street.' Intrigued, you decide to investigate further.\nAs you approach the museum, an old man with a weathered face and wise eyes greets you. He claims to be a friend of the missing historian and warns you of dark secrets lurking within the old building. With a sense of determination, you feel the weight of your backpack, knowing it could prove useful. What would you like to do? Inventory contents: {\"High-Beam Flashlight\": 1,\"Cash\": 50,\"Lock-Picking Tools\": 1,\"Museum Map\": 1}",

    "In the year 2022, in the heart of a tranquil suburban town, you are standing in front of a quaint bookstore that has been a local treasure for decades. The scent of old books and freshly printed pages fills the air as you step inside. The cozy, dimly-lit interior invites you to explore its endless shelves of literary wonders. While browsing, you come across a leather-bound book with no title. Inside the cover, there's an inscription: 'Seek the Hidden Library - Where Time Stands Still.'\nCuriosity piqued, you approach the elderly shopkeeper, who reveals a map hidden within the pages of the book. This map allegedly leads to a secret library said to contain knowledge and artifacts from ancient civilizations. With your backpack slung over your shoulder, you prepare for the journey ahead. What would you like to do? Inventory contents: {\"Magnifying Glass\": 1,\"Cash\": 30,\"Digital Camera\": 1,\"Library Map\": 1}",

    # sci-fi environments:
    "In the year 2175, you find yourself in the heart of the futuristic city of Neonspire, a dazzling metropolis where towering skyscrapers adorned with holographic advertisements pierce the sky. The streets are alive with the hum of hover cars and the chatter of robots and humans alike. As you walk through a bustling market square, the smell of synthetic foods mingles with the crisp scent of ozone from the numerous electronic devices on display. Suddenly, a small drone whizzes past you, dropping a data chip into your hand inscribed with the words 'The Omega Protocol.'\nCuriosity takes hold as you scan the chip using your wrist-mounted holo-device. It reveals a hidden message about a rogue AI that holds the power to either save or destroy Neonspire. With a sense of urgency, you check the contents of your high-tech utility belt. What would you like to do? Inventory contents: {\"Plasma Pistol\": 1,\"Credits\": 100,\"Portable Hacking Tool\": 1,\"Neonspire Map\": 1}",

    "In the year 3050, deep in the Alpha Centauri colony, you are stationed in the bustling spaceport city of Celestia Prime. The city floats above a gas giant, its shimmering architecture reflecting the stars. As you walk through the busy concourse filled with travelers from various planets, the air buzzes with interstellar languages and the scent of exotic alien foods. A broadcast appears on your holo-comm device, announcing that an ancient spaceship has been discovered on a distant moon, said to hold the secrets of an advanced extinct civilization.\nDetermined to unlock these secrets, you head to the nearest spaceport and board your personal starship. Your journey will be perilous, but you are prepared. What would you like to do? Inventory contents: {\"Laser Rifle\": 1,\"Credits\": 200,\"Quantum Scanner\": 1,\"Celestia Prime Map\": 1}"
    ]


    #basically just generate one more!

    prompt = "The following is a list of potential starting prompts for a text adventure game. Please follow the format and produce one more example for the list. Simply start your example, no need to say \"here you go\" every time. eNEVER WRITE TWO NEWLINES IN A ROW.\n"

    # Select 5 random examples from the list
    selectedExamples = random.sample(examples, 5)
    # Iterate through each selected example
    for index, example in enumerate(selectedExamples, start=1):
        # Print each string with its number in front
        prompt += (f"{index}. {example}")

    conversation = [{"role": "user", "content": prompt}]

    await sendMessageAndStreamResponse(conversation, message_callback)

    
async def generateNextTurn(conversation: dict, callback:callable, n: int = 50) -> None:
    """
    Generate the next turn in the conversation for a text-adventure game.

    This function takes the current conversation history and generates the next
    turn in the conversation. It uses the context of the last `n` messages to 
    craft a prompt for the AI model, which then generates a response. The response 
    is streamed back and handled by the provided callback function.

    Args:
        conversation (dict): The conversation history to send to the AI model.
        callback (callable): A callback function to handle each part of the response.
        n (int, optional): The number of recent messages to use as context. Defaults to 50.

    Returns:
        None
    """
    # Select the last n messages from the conversation for context
    recentConversation = conversation[-n:]

   
    conversationContext = "\n\n".join([f"{message['role']}: {message['content']}" for message in recentConversation])
    
    # Check if the previous response is a system message with the dice roll
    if recentConversation and recentConversation[-1]["role"] == "system" and "The user rolled" in recentConversation[-1]["content"]:
        systemMessage = recentConversation[-1]["content"]
        if "The user rolled" in systemMessage:
            if "They passed." in systemMessage:
                diceRollResult = "THE USER PASSED THEIR DICE-ROLL CHECK. YOUR RESPONSE SHOULD REFLECT THE SUCCESS OF THEIR ACTIONS. "
            elif "They failed." in systemMessage:
                diceRollResult = "THE USER FAILED THEIR DICE-ROLL CHECK. YOUR RESPONSE SHOULD REFLECT THE FAILURE OF THEIR ACTIONS. "
            else:
                diceRollResult = ""
        else:
            diceRollResult = ""
    else:
        diceRollResult = ""


    # Craft the prompt with specific instructions
    prompt = f"You are a dungeon master for a text-adventure game. You are in charge of the high-level decision making and world management. You are also required to 'switch' from DM mode and roleplay as the NPCs as required. The following is the most recent part of the game's story:\n{conversationContext}\n\n"
    
    if diceRollResult != "":
        prompt += diceRollResult * 3
    
    prompt += "If the user is engaging with an NPC, you are to roleplay as that NPC. While roleplaying, only respond with the dialogue of the NPC. For example, USER: \"what is your name?\" RESPONSE:\"My name is Elarin\", the woman replies. Don't give scene direction during roleplay unless absolutely necessary. Generally, do not make any decisions for the character. Simply provide a detailed explaination of what happens as a result of the user's last action, keeping in mind the game's tone and themes. AGAIN, NEVER make a decision on behalf of the user or tell the user how their character is feeling. Your response should be one, detailed paragraph, but may be longer if dialogue and action MUST occur in the same turn."
    
    # Add the prompt to the conversation for the LLM to process
    conversationWithPrompt = [{"role": "user", "content": prompt}]
    
    # Send the updated conversation to the LLM and stream the response to the callback
    await sendMessageAndStreamResponse(conversationWithPrompt, callback)

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

    response = sendMessageAndStaticResponse(conversation, json=True)
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

    # Ensure oldInventory is a dictionary with item names as keys and quantities as values
    if oldInventory and not isinstance(oldInventory, dict):
        print("Error: oldInventory is not in the expected dictionary format.")
        return False
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

    
    prompt = "You are in charge of inventory management for an adventure game! You will take the user's inventory, the user's last action, and the last AI action, and determine what items were obtained or lost during the user's last turn. You will then update the user's inventory accordingly. Think critically about what happened in the last turn. Remember, anything and everything that is handed to or taken from the player must be accounted for. Your job isn't to pass judgement, you are simply an incredibly dilligent and accurate record keeper. This means you must track not just the items obtained or dispersed, but the quantity as well. Provide a JSON-formatted response reflecting the inventory changes, following this template: {'justification':'<why you think the inventory changed. be specific, use chain-of-thought reasoning to determine which items need to be removed or added. Be verbose.>','<ITEM NAME>':'<QUANTITY>','<ITEM NAME>':'<QUANTITY>', etc. }"


    prompt += """
    Example 1:
    Input: 
    The user's current inventory is: {'Water Bottle': 1, 'Spare Ration Pack': 3, 'First-Aid Kit': 2, 'Survival Manual': 1}
    Most recent user action: burn the survival manual for warmth
    Most recent AI action: "What foolishness is this? You would burn the only guide that could help you survive in this desolate wasteland?" the tattered figure exclaims, their voice laced with a mix of concern and desperation. "You think the brief warmth it would bring is worth risking your life for? I gave you that manual to save you from certain doom, not to use as kindling! Look around, have you forgotten where we are? Every action has consequences, and burning away our only hope for survival is a reckless decision indeed."

    Response:
    { "justification": "The user burned the Survival Manual to gain warmth during their last turn, so we must subtract one instance of it from the inventory since it is no longer present. No other items were obtained or removed during this turn.", 
    "Water Bottle": 1,
    "Spare Ration Pack": 3,
    "First-Aid Kit": 2 }
    """


    #check if oldInventory is empty
    if not oldInventory:
        prompt += "Inventory currently empty. "

    else:
        prompt += "The user's current inventory is: " + str(oldInventory)
    

    prompt += " Most recent user action: " + user_response

    
    prompt += " Most recent AI action: " + assistant_response 


    


    conversation = [{"role": "user", "content": prompt}]

    response = sendMessageAndStaticResponse(conversation, json=True)
    print("Raw response: ", response["content"])

    # Scrape inventory from response
    response_content = json.loads(response["content"])

    # Extract inventory items from the response content
    newInventory = {}
    for key, value in response_content.items():
        if key.lower() != 'justification':
            # Clean the key to ensure proper formatting
            clean_key = key.replace('_', ' ').title()
            try:
                quantity = int(value)
            except ValueError:
                quantity = value.strip()
            newInventory[clean_key] = quantity

    print("newInventory : ", newInventory)
    
    print("newInventory after cleaning: ", newInventory)
    
    writeInventory(newInventory)

    if json.dumps(newInventory, sort_keys=True) != json.dumps(oldInventory, sort_keys=True):
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
    
    
    prompt = "You are a game master AI for a text-based adventure game. You specialize in determining when dice-rolls are necessary for a user's turn. Dice rolls are required for certain difficult chance-based actions. Combat actions like attacking an enemy, defending against an attack, performing a stealth action, casting a spell, etc. Exploration Actions such as climbing a steep cliff, disarming a trap, unlocking a treasure chest, etc. Social interactions like persuading a guard to let you pass, bartering with a merchant, etc. Dice rolls are NOT required for simpler, guaranteed actions or basic tasks that do not have an element of significant risk or chance. For example: Walking through an open field,Having a casual conversation, Picking up a common object from the ground, Eating or drinking at an inn, Entering a building, Reading a sign or a book, etc.\n\nThe following are the two most recent actions in the story:"

    prompt += "\nMost recent AI action: " + assistant_response

    prompt += "\n\nMost recent user action: " + user_response
    
    prompt += "\nPlease determine whether a dice roll is required, and if so, what dice and threshold for success. Dice rolls are for situations where a character's success or failure isn't guaranteed. If anyone can easily accomplish a task, a dice roll is not necessary. Do not make assumptions about the user's action (i.e. if their action is to go to a tavern, don't assume they're checking for information.) You must respond in JSON format using the following template: {'reason':'What the user is rolling the dice to accomplish. Usage: (User rolled a 2 while trying to REASON)', 'threshold':'the minimum number the user needs to roll for success', 'dice_size':'The highest number the user can roll'}. If you decide a dice roll is not necessary, leave the reason as 'NULL' and set threshold and dice_size to -1."


    conversation = [{"role": "user", "content": prompt}]
    response = sendMessageAndStaticResponse(conversation, json=True)

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



def generateAdventureName(conversation):
    print("Starting generateAdventureName function.")
    
    if not conversation:
        print("No conversation available. Returning default name 'Unnamed Adventure'.")
        return "Unnamed Adventure"  # Default name if no conversation is available

    print("Combining conversation messages into a single text.")
    combined_text = "".join([message["content"] for message in conversation])
    n = 1000
    last_n_chars = combined_text[-n:]
    print(f"Extracted the last {n} characters of the combined text.")

    prompt = "Create a title for this adventure."
    prompt += " Adventure: ```" + last_n_chars + "```"
    prompt += " Again, respond with just 3-4 word title. Format as such: {'title': '<TITLE GOES HERE>'}"
    print("Constructed the prompt for generating the adventure name.")

    conversation = [{"role": "user", "content": prompt}]
    print("Sending prompt to AI for response.")
    response = sendMessageAndStaticResponse(conversation, json=True)

    try:
        adventure_name = json.loads(response["content"])["title"]
        print(f"Received adventure name: {adventure_name}")
        return adventure_name
    except (KeyError, json.JSONDecodeError):
        print("Error encountered. Returning default name 'Unnamed Adventure'.")
        return "Unnamed Adventure"


    


def processTurn():
    pass