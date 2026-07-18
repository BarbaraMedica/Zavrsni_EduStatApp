import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    ConfusionMatrixDisplay
)

import joblib

# 1. GENERIRANJE PODATAKA - SIMULACIJA STUDENTSKE RUTINE
np.random.seed(42)
n = 1000

sleep_hours = np.random.normal(7, 1.5, n).clip(3, 10)
study_duration = np.random.normal(90, 30, n).clip(20, 240)
breaks = np.random.randint(0, 5, n)
time_of_day = np.random.randint(0, 24, n)

energy = (sleep_hours * 1.5 + np.random.normal(0, 1, n)).clip(1, 10)
stress = (10 - sleep_hours + study_duration / 60 + np.random.normal(0, 1, n)).clip(1, 10)

focus = (
    0.5 * energy
    - 0.4 * stress
    - 0.2 * (study_duration / 60)
    + 0.3 * breaks
    + np.random.normal(0, 1, n)
).clip(1, 10)

study_score = (
    0.4 * focus +
    0.3 * energy -
    0.3 * stress +
    0.2 * (sleep_hours / 8) -
    0.2 * (study_duration / 180)
)

noise = np.random.normal(0, 0.5, n)
label = ((study_score + noise) > 4.5).astype(int)

df = pd.DataFrame({
    "sleep_hours": sleep_hours,
    "study_duration": study_duration,
    "breaks": breaks,
    "time_of_day": time_of_day,
    "focus": focus,
    "stress": stress,
    "energy": energy,
    "good_time_to_study": label
})
print(df["good_time_to_study"].value_counts())

# 2. PRIPREMA PODATAKA - SPLIT NA TRAIN I TEST SET

X = df.drop("good_time_to_study", axis=1)
y = df["good_time_to_study"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42 #podjela na 20/80
)

# 3. LOGISTIČKA REGRESIJA - BASIC MODEL
lr_model = LogisticRegression(max_iter=1000)
lr_model.fit(X_train, y_train)

lr_pred = lr_model.predict(X_test)
lr_acc = accuracy_score(y_test, lr_pred)

# 4. RANDOM FOREST klasifikator

rf_model = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    random_state=42
)
rf_model.fit(X_train, y_train)

rf_pred = rf_model.predict(X_test)
rf_acc = accuracy_score(y_test, rf_pred)

# 5. USPOREDBA MODELA
print(f"Logistic Regression točnost: {lr_acc:.2f}")
print(f"Random Forest točnost: {rf_acc:.2f}")

print("\nEvaluacija Random Forest modela")

print(classification_report(y_test, rf_pred))

cm = confusion_matrix(y_test, rf_pred)

print("Confusion Matrix:")
print(cm)

disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()

plt.title("Confusion Matrix - Random Forest")
plt.savefig("model/confusion_matrix.png")
plt.close()
# 6. ODABIR NAJBOLJEG MODELA

if rf_acc > lr_acc:
    best_model = rf_model
    print("Odabran model: Random Forest")
else:
    best_model = lr_model
    print("Odabran model: Logistic Regression")

# 7. FEATURE IMPORTANCE

if isinstance(best_model, RandomForestClassifier):

    importances = best_model.feature_importances_

    feature_names = X.columns

    feat_df = pd.DataFrame({
        "feature": feature_names,
        "importance": importances
    }).sort_values(by="importance", ascending=False)

    print("\nVažnost varijabli:")
    print(feat_df)

    feat_df.to_csv("model/feature_importance.csv", index=False)

    plt.figure(figsize=(8,5))

    plt.bar(
        feat_df["feature"],
        feat_df["importance"]
    )

    plt.title("Važnost varijabli")
    plt.xlabel("Varijabla")
    plt.ylabel("Važnost")

    plt.xticks(rotation=45)

    plt.tight_layout()

    plt.savefig("model/feature_importance.png")

    plt.close()
#rezultat
results = pd.DataFrame({
    "Model": [
        "Logistic Regression",
        "Random Forest"
    ],
    "Accuracy": [
        lr_acc,
        rf_acc
    ]
})

results.to_csv(
    "model/model_results.csv",
    index=False
)

# 8. SPREMANJE

joblib.dump(best_model, "model/model.pkl")
df.to_csv("model/dataset.csv", index=False)

print("\nModel i dataset spremljeni.")