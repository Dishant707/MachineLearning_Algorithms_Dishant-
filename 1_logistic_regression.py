# Import required libraries
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import numpy as np

# Load the Iris dataset
data = load_iris()
X = data.data  # Features: sepal length, sepal width, petal length, petal width
y = data.target  # Target: iris species (0, 1, 2)

# Split data into training and testing sets (80% train, 20% test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Logistic Regression model
model = LogisticRegression(multi_class='multinomial', max_iter=200)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=data.target_names)

# Output results
print("Logistic Regression on Iris Dataset")
print(f"Accuracy: {accuracy:.4f}")
print("\nClassification Report:")
print(report)
# Expected output:
# Accuracy: ~0.9667
# Classification Report with precision, recall, f1-score for each class (setosa, versicolor, virginica)