from src.ui.applicationUI import appUI
import src.ai.brain as brain

from src.ai.textGeneration import send_message_and_stream_response

import os
import json
import threading
import asyncio


class GameEngine:
    def __init__(self, master):
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

        self.conversation = []

        self.ui = appUI(master=master, input_callback=self.process_turn, conversation=self.conversation)

    def save_conversation(self, filepath="conversation.json"):
        with open(filepath, "w") as file:
            json.dump(self.conversation, file, indent=4)


    async def load_conversation(self, filepath="conversation.json"):
        try:
            with open(filepath, "r") as file:
                return json.load(file)
        except FileNotFoundError:
            print("Conversation file not found. Starting a new conversation.")
            await brain.generateAdventureStart(self.ui.append_message_and_update)
            return []

    async def start_game_async(self):
        # Display initial game UI/setup
        self.ui.display_stage(self.background, self.characters)
        
        # Load conversation after UI is ready
        self.conversation = await self.load_conversation()

    def start_game(self):
        # Since start_game is synchronous, use asyncio to run the asynchronous version
        asyncio.run(self.start_game_async())


    def process_turn(self, conversation):
        print("Saving conversation.")

        # You might need to adjust the creation of the thread for each turn processing
        # depending on how you want to manage the interaction (e.g., queueing messages)
        print("Callback successful. Starting thread.")
        threading.Thread(target=self.call_async_process, args=(conversation,), daemon=True).start()
        print("Thread started.")

    def call_async_process(self, conversation):
        self.save_conversation()
        self.call_async_send_stream(conversation)



    def call_async_send_stream(self, conversation):
        # Running the asyncio event loop in a thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        print("Calling async send & stream.")
        loop.run_until_complete(send_message_and_stream_response(conversation, self.ui.append_message_and_update))
        loop.close()






# async def test_send_message_and_stream_response():
#     conversation = [{"role": "user", "content": "Hi, how are you?"}]

#     def message_callback(sender, message):
#         # Adapt this function to log or print the message information to validate the behavior
#         print(f"Received message from {sender} with content '{message}'")

#     # This line directly calls the function with the provided inputs.
#     await send_message_and_stream_response(conversation, message_callback)
    