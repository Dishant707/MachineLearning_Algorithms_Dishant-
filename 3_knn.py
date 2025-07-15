# Import required libraries
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import numpy as np

# Load the Digits dataset
data = load_digits()
X = data.data  # Features: 8x8 pixel intensities
y = data.target  # Target: digit (0-9)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the KNN model
model = KNeighborsClassifier(n_neighbors=5)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)

# Output results
print("K-Nearest Neighbors on Digits Dataset")
print(f"Accuracy: {accuracy:.4f}")
print("\nSample Predictions (first 5 test samples):")
for i in range(5):
    print(f"Predicted: {y_pred[i]}, Actual: {y_test[i]}")
# Expected output:
# Accuracy: ~0.98-0.99
# Sample Predictions: Predicted vs. actual digits for first 5 test samples