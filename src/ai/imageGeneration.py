import json
from urllib import request, parse
import random

import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


def queuePrompt(prompt):
    workflow = json.load(open('workflow_api.json'))

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

def generateImage(prompt):
    queuePrompt(prompt)

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



prompt = "man"
generateImage(prompt)