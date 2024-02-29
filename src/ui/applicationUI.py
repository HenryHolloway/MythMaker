import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import json
import threading
import asyncio

import src.ai.brain as brain


class appUI:
    def __init__(self, master, input_callback, reset, conversation):
        self.input_callback = input_callback
        self.master = master
        self.conversation = conversation

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

        self.reset_button = tk.Button(master, text="Reset Game", command=reset)
        self.reset_button.pack(side="right")

        self.user_input.bind("<Return>", self.send_message)




    def trigger_send_message(self):
        self.send_message(None)


    def send_message(self, event):
        user_text = self.user_input.get().strip()

        if user_text:
            print("User said: " + user_text)
            self.append_message("user", user_text)

            self.input_callback(self.conversation)  # self.input_callback should be bound to GameEngine.process_turn

            self.user_input.delete(0, tk.END)  # Clear input field after processing
        self.user_input.focus_set()  # Refocus on the input field
    

    def append_message_and_update(self, speaker, text, done=True):
        print("Appending message and updating conversation window.")
        def task():
            self.append_message(speaker, text)
        # This ensures that Tkinter's operations remain in the main thread
        self.master.after(0, task)

        if done:
            return True
        return False


    def append_message(self, speaker, text):
        if self.conversation:  # Check if conversation list is not empty
            last_message = self.conversation[-1]  # Get the last message
            # Check if the last message was from "assistant" and the current speaker is also "assistant"
            if last_message["role"] == "assistant" and speaker == "assistant":
                # Append the new text to the last message's content
                last_message["content"] +=  text  # Adding a space for readability
            else:
                # If last speaker was not "assistant" or the current speaker is not "assistant",
                # append the new message as a new entry
                self.conversation.append({"role": speaker, "content": text})
        else:
            # If the conversation list is empty, just append the message
            self.conversation.append({"role": speaker, "content": text})
        
        self.update_chat_display()  # Update display after every new message


    def update_chat_display(self):
        self.chat_window.config(state=tk.NORMAL)  # Enable editing to update content
        self.chat_window.delete("1.0", tk.END)  # Clear existing content

        for i, msg in enumerate(self.conversation):
            tag_name = f"tag_{i}"
            if msg["role"] == "user":
                background_color = "#808080"
                font_color = "#FFFFFF"  # White font color for user messages
            elif msg["role"] == "assistant":
                background_color = "#EEEEEE"
                font_color = "#000000"  # Black font color for assistant messages
            elif msg["role"] == "system":
                background_color = "#000000"
                font_color = "#FFFFFF"  # White font color for system messages

            self.chat_window.tag_configure(tag_name, background=background_color, foreground=font_color, lmargin1=10, lmargin2=10, rmargin=10, spacing3=10)
            
            content = ""
            if msg["role"] != "user": 
                content += f"{msg['content']}\n\n"
            else:
                content += f"You: {msg['content']}\n\n"
            self.chat_window.insert(tk.END, content, tag_name)

        self.chat_window.config(state=tk.DISABLED)  # Disable editing after update
        self.chat_window.yview_moveto(1.0)  # Scroll to the bottom


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