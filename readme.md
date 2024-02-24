# THIS IS VERY WIP! COME BACK LATER!


Aspirational Architecture:

```
text_adventure_game/
│
├── assets/
│   ├── backgrounds/
│   ├── characters/
│   └── items/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── game_engine.py
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── llm_interaction.py
│   │   ├── image_generation.py
│   │   └── inventory_management.py
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── character_db.py
│   │   └── inventory_db.py
│   │
│   └── ui/
│       ├── __init__.py
│       └── application_ui.py
│   
└── tests/
    ├── __init__.py
    └── test_cases_for_modules.py
```