<div align="center">
<img alt="The Myth Maker" src="https://github.com/HenryHolloway/MythMaker/blob/main/assets/TheMythMaker.png" width="200">
</div>

## Myth Maker
### A guided framework for LLM text adventures.

Please note that this project is still work in progress.

## Roadmap

### Stage 1: Foundation and Backend Setup
- [ ] **Ollama Backend** - Setting up the core backend services.
- [ ] **Prompt Engineering** - Developing the logic for:
  - [ ] Dice rolls
  - [ ] Inventory management
  - [ ] Character management
  - [ ] Location Management
- [ ] **ComfyUI Backend** - Implementing a user-friendly interface backend.
- [ ] **Character & Location Imagery** - Prompt engineering for generating images of characters & locations.
- [ ] **Transparency Logic** - Backend logic to turn the character background transparent.
- [ ] **Adventure Logging** - Structured logging of adventures for future reference.

### Stage 2: Enhancement and Fine-tuning
- [ ] **Data Pruning/Annotation** - Cleaning and annotating data for better model training.
- [ ] **Model Training** - Train LoRA or QLoRA models for improved performance.
- [ ] **Full Fine-tune** - Full model fine-tuning (if needed).
- [ ] **GBNF Grammar Implementation** - Implement new model using GBNF grammar to replicate the adventure logs more accurately.
  - [ ] This step involves redoing the game flow to eliminate prior prompt engineering, allowing the fine-tuned model to handle the logic.