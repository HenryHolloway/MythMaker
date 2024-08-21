from src.ui.applicationUI import appUI
import src.ai.brain as brain

from src.ai.textGeneration import sendMessageAndStreamResponse

import src.database.characterDB as characterDB
import src.database.inventoryDB as inventoryDB
import src.database.locationDB as locationDB

import os
import json
import threading
import asyncio
import json
from datetime import datetime

class GameEngine:
    def __init__(self, master):
        # Directory initialization
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = os.path.join(self.base_dir, 'assets')
        
        self.items_dir = os.path.join(self.assets_dir, 'items')


        self.inventory = inventoryDB.fetchInventory()

        self.conversation = [{"role": "system", "content": "Loading!"}]

        self.ui = appUI(master=master, input_callback=self.process_turn, start_new_conversation_callback=self.start_new_conversation_thread, conversation=self.conversation)


    def start_new_conversation_thread(self):
        self.clear_initial_loading_message() 
        threading.Thread(target=self.call_async_generate_adventure_start, daemon=True).start()

    def clear_initial_loading_message(self):
        if self.ui.conversation and self.ui.conversation[0]["content"] == "Loading!":
            self.ui.conversation.pop(0)  # Remove the first message if it is the "Loading!" message

    def call_async_generate_adventure_start(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(brain.generateAdventureStart(self.ui.append_message_and_update))

        threading.Thread(target=brain.updateLocation, args=(self.ui.conversation, self.ui.display_stage), daemon=True).start()
       
        # Find the last system message in the conversation that contains the inventory
        for message in reversed(self.ui.conversation):
            if message["role"] == "assistant" and "Inventory contents:" in message["content"]:
                inventory_str = message["content"].split("Inventory contents: ")[1]
                try:
                    self.inventory = json.loads(inventory_str, strict=False)
                    inventoryDB.writeInventory(self.inventory)
                except json.JSONDecodeError as e:
                    print(f"Error decoding JSON: {e}")
                    self.inventory = {}
                # Remove the inventory part from the original message
                message["content"] = message["content"].split("Inventory contents: ")[0].strip()
                break
        else:
            self.inventory = {}

            self.ui.conversation = [{"role": "system", "content": "Loading!"}]
            self.ui.update_chat_display()
            print("UI conversation cleared.")

            self.start_new_conversation_thread()
            return

        if self.inventory is not False:
            new_inventory_str = ', '.join([f"{k}: {v}" for k, v in self.inventory.items()])
            self.ui.append_message_and_update("system", f"Inventory updated: {new_inventory_str}", done=True)


        loop.close()



    def process_turn(self, conversation):
        print("Saving conversation.")

        # You might need to adjust the creation of the thread for each turn processing
        # depending on how you want to manage the interaction (e.g., queueing messages)
        print("Callback successful. Starting thread.")
        threading.Thread(target=self.call_async_process, args=(conversation,), daemon=True).start()
        print("Thread started.")


    def call_async_process(self, conversation):
        self.async_process_turn(conversation)


    def async_process_turn(self, conversation):
        # Running the asyncio event loop in a thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)


        diceRoll = brain.determineDiceRoll(conversation)
        if diceRoll is not False:
            self.ui.append_message_and_update("system", diceRoll)

        loop.run_until_complete(brain.generateNextTurn(self.ui.conversation, self.ui.append_message_and_update))
        
        threading.Thread(target=brain.updateLocation, args=(self.ui.conversation, self.ui.display_stage), daemon=True).start()


        oldInventory = self.inventory
        self.inventory = brain.changeInventory(conversation)

        if self.inventory is not False:
            old_inventory_str = ', '.join([f"{k}: {v}" for k, v in oldInventory.items()])
            new_inventory_str = ', '.join([f"{k}: {v}" for k, v in self.inventory.items()])
            self.ui.append_message_and_update("system", f"Old Inventory: {old_inventory_str} \nInventory updated: {new_inventory_str}", done=True)



        self.ui.save_conversation()


        loop.close()







# async def test_sendMessageAndStreamResponse():
#     conversation = [{"role": "user", "content": "Hi, how are you?"}]

#     def message_callback(sender, message):
#         # Adapt this function to log or print the message information to validate the behavior
#         print(f"Received message from {sender} with content '{message}'")

#     # This line directly calls the function with the provided inputs.
#     await sendMessageAndStreamResponse(conversation, message_callback)
    