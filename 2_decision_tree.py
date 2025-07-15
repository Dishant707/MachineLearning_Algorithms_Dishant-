# Import required libraries
from sklearn.datasets import fetch_openml
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, confusion_matrix
import pandas as pd

# Load the Titanic dataset
data = fetch_openml(name='titanic', version=1, as_frame=True)
df = data.frame

# Select features and handle missing values
features = ['pclass', 'age', 'sex']
X = df[features].copy()
X['age'].fillna(X['age'].mean(), inplace=True)  # Fill missing age with mean
X['sex'] = X['sex'].map({'male': 0, 'female': 1})  # Encode sex as binary
y = df['survived'].astype(int)  # Target: survival (0 or 1)

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize and train the Decision Tree model
model = DecisionTreeClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
conf_matrix = confusion_matrix(y_test, y_pred)

# Output results
print("Decision Tree on Titanic Dataset")
print(f"Accuracy: {accuracy:.4f}")
print("\nConfusion Matrix:")
print(conf_matrix)
# Expected output:
# Accuracy: ~0.78-0.82
# Confusion Matrix: 2x2 matrix showing true negatives, false positives, false negatives, true positives