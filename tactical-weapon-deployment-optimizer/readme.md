# Tactical Weapon Deployment Optimizer

## Overview

This project simulates a **tactical decision support system** that determines the **best deployment position for weapons against enemy targets** using geographic coordinates and weapon capabilities.

The system analyzes:

- Friendly unit position
- Enemy target locations
- Weapon ranges and constraints
- Tactical safety rules

Based on this information, the optimizer generates **multiple possible deployment positions**, evaluates their effectiveness, and selects the **most optimal position for weapon deployment**.

This project demonstrates concepts such as **geospatial calculations, tactical scoring, and rule-based optimization using Python**.

---

## System Pipeline

Friendly Position + Enemy Positions → Weapon Recommendation → Candidate Deployment Positions → Tactical Evaluation → Best Deployment Location

1. Friendly unit location is provided.
2. Enemy target coordinates are entered.
3. The system analyzes enemy distribution.
4. Suitable weapons are recommended.
5. Multiple deployment positions are generated.
6. Each position is evaluated based on weapon range and potential damage.
7. The best tactical deployment location is selected.

---

## Features

- Tactical weapon placement optimization
- Automatic weapon recommendation
- Geographic distance calculations using coordinates
- Grid-based candidate position generation
- Tactical scoring system for evaluating positions
- Output results saved for analysis

---

## Project Structure

```
tactical-weapon-deployment-optimizer
│
├── main.py
├── config.py
├── weapon_recommender.py
│
├── weapons
│   └── weapons_data.py
│
├── utils
│   ├── geoutils.py
│   └── mathutils.py
│
├── data
│   └── output
│       └── smart_position_1.txt
│
└── README.md
```

---

## Important Files

### main.py

Entry point of the project.

Responsibilities:

- Takes friendly and enemy coordinates as input
- Calls the weapon recommender
- Generates candidate deployment positions
- Evaluates tactical effectiveness
- Displays and saves the best deployment location

---

### config.py

Contains configuration values used throughout the system such as:

- grid resolution
- search radius
- output directory

These parameters control how many deployment positions are tested.

---

### weapon_recommender.py

Handles the **weapon selection logic**.

It analyzes enemy targets and determines which weapons are most suitable based on:

- range
- target type
- tactical direction

---

### weapons/weapons_data.py

Acts as the **weapon database** for the system.

Each weapon entry contains information such as:

- weapon type
- minimum firing range
- maximum firing range
- mobility
- lethality

This data is used when evaluating candidate positions.

---

### utils/geoutils.py

Contains **geographic utility functions** used by the system.

Tasks handled here include:

- calculating distance between coordinates
- generating candidate deployment grids
- computing compass directions
- generating forward tactical positions

---

### utils/mathutils.py

Contains the **tactical scoring logic**.

This module evaluates how effective a candidate position is based on:

- distance to enemy targets
- weapon lethality
- safety constraints
- total expected damage

The position with the highest score becomes the recommended deployment location.

---

### data/output

This folder stores the **generated results**.

Example output file:

```
smart_position_1.txt
```

This file may contain:

- selected deployment coordinates
- recommended weapon
- tactical direction
- damage score

---

## Installation

Clone the repository

```
git clone https://github.com/ATULAggarwal7/ai-projects-portfolio
```

Move to the project directory

```
cd tactical-weapon-deployment-optimizer
```

Install dependencies

```
pip install numpy
```

---

## Run the Project

```
python main.py
```

The system will:

1. Ask for friendly position coordinates
2. Ask for enemy target coordinates
3. Recommend suitable weapons
4. Generate optimal deployment positions
5. Save results in the output folder

---

## Technologies Used

- Python
- NumPy
- Geospatial calculations
- Rule-based decision system

---

## Applications

- Tactical battlefield simulations
- Military planning research
- Geospatial optimization studies
- Defense strategy modeling
- Educational projects in optimization and decision systems

---

## Future Improvements

Possible upgrades:

- Interactive map visualization
- Heatmap for best deployment locations
- Terrain analysis integration
- Machine learning based weapon selection
- Real-time battlefield simulation

---

## Author

Atul Aggarwal