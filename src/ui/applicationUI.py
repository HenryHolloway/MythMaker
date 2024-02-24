# gpt boilerplate, needs to be refactored & cleaned


import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

class appUI:
    def __init__(self, master, input_callback):
        self.input_callback = input_callback
        self.master = master
        master.title("Text Adventure Game")
        
        # Set the stage for image display
        self.stage_frame = tk.Frame(master, width=600, height=400)
        self.stage_frame.pack_propagate(0)  # To prevent the frame from resizing itself
        self.stage_frame.pack()
        
        # Placeholder for where images will be displayed
        self.stage_label = tk.Label(self.stage_frame)
        self.stage_label.pack(fill="both", expand=True)
        
        # Chat window for AI interaction below the stage
        self.chat_frame = tk.Frame(master, height=200)
        self.chat_frame.pack(fill="x", side="bottom")
        
        self.chat_window = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD)
        self.chat_window.pack(fill="both", expand=True)
        
        self.user_input = tk.Entry(master)
        self.user_input.pack(fill="x", side="bottom")
        self.user_input.bind("<Return>", self.send_message)
    
    def send_message(self, event):
        user_text = self.user_input.get()
        self.chat_window.insert(tk.END, "You: " + user_text + "\n")
        
        # Use the callback to process the input through GameEngine
        if self.input_callback:
            self.input_callback(user_text)
        
        self.user_input.delete(0, tk.END)

    def display_stage(self, background_image_path, character_images=[]):
        # Load and display the background image
        bg_image = Image.open(background_image_path)
        bg_photo = ImageTk.PhotoImage(bg_image)
        
        self.stage_label.config(image=bg_photo)
        self.stage_label.image = bg_photo  # Keep a reference!
        
        # Load and overlay character images (example for one, extend for more)
        for character_image_path in character_images:
            char_image = Image.open(character_image_path)
            char_photo = ImageTk.PhotoImage(char_image)
            
            # For simplicity, characters are also just shown in the stage_label;
            # you might want to fine-tune their positions
            char_label = tk.Label(self.stage_label, image=char_photo, bg="white")
            char_label.photo = char_photo  # Keep a reference!
            char_label.pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = TextAdventureApp(root)
    
    # Example to display a background and character images
    # Please ensure you have "background.png" and "character.png" files in your working directory
    app.display_stage("background.png", ["character1.png", "character2.png"])
    
    root.mainloop()