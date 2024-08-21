import tkinter as tk
from src.gameEngine import GameEngine

def main():
    # Create the root window for Tkinter
    root = tk.Tk()
    root.title("Myth Maker")
    root.geometry("1920x1080")  # Example window size, adjust as needed
    
    # Initialize the GameEngine with Tkinter root as master
    game_engine = GameEngine(master=root)
    game_engine.ui.startGame()

    # Start the Tkinter main loop
    root.mainloop()

if __name__ == "__main__":
    main()