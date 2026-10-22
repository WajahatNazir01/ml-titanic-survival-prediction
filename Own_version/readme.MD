# Titanic Passenger Survival Prediction System

A machine learning web app that predicts whether a Titanic passenger would have survived, based on four details. Built for AIC354 Machine Learning Fundamentals (Assignment 2, Task 1) at COMSATS University Islamabad, Lahore Campus.

**Live demo:** https://ml-titanic-survival-prediction-by-wajahat.streamlit.app/

## Dataset
- Full Titanic dataset, 891 passengers (889 after dropping 2 rows with a missing port)
- Source: seaborn's copy of the Kaggle Titanic data
- Target: `Survived` (0 = no, 1 = yes), about 38% survived

## Input features
| Feature | Meaning | Values |
|---|---|---|
| `PClass` | Ticket class | First, Second, Third |
| `Gender` | Passenger gender | Male, Female |
| `Sibling` | Siblings or spouses aboard | Zero, One, Two, Three or more |
| `Embarked` | Port of embarkation | Southampton, Cherbourg, Queenstown |

## Project steps
1. Data collection
2. Data understanding (missing values, survival rate by sex and class)
3. Preprocessing (4 columns kept, missing rows dropped, readable categories)
4. Label encoding (inside the model pipeline)
5. Model selection and training (SVC, Logistic Regression, Decision Tree)
6. Evaluation (accuracy, classification report, confusion matrix)
7. Deployment on Streamlit Community Cloud

## Files
- `titanic_survival_prediction.ipynb`: full notebook
- `app.py`: Streamlit web app (boarding-pass design)
- `titanic_model.pkl`: trained SVC pipeline (created by the notebook)
- `titanic.csv`: dataset
- `requirements.txt`: dependencies (scikit-learn pinned to match the saved model)
- `.streamlit/config.toml`: light theme settings

## Run locally
```bash
python -m venv venv
venv\Scripts\activate        # Mac/Linux: source venv/bin/activate
pip install -r requirements.txt
pip install jupyter ipykernel
```
1. Run the notebook top to bottom to create `titanic_model.pkl`.
2. Start the app: `streamlit run app.py`

## Results
| Model | Test accuracy |
|---|---|
| SVC (deployed) | 0.84 |
| Logistic Regression | 0.83 |
| Decision Tree | 0.85 |

_Update these with your own run if the numbers differ._

## Limitations
- Only four features are used. Age and fare would likely improve accuracy.
- The model learns patterns in this dataset only, not a historical analysis.

