import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import os
import threading
import asyncio

import src.ai.brain as brain

from src.ai.textToSpeech import tts

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
        self.chat_frame = tk.Frame(master, height=200, background="#303030", borderwidth=2, relief="solid")  # Very dark grey background for the frame
        self.chat_frame.pack(fill="both", expand=True, side="top")

        self.chat_window = tk.Text(self.chat_frame, wrap=tk.WORD, state=tk.DISABLED, background="#303030", font=("Helvetica", 12), borderwidth=0, highlightthickness=0)
        self.chat_window.pack(side="left", fill="both", expand=True, padx=(75, 75), pady=(15, 15))  # Adjusted padding

        # Scroll function
        self.chat_window.bind("<MouseWheel>", self.on_mousewheel)

        self.update_chat_display()

        # Frame for user input and submit button
        self.input_frame = tk.Frame(master, background="#303030")  # Dark background for the frame
        self.input_frame.pack(fill="x", side="bottom")

        self.user_input = tk.Entry(self.input_frame, font=("Helvetica", 12), insertbackground="white", fg="white", bg="#505050")  # Light text on dark background
        self.user_input.pack(side="left", fill="x", expand=True, ipady=4)  # Adjust ipady as needed for visual alignment

        self.reset_button = tk.Button(self.input_frame, text="♻️", command=reset, font=("Helvetica", 10), fg="white", bg="#707070", borderwidth=0, highlightthickness=0)
        self.reset_button.pack(side="right", padx=5)  # Add padding for aesthetic spacing

        self.submit_button = tk.Button(self.input_frame, text="↩️", command=self.send_message, font=("Helvetica", 10), fg="white", bg="#707070", borderwidth=0, highlightthickness=0)
        self.submit_button.pack(side="right")


        self.user_input.bind("<Return>", self.send_message)


    def on_mousewheel(self, event):
        self.chat_window.yview_scroll(int(-1*(event.delta/120)), "units")



    def send_message(self, event):
        user_text = self.user_input.get().strip()

        if user_text:
            print("User said: " + user_text)
            self.append_message("user", user_text, done=True)

            self.input_callback(self.conversation)  # self.input_callback should be bound to GameEngine.process_turn

            self.user_input.delete(0, tk.END)  # Clear input field after processing
        self.user_input.focus_set()  # Refocus on the input field
    

    def append_message_and_update(self, role, text, done=True):
        print("Appending message and updating conversation window.")
        def task():
            self.append_message(role, text, done)
        # This ensures that Tkinter's operations remain in the main thread
        self.master.after(0, task)


        if done:
            return True
        return False


    def append_message(self, role, text, done):
        if self.conversation:  # Check if conversation list is not empty
            last_message = self.conversation[-1]  # Get the last message
            # Check if the last message was from "assistant" and the current role is also "assistant"
            if last_message["role"] == "assistant" and role == "assistant":
                # Append the new text to the last message's content
                last_message["content"] +=  text  # Adding a space for readability
            else:
                # If last role was not "assistant" or the current role is not "assistant",
                # append the new message as a new entry
                if role == "assistant" and text.startswith(" "):
                    text = text[1:]

                self.conversation.append({"role": role, "content": text})
            
            
        else:
            # Remove the initial "6. " if it exists
            if role == "assistant":
                if text.startswith("6") and not self.conversation:
                    text = text[1:]
                elif text.startswith(".") and not self.conversation:
                    text = text[1:]
                elif text.startswith(" "):
                    text = text[1:]
                    self.conversation.append({"role": role, "content": text})
            else:
                self.conversation.append({"role": role, "content": text})


        self.update_chat_display(done)  # Update display after every new message


    def update_chat_display(self, done=False):
        self.chat_window.config(state=tk.NORMAL)  # Enable editing to update content
        self.chat_window.delete("1.0", tk.END)  # Clear existing content

        for i, msg in enumerate(self.conversation):
            tag_name = f"tag_{i}"
            if msg["role"] == "user":
                background_color = "#D3D3D3"  # Light Gray for user messages
                font_color = "#000000"  # Black font color for better readability
            elif msg["role"] == "assistant":
                background_color = "#A9A9A9"  # Medium Dark Grey for assistant messages
                font_color = "#000000"  # Black font color for better readability
            elif msg["role"] == "system":
                background_color = "#000000"  # Dark Grey for system messages
                font_color = "#8B0000"  # Blood Red font color for better readability
            self.chat_window.tag_configure(tag_name, background=background_color, foreground=font_color, lmargin1=20, lmargin2=20, rmargin=20, spacing1=25, spacing3=25, borderwidth=2, relief="solid", font=("Helvetica", 14))
            
            content = ""
            if msg["role"] != "user": 
                content += f"{msg['content']}\n"
            else:
                content += f"You: {msg['content']}\n"
            self.chat_window.insert(tk.END, content, tag_name)

            if msg["role"] == "assistant" and done:                
                # Create a TTS button (Label) with the background color
                tts_label = tk.Label(self.chat_window, text="🔊", bg=background_color, cursor="hand2")
                tts_label.bind("<Button-1>", lambda event, m=msg["content"]: self.do_tts(m))
                
                # Embed the label at the current end position
                self.chat_window.window_create(tk.END, window=tts_label)
                
                # Insert a newline for spacing after the TTS button
                self.chat_window.insert(tk.END, "\n", tag_name)
                
        self.chat_window.config(state=tk.DISABLED)  # Disable editing after update
        self.chat_window.yview_moveto(1.0)  # Scroll to the bottom

    def do_tts(self, msg):
        tts_thread = threading.Thread(target=tts, args=(msg,))
        tts_thread.start()

    def display_stage(self, background_image_path, character_images=[]):
        self.stage_frame.after(100, self.load_and_display_background, background_image_path, character_images)

    def load_and_display_background(self, background_image_path, character_images):
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        relative_image_path = background_image_path.replace('MythMaker/assets/backgrounds/', '', 1)
        absolute_image_path = os.path.join(base_dir, 'assets', 'backgrounds', relative_image_path)

        try:
            bg_image = Image.open(absolute_image_path)
            # Ensure the frame has been rendered and has a valid size
            self.stage_frame.update_idletasks()  # Update the layout to ensure the sizes are current
            target_width = self.stage_frame.winfo_width()
            target_height = self.stage_frame.winfo_height()
            if target_width > 1 and target_height > 1:  # Check if dimensions are valid
                bg_image = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                bg_photo = ImageTk.PhotoImage(bg_image)
                self.stage_label.config(image=bg_photo)
                self.stage_label.image = bg_photo  # Keep a reference!
            else:
                print("Invalid dimensions for stage_frame:", target_width, target_height)
        except Exception as e:
            print(f"Failed to open or convert image due to: {e}.")
        
        for character_image_path in character_images:
            try:
                absolute_character_image_path = os.path.join(base_dir, character_image_path)
                char_image = Image.open(absolute_character_image_path)
                char_photo = ImageTk.PhotoImage(char_image)
                char_label = tk.Label(self.stage_label, image=char_photo, bg="white")
                char_label.photo = char_photo  # Keep a reference!
                char_label.pack()
            except Exception as e:
                print(f"Failed to load character image due to: {e}.")