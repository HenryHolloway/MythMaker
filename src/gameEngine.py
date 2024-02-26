from src.ui.applicationUI import appUI
import src.ai.brain as brain

from src.ai.textGeneration import send_message_and_stream_response

import os
import json
import threading
import asyncio


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


    # def process_turn(self, conversation):
    #     # Simulate processing and getting an AI response
    #     # Note: Here we consider the last message from the user for simplicity
        
    #     if conversation:
    #         last_message = conversation[-1]["text"]  # Get the last user message
    #         ai_response_text = "Echo: " + last_message  # Simulated AI response
            
    #         send_to_api_and_stream(last_message, self.ui.append_message_and_update)

    #         # Append the AI response to the conversation
    #         conversation.append({
    #             "speaker": "AI",
    #             "text": ai_response_text,
    #             "color": "#EEEEEE"  # Grey background for AI messages
    #         })

    #     self.save_conversation()
    #     return conversation



    def process_turn(self, conversation):
        # You might need to adjust the creation of the thread for each turn processing
        # depending on how you want to manage the interaction (e.g., queueing messages)
        threading.Thread(target=self.call_async_process, args=(conversation,), daemon=True).start()

    def call_async_process(self, conversation):
        # Running the asyncio event loop in a thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        loop.run_until_complete(send_message_and_stream_response(conversation, self.ui.append_message_and_update))
        loop.close()

    def save_conversation(self, filepath="conversation.json"):
        with open(filepath, "w") as file:
            json.dump(self.conversation, file, indent=4)


    def load_conversation(self, filepath="conversation.json"):
        try:
            with open(filepath, "r") as file:
                self.conversation = json.load(file)
        except FileNotFoundError:
            print("Conversation file not found. Starting a new conversation.")
    