import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk

class appUI:
    def __init__(self, master, input_callback):
        self.input_callback = input_callback
        self.master = master
        
        # Set the stage for image display
        self.stage_frame = tk.Frame(master, width=1920, height=304)
        self.stage_frame.pack_propagate(0)  # Prevent the frame from auto-resizing
        self.stage_frame.pack()
        
        # Placeholder for where images will be displayed
        self.stage_label = tk.Label(self.stage_frame)
        self.stage_label.pack(fill="both", expand=True)
        
        # Chat window for AI interaction
        self.chat_frame = tk.Frame(master, height=200)
        self.chat_frame.pack(fill="both", expand=True, side="top")  # Fill available space
        
        self.chat_window = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD)
        self.chat_window.pack(side="left", fill="both", expand=True)
        
        # Frame for user input and submit button
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(fill="x", side="bottom")
        
        self.user_input = tk.Entry(self.input_frame)  # Parent is now self.input_frame
        self.user_input.pack(side="left", fill="x", expand=True)
        
        self.submit_button = tk.Button(self.input_frame, text="Submit", command=self.trigger_send_message)
        self.submit_button.pack(side="right")
        
        self.user_input.bind("<Return>", self.send_message)
    
    def trigger_send_message(self):
        # This method will simulate pressing Enter or clicking the Submit button
        self.send_message(None)
        
    def send_message(self, event):
        user_text = self.user_input.get()
        if user_text.strip():  # Ensure we don't process empty strings
            self.chat_window.insert(tk.END, "You: " + user_text + "\n")
            
            # Use the callback to process the input through GameEngine
            if self.input_callback:
                self.input_callback(user_text)
            
            self.user_input.delete(0, tk.END)  # Ensure this happens after processing
        self.user_input.focus_set()  # Set focus back to the input field


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