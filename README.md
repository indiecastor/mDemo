# mDemo — population models demo for students
This is a study project for populational models. This program includes:
malthusian model, logistic model, predator-prey & competitive Lotka-Volterra models.

# Installation
```bash
git clone https://github.com/indiecastor/mdemo.git
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

# Requirements
- DearPyGUI - 2.0.0
- NumPy     - 2.2.6
- SciPy     - 1.15.2

# Structure
project_root/
├── main.py              # Entry point and main window interface
├── constants.py         # Min/max values for model parameters
│
├── models/
│   ├── malt.py          # Malthusian model and interface
│   ├── log.py           # Logistic model and interface
│   ├── pplv.py          # Predator–prey Lotka–Volterra model
│   └── complv.py        # Competitive Lotka–Volterra model
│
├── gui/
│   ├── fonts/
│   │   └── JetBrainsMono/   # Font family
│   │
│   ├── indents.py       # UI spacing and indents
│   └── texts.py         # Raw texts and formatting tag lists
│
└── README.md            # (optional) Project description

# Contacts
*Vadim Tarasov*  
*Kazan Federal University*  
VaITarasov@stud.kpfu.ru
