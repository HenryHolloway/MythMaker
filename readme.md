<div align="center">
<img alt="The Myth Maker" src="https://github.com/HenryHolloway/MythMaker/blob/main/assets/TheMythMaker.png" width="200">
</div>

## Myth Maker
### v0.0.5

Myth Maker is revolutionizing the world of text-based adventures by harnessing the power of Large Language Models (LLMs). We aim to replicate the tools found in tabletop RPG games to avoid bias and navigate complex game mechanics, such as dice rolls for determining outcomes, character card generation for creating diverse but consistent personas, inventory management for tracking players' items and preventing cheating or metagaming, and location dynamics that change based on player decisions.

## Installation

I am going to come back and refine this later, as this project likely isn't worth running yet, but if you're interested in checking out the status thus far, here's a rough guide of what you'll need to do:

- Have Ollama running on 127.0.0.1:11434, with an `openchat` model available
- Have ComfyUI running on 127.0.0.1:8188, with outputs going to ~/ComfyUI/output
- Clone this repository
- Install python requirements (...TO DO: create requirements.txt)
- run `python3 -m src.main` from the MythMaker Directory

## Roadmap

### Stage 1: Foundation and Backend Setup
- 🟩🟩🟩🟩🟩🟩 **Ollama Backend** - Setting up the core backend services.
- 🟩🟩🟨🟨⬜⬜ **Prompt Engineering** - Developing the logic for:
  - 🟩🟩🟩🟩🟩🟩 Dice rolls 
  - 🟩🟩🟩🟩🟨⬜ Inventory management
  - ⬜⬜⬜⬜⬜⬜ Character management
  - ⬜⬜⬜⬜⬜⬜ Location Management
- 🟩🟩🟩🟩🟩🟩 **ComfyUI Backend** - Implementing a user-friendly interface backend.
- ⬜⬜⬜⬜⬜⬜ **Character & Location Imagery** - Prompt engineering for generating images of characters & locations. 
  - ⬜⬜⬜⬜⬜⬜ **Transparency Logic** - Backend logic to turn the character background transparent.
- ⬜⬜⬜⬜⬜⬜ **TTS Backend** - Backend logic for elegant sounding text-to-speech
- ⬜⬜⬜⬜⬜⬜ **TTS Frontend** - UI and frontend logic
- ⬜⬜⬜⬜⬜⬜ **Frontend Settings & UI Changes** - User preferences and backend tweaks
- 🟩🟩⬜⬜⬜⬜ **Adventure Logging** - Structured logging of adventures for future reference.
- 🟩⬜⬜⬜⬜⬜ **Modelfile** - Ollama modelfile for task(s)

### Stage 2: Enhancement and Fine-tuning
- ⬜⬜⬜⬜⬜⬜ **Data Pruning/Annotation** - Cleaning and annotating data for better model training.
- ⬜⬜⬜⬜⬜⬜ **Model Training** - Train LoRA or QLoRA models for improved performance.
- ⬜⬜⬜⬜⬜⬜ **Full Fine-tune** - Full model fine-tuning (if needed).
- ⬜⬜⬜⬜⬜⬜ **GBNF Grammar Implementation** - Implement new model using GBNF grammar to replicate the adventure logs 'in place', passing between the user, system, and model.