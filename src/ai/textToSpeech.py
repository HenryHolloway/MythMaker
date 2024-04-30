import subprocess
from playsound import playsound
import os

def tts(prompt):
    print("Initializing TTS process...")
    output_file = 'TTS.wav'

   
    temp_prompt_file = 'temp_prompt.txt'
    with open(temp_prompt_file, 'w') as temp_file:
        temp_file.write(prompt)
    
    # Prepare the command without using shell=True
    command = ["piper", "--model", "en_GB-alba-medium", "--output_file", output_file]

    # Open the temporary file for reading
    with open(temp_prompt_file, 'rb') as temp_file:
        # Execute the command, passing the file's contents to stdin
        subprocess.run(command, input=temp_file.read())

    # Cleanup the temporary file
    os.remove(temp_prompt_file)

    print(f"Speaking message: {prompt}")
    print(f"Subprocess executed with command: {' '.join(command)}")
    playsound(output_file)
    os.remove(output_file)
    print(f"Playback of {output_file} completed.")

if __name__ == "__main__":
    # Test the tts function with a sample prompt
    sample_prompt = "You find yourself in the bustling marketplace of the colorful city of Oasis, where merchants from far-and-wide have gathered to trade their wares."
    tts(sample_prompt)
