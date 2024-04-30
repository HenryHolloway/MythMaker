import json
from urllib import request, parse
import random

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def queuePrompt(prompt, workflow_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))  # Gets the directory of the current script
    workflow_path = os.path.join(dir_path, workflow_name)  # Joins the directory path with the workflow filename
    workflow = json.load(open(workflow_path))
    
    workflow["6"]["inputs"]["text"] = prompt

    prompt = workflow

    p = {"prompt": prompt}
    data = json.dumps(p).encode('utf-8')
    req =  request.Request("http://127.0.0.1:8188/prompt", data=data)
    request.urlopen(req)


class NewImageHandler(FileSystemEventHandler):
    def __init__(self, file_extension='.png', start_time=0):
        self.latest_file = None
        self.file_extension = file_extension
        self.start_time = start_time

    def on_created(self, event):
        # If a file is created in the directory, check if it's a new image file
        if event.is_directory:
            return
        if time.time() > self.start_time and event.src_path.endswith(self.file_extension):
            self.latest_file = event.src_path
            return True

def generateImage(prompt, workflow_name):
    queuePrompt(prompt, workflow_name)

    output_dir = os.path.expanduser('~/ComfyUI/output')
    start_time = time.time()

    # Set up the event handler and observer
    event_handler = NewImageHandler(start_time=start_time)
    observer = Observer()
    observer.schedule(event_handler, output_dir, recursive=False)
    observer.start()

    try:
        print("Waiting for the new image to be generated...")
        while event_handler.latest_file is None:
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()

    if event_handler.latest_file:
        print("New image generated:", event_handler.latest_file)
        return event_handler.latest_file
    else:
        print("No new image detected.")
        return None



# TO DO: 
# flow for processing character images: i.e. prompt with a white bakcground and then automate to key it out so that we have a character image on a transparent background

def generateCharacterImage(prompt):
    workflow = "character_workflow_api.json"
    
    path = generateImage("(white background 1.25)" + prompt, workflow)

    # Generate a new filename based on the prompt, with spaces removed
    new_filename = "ch_" + prompt.replace(" ", "") + ".png"

    # Calculate the absolute path to the 'assets/characters' directory relative to the current file
    final_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'characters', new_filename)
    os.rename(path, final_path)

    # Normalize the path to resolve any '..'
    normalized_path = os.path.normpath(final_path)
    # Find the index of the project root directory name in the path
    project_root_name = "MythMaker"
    root_index = normalized_path.find(project_root_name)
    if root_index != -1:
        # Strip everything before the project root directory name
        relative_path = normalized_path[root_index:]
        return relative_path
    else:
        # If the project root name is not found in the path, return the normalized path
        return normalized_path

def generateBackgroundImage(prompt):
    workflow = "background_workflow_api.json"
    
    preprompt = "(8k masterpiece surreal cel shaded background art 1.25)"

    fullprompt = preprompt + prompt

    path = generateImage(fullprompt, workflow)

    # Generate a new filename based on the prompt, with spaces removed
    new_filename = "bg_" + prompt.replace(" ", "")[:20] + ".png"
    # Calculate the absolute path to the 'assets/backgrounds' directory relative to the current file
    final_path = os.path.join(os.path.dirname(__file__), '..', '..', 'assets', 'backgrounds', new_filename)
    os.rename(path, final_path)

    # Normalize the path to resolve any '..'
    normalized_path = os.path.normpath(final_path)
    # Find the index of the project root directory name in the path
    project_root_name = "MythMaker"
    root_index = normalized_path.find(project_root_name)
    if root_index != -1:
        # Strip everything before the project root directory name
        relative_path = normalized_path[root_index:]
        return relative_path
    else:
        # If the project root name is not found in the path, return the normalized path
        return normalized_path




if __name__ == "__main__":
    test_character = generateCharacterImage("(hypperreal 8k anime) elf with  and long brown hair")
    print("Generated character image path:", test_character)

