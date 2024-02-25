from ui.applicationUI import appUI
import ai.brain as brain

#from database.characterDB import CharacterDB
#from database.InventoryDB import InventoryDB

import os
import json

class GameEngine:
    def __init__(self, master):
        # Initialize conversation history
        self.conversation=[]
        self.load_conversation()



        # Directory initialization
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = os.path.join(self.base_dir, 'assets')
        
        self.backgrounds_dir = os.path.join(self.assets_dir, 'backgrounds')
        self.characters_dir = os.path.join(self.assets_dir, 'characters')
        self.items_dir = os.path.join(self.assets_dir, 'items')
        
        # Initializing Background
        self.default_background = os.path.join(self.backgrounds_dir, 'default_background.png')
        self.background = self.default_background



        self.characters = []


        #self.inventory = self.inventory_db.load_inventory()



        self.ui = appUI(master=master, input_callback=self.process_turn, conversation=self.conversation)


        


    def start_game(self):
        # Display initial game UI/setup
        self.ui.display_stage(self.background, self.characters)


    def process_turn(self, conversation):
        # Simulate processing and getting an AI response
        # Note: Here we consider the last message from the user for simplicity
        
        if conversation:
            last_message = conversation[-1]["text"]  # Get the last user message
            ai_response_text = "Echo: " + last_message  # Simulated AI response
            
            # Append the AI response to the conversation
            conversation.append({
                "speaker": "AI",
                "text": ai_response_text,
                "color": "#EEEEEE"  # Grey background for AI messages
            })

        self.save_conversation()
        return conversation


    def save_conversation(self, filepath="conversation.json"):
        with open(filepath, "w") as file:
            json.dump(self.conversation, file, indent=4)


    def load_conversation(self, filepath="conversation.json"):
        try:
            with open(filepath, "r") as file:
                self.conversation = json.load(file)
        except FileNotFoundError:
            print("Conversation file not found. Starting a new conversation.")
    