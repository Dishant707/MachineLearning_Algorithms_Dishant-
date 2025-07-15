# Import required libraries
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Load the Breast Cancer dataset
data = load_breast_cancer()
X = data.data  # Features: tumor measurements (radius, texture, etc.)
y = data.target  # Target: 0 (malignant), 1 (benign)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the SVM model
model = SVC(kernel='linear')
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=data.target_names)

# Output results
print("Support Vector Machine on Breast Cancer Dataset")
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(report)
# Expected output:
# Accuracy: ~0.95-0.97
# Classification Report: precision, recall, f1-score for malignant and benign classes