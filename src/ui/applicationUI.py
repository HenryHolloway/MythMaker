import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import json

class appUI:
    def __init__(self, master, input_callback, conversation):
        self.input_callback = input_callback
        self.master = master
        self.conversation = conversation  # Initialize conversation storage
        

        # Set the stage for image display
        self.stage_frame = tk.Frame(master, width=1920, height=304)
        self.stage_frame.pack_propagate(0)  # Prevent auto-resizing
        self.stage_frame.pack()

        # Placeholder for where images will be displayed
        self.stage_label = tk.Label(self.stage_frame)
        self.stage_label.pack(fill="both", expand=True)

        # Chat window for AI interaction
        self.chat_frame = tk.Frame(master, height=200)
        self.chat_frame.pack(fill="both", expand=True, side="top")

        self.chat_window = scrolledtext.ScrolledText(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED, background="#F5F5F5")
        self.chat_window.pack(side="left", fill="both", expand=True)
        self.update_chat_display()

        # Frame for user input and submit button
        self.input_frame = tk.Frame(master)
        self.input_frame.pack(fill="x", side="bottom")

        self.user_input = tk.Entry(self.input_frame)  # Parent is now self.input_frame
        self.user_input.pack(side="left", fill="x", expand=True)

        self.submit_button = tk.Button(self.input_frame, text="Submit", command=self.trigger_send_message)
        self.submit_button.pack(side="right")

        self.user_input.bind("<Return>", self.send_message)


    def trigger_send_message(self):
        self.send_message(None)


    def send_message(self, event):
        user_text = self.user_input.get().strip()
        if user_text:  # Process non-empty strings
            self.append_message("You", user_text, "#FFFFFF")
            # Directly trigger the processing, without reassigning self.conversation
            self.input_callback(self.conversation)  # self.input_callback should be bound to GameEngine.process_turn
            # Note: Consider how GameEngine.process_turn handles the conversation
            self.user_input.delete(0, tk.END)  # Clear input field after processing
        self.user_input.focus_set()  # Refocus on the input field
    
    def append_message_and_update(self, speaker, text, color):
        def task():
            self.append_message(speaker, text, color)
        # This ensures that Tkinter's operations remain in the main thread
        self.master.after(0, task)

    def append_message(self, speaker, text, bg_color):
        self.conversation.append({"speaker": speaker, "text": text, "color": bg_color})
        self.update_chat_display()  # Update display after every new message


    def update_chat_display(self):
        self.chat_window.config(state=tk.NORMAL)  # Enable editing to update content
        self.chat_window.delete("1.0", tk.END)  # Clear existing content

        for i, msg in enumerate(self.conversation):
            tag_name = f"tag_{i}"
            self.chat_window.tag_configure(tag_name, background=msg["color"], lmargin1=10, lmargin2=10, rmargin=10, spacing3=10)
            
            content = f"{msg['speaker']}: {msg['text']}\n\n"
            self.chat_window.insert(tk.END, content, tag_name)

        self.chat_window.config(state=tk.DISABLED)  # Disable editing after update


    def display_stage(self, background_image_path, character_images=[]):
        bg_image = Image.open(background_image_path)
        bg_photo = ImageTk.PhotoImage(bg_image)
        
        self.stage_label.config(image=bg_photo)
        self.stage_label.image = bg_photo  # Keep a reference!

        for character_image_path in character_images:
            char_image = Image.open(character_image_path)
            char_photo = ImageTk.PhotoImage(char_image)

            char_label = tk.Label(self.stage_label, image=char_photo, bg="white")
            char_label.photo = char_photo  # Keep a reference!
            char_label.pack()