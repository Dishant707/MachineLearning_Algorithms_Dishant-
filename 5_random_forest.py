# Import required libraries
from sklearn.datasets import load_wine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import numpy as np

# Load the Wine dataset
data = load_wine()
X = data.data  # Features: chemical properties of wine
y = data.target  # Target: wine class (0, 1, 2)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Random Forest model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)

# Output feature importances
feature_importances = model.feature_importances_
feature_names = data.feature_names

# Output results
print("Random Forest on Wine Dataset")
print(f"Accuracy: {accuracy:.4f}")
print("\nFeature Importances:")
for name, importance in zip(feature_names, feature_importances):
    print(f"{name}: {importance:.4f}")
# Expected output:
# Accuracy: ~0.97-1.00
# Feature Importances: importance scores for each feature (e.g., alcohol, malic_acid)