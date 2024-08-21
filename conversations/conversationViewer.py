import tkinter as tk
from tkinter import filedialog, messagebox
import json

class ConversationReader:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversation Reader")
        self.root.geometry("600x400")

        self.text_area = tk.Text(self.root, wrap=tk.WORD)
        self.text_area.pack(expand=True, fill=tk.BOTH)

        self.load_button = tk.Button(self.root, text="Load Conversation", command=self.load_conversation)
        self.load_button.pack(pady=10)

    def load_conversation(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            try:
                with open(file_path, 'r') as file:
                    conversation_data = json.load(file)
                    self.display_conversation(conversation_data)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load file: {e}")

    def display_conversation(self, data):
        self.text_area.delete(1.0, tk.END)
        for message in data:
            role = message.get('role', 'Unknown')
            content = message.get('content', '')
            self.text_area.insert(tk.END, f"{role.capitalize()}:\n{content}\n\n")
            self.text_area.insert(tk.END, "-"*50 + "\n\n")

if __name__ == "__main__":
    root = tk.Tk()
    app = ConversationReader(root)
    root.mainloop()