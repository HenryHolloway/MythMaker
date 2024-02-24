from ui.applicationUI import appUI
from ai.continuityManagement import *
#from database.characterDB import CharacterDB
#from database.InventoryDB import InventoryDB

import os

class GameEngine:
    def __init__(self, master):
        self.ui = appUI(master=master, input_callback=self.process_turn)



        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.assets_dir = os.path.join(self.base_dir, 'assets')
        
        self.backgrounds_dir = os.path.join(self.assets_dir, 'backgrounds')
        self.characters_dir = os.path.join(self.assets_dir, 'characters')
        self.items_dir = os.path.join(self.assets_dir, 'items')
        
        self.default_background = os.path.join(self.backgrounds_dir, 'default_background.png')


        # Load initial game state
        self.background = self.default_background
        self.characters = []
        #self.inventory = self.inventory_db.load_inventory()

    def start_game(self):
        # Display initial game UI/setup
        self.ui.display_stage(self.background, self.characters)
        self.process_turn()

    def process_turn(self):
    # Instead of looping here, process the received input once, update the game state, and wait for the next event
        # llm_response = self.llm_interaction.process_input(user_input)

        # self.update_game_state(llm_response)
        # self.ui.update_ui(self.background, self.characters)
        # self.handle_inventory_changes(llm_response)
        pass


    