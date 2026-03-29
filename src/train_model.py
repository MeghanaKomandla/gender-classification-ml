import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

# Load dataset
df = pd.read_csv("../dataset/gender_data.csv", on_bad_lines='skip')

# Encode gender
label_encoder = LabelEncoder()
df["gender"] = label_encoder.fit_transform(df["gender"])

# Features and labels
X = df.drop(columns=["gender"])
y = df["gender"]

# Train test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Scale features
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Define models and parameter grids
model_params = {
    "Random Forest": {
        "model": RandomForestClassifier(random_state=42),
        "params": {
            "n_estimators": [50, 100, 150]
        }
    },
    "Gradient Boosting": {
        "model": GradientBoostingClassifier(random_state=42),
        "params": {
            "n_estimators": [50, 100, 150],
            "learning_rate": [0.01, 0.1, 0.2]
        }
    },
    "SVM": {
        "model": SVC(),
        "params": {
            "kernel": ["linear", "rbf"],
            "C": [0.1, 1, 10]
        }
    }
}

best_model = None
best_score = 0

# Train and tune each model
for name, mp in model_params.items():
    grid = GridSearchCV(mp["model"], mp["params"], cv=5)
    grid.fit(X_train, y_train)

    y_pred = grid.predict(X_test)
    acc = accuracy_score(y_test, y_pred)

    print(f"{name} Best Params: {grid.best_params_}")
    print(f"{name} Accuracy: {acc:.4f}\n")

    if acc > best_score:
        best_score = acc
        best_model = grid.best_estimator_

print("Best Model:", best_model)

# Final evaluation
y_final_pred = best_model.predict(X_test)

print(classification_report(y_test, y_final_pred))

# Confusion matrix
sns.heatmap(confusion_matrix(y_test, y_final_pred), annot=True, fmt="d")
plt.xlabel("Predicted")
plt.ylabel("Actual")
plt.title("Confusion Matrix")
plt.show()
