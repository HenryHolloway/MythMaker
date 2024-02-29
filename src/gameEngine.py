from src.ui.applicationUI import appUI
import src.ai.brain as brain

from src.ai.textGeneration import send_message_and_stream_response

import src.database.characterDB as characterDB
import src.database.inventoryDB as inventoryDB
import src.database.locationDB as locationDB

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

        self.conversation = [{"role": "system", "content": "Loading!"}]

        self.ui = appUI(master=master, input_callback=self.process_turn, reset=self.reset_game, conversation=self.conversation)

    def save_conversation(self, filepath="conversation.json"):
        with open(filepath, "w") as file:
            json.dump(self.ui.conversation, file, indent=4)


    def load_conversation(self, filepath="conversation.json"):
        try:
            with open(filepath, "r") as file:
                file_content = file.read()
                if file_content == "[]":
                    print("Conversation file not found. Starting a new conversation.")
                    self.start_new_conversation_thread()
                    return []
                else:
                    loaded_conversation = json.loads(file_content)  # Use json.loads to parse the string content
                    self.ui.conversation = loaded_conversation  # Update the UI's conversation
                    self.ui.update_chat_display()  # Reflect the loaded conversation in the UI
                    return loaded_conversation        
        except FileNotFoundError:
            print("File not found. Creating a new conversation file.")
            self.start_new_conversation_thread()
            return []

    def start_new_conversation_thread(self):
        self.clear_initial_loading_message() 
        threading.Thread(target=self.call_async_generate_adventure_start, daemon=True).start()

    def clear_initial_loading_message(self):
        if self.conversation and self.conversation[0]["content"] == "Loading!":
            self.conversation.pop(0)  # Remove the first message if it is the "Loading!" message

    def call_async_generate_adventure_start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(brain.generateAdventureStart(self.ui.append_message_and_update))

        newInventory = brain.changeInventory(self.ui.conversation)

        if newInventory is not False:
            self.ui.append_message_and_update("system", f"Inventory updated: {', '.join(newInventory)}", done=True)
        

        loop.close()

    async def start_game_async(self):
        # Display initial game UI/setup
        self.ui.display_stage(self.background, self.characters)

        self.ui.master.update_idletasks()        

        # Load conversation after UI is ready
        self.conversation = self.load_conversation()

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
        self.call_async_send_stream(conversation)


    def call_async_send_stream(self, conversation):
        # Running the asyncio event loop in a thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        diceRoll = brain.determineDiceRoll(conversation)
        if diceRoll is not False:
            self.ui.append_message_and_update("system", diceRoll)

        conversation = self.ui.conversation

        print("Calling async send & stream.")
        loop.run_until_complete(send_message_and_stream_response(conversation, self.ui.append_message_and_update))
        
        newInventory = brain.changeInventory(conversation)

        if newInventory is not False:
            self.ui.append_message_and_update("system", f"Inventory updated: {', '.join(newInventory)}", done=True)
        

        self.save_conversation()


        loop.close()


    def reset_game(self):
        print("reset_game called.")
        self.conversation = []

        self.ui.conversation = self.conversation
        print("Conversation cleared.")

        self.ui.update_chat_display()
        self.ui.master.update_idletasks()        
        print("Update chat display called.")

        self.save_conversation()
        print("Conversation saved.")


        characterDB.resetCharacterDB()
        inventoryDB.resetInventoryDB()
        locationDB.resetLocationDB()

        print("Databases reset.")

        print("Calling start_game()")
        self.start_game()
        






# async def test_send_message_and_stream_response():
#     conversation = [{"role": "user", "content": "Hi, how are you?"}]

#     def message_callback(sender, message):
#         # Adapt this function to log or print the message information to validate the behavior
#         print(f"Received message from {sender} with content '{message}'")

#     # This line directly calls the function with the provided inputs.
#     await send_message_and_stream_response(conversation, message_callback)
    