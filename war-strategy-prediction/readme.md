# War Strategy Prediction System

## Overview

This project is a **machine learning based war strategy prediction system** that analyzes battlefield parameters and predicts the **most suitable military strategy** along with a **success probability score**.

The system uses multiple trained machine learning models to analyze historical battle data and recommend strategies based on input features such as:

- terrain
- enemy strength
- weather conditions
- troop size
- military resources

The project demonstrates how **machine learning can assist decision making in strategic simulations**.

---

## System Pipeline

Battlefield Inputs → Feature Encoding → Machine Learning Models → Strategy Prediction → Success Score

1. Battlefield parameters are entered through the dashboard.
2. Input features are encoded using trained label encoders.
3. Multiple ML models analyze the input.
4. The system predicts the most suitable war strategy.
5. A success probability score is generated.

---

## Features

- War strategy prediction using machine learning
- Multiple ML models trained for comparison
- Strategy recommendation based on battlefield conditions
- Success probability estimation
- Simple web dashboard interface
- Pre-trained models included

---

## Project Structure

```
war-strategy-prediction
│
├── app.py
├── training.py
│
├── battle_data.csv
├── combined_dataset.csv
│
├── military_random_forest_model.pkl
├── military_gradient_boosting_model.pkl
├── military_extra_trees_model.pkl
├── military_ridge_regression_model.pkl
│
├── military_label_encoders.pkl
│
├── strategies.txt
├── success_score.txt
├── model_accuracy.txt
│
├── col_defination.txt
├── reference.txt
│
├── templates
│   └── dashboard.html
│
└── README.md
```

---

## Important Files

### app.py

Main application file that runs the **web dashboard**.

Responsibilities:

- Loads trained machine learning models
- Loads label encoders
- Accepts battlefield inputs from the user
- Runs predictions
- Displays predicted strategy and success score

---

### training.py

Used for **training the machine learning models**.

This script:

- loads battlefield datasets
- preprocesses the data
- encodes categorical variables
- trains multiple ML models
- saves trained models as `.pkl` files

---

### battle_data.csv

Dataset containing **battlefield scenarios and outcomes** used for training the models.

---

### combined_dataset.csv

Expanded dataset containing **merged battlefield data** used for improving model accuracy.

---

### military_random_forest_model.pkl  
### military_gradient_boosting_model.pkl  
### military_extra_trees_model.pkl  
### military_ridge_regression_model.pkl  

These are **trained machine learning models** used by the system to make predictions.

Each model uses a different algorithm to analyze battlefield data.

---

### military_label_encoders.pkl

Stores the **trained label encoders** used to convert categorical battlefield inputs into numeric values required by machine learning models.

---

### strategies.txt

Contains the list of **possible military strategies** that the model can recommend.

Examples may include:

- defensive strategy
- offensive strategy
- guerrilla warfare
- ambush tactics

---

### success_score.txt

Stores information about **predicted success probabilities** for strategies.

---

### model_accuracy.txt

Contains the **accuracy scores of the trained models** for evaluation.

---

### col_defination.txt

Explains the meaning of dataset columns used during training.

---

### reference.txt

Contains references and notes related to battlefield strategy logic and dataset preparation.

---

### templates/dashboard.html

Frontend interface of the project.

This file creates the **web dashboard where users input battlefield conditions and view predictions**.

---

## Installation

Clone the repository

```
git clone https://github.com/ATULAggarwal7/ai-projects-portfolio
```

Move into the project directory

```
cd war-strategy-prediction
```

Install dependencies

```
pip install flask pandas scikit-learn numpy
```

---

## Run the Project

```
python app.py
```

After running the command, open your browser and go to:

```
http://localhost:5000
```

You will see the **War Strategy Prediction Dashboard** where you can enter battlefield parameters.

---

## Technologies Used

- Python
- Flask
- Scikit-learn
- Pandas
- NumPy
- HTML

---

## Applications

- Military strategy simulations
- Decision support systems
- Defense research simulations
- Educational machine learning projects
- Strategy modeling experiments

---

## Future Improvements

Possible improvements for the project:

- Add more battlefield parameters
- Improve model accuracy with larger datasets
- Add interactive battlefield visualization
- Integrate reinforcement learning for strategy planning
- Add real-time simulation environment

---

## Author

Atul Aggarwal