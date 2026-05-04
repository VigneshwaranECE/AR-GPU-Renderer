import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

# 🔥 Simple dataset (temperature → condition)
# 0 = GOOD, 1 = WARNING, 2 = CRITICAL
data = pd.DataFrame({
    "temperature": [30,35,40,45,50,55,60,65,70,75,80,85,90,95],
    "condition":   [0,0,0,0,0,1,1,1,1,2,2,2,2,2]
})

# Features and labels
X = data[["temperature"]]
y = data["condition"]

# Create model
model = RandomForestClassifier(n_estimators=100, random_state=42)

# Train
model.fit(X, y)

# Save model
joblib.dump(model, "gpu_model.pkl")

print("✅ Model trained and saved as gpu_model.pkl")