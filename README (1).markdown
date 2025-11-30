# 🌟 Machine Learning Algorithms Repository

Welcome to the **MachineLearning_Algorithms_YourName** repository! 🚀 This project showcases five powerful machine learning algorithms implemented in Python using scikit-learn's built-in datasets. Each script is meticulously crafted with clear comments, data loading, model training, prediction, and evaluation steps to help you understand and explore machine learning concepts.

---

## 📋 Project Overview

This repository contains five Python scripts, each implementing a different machine learning algorithm applied to a unique dataset. The scripts are designed for learning and demonstration purposes, with detailed comments explaining every step. Whether you're a beginner or an experienced data scientist, this repository offers a hands-on way to explore classification algorithms!

---

## 🛠️ Algorithms and Scripts

Below is a summary of the five scripts included in this repository, along with their respective algorithms, datasets, and expected outputs:

| **Script**                     | **Algorithm**                | **Dataset**             | **Description**                                                                 |
|--------------------------------|------------------------------|-------------------------|---------------------------------------------------------------------------------|
| `1_logistic_regression.py`     | Logistic Regression          | Iris                    | Classifies iris flowers into three species using sepal and petal measurements.   |
| `2_decision_tree.py`           | Decision Tree Classifier     | Titanic                 | Predicts passenger survival on the Titanic based on age, sex, and class.         |
| `3_knn.py`                     | K-Nearest Neighbors (KNN)    | Digits                  | Classifies handwritten digits (0-9) based on pixel intensities.                  |
| `4_svm.py`                     | Support Vector Machine (SVM) | Breast Cancer           | Classifies tumors as malignant or benign using tumor measurements.               |
| `5_random_forest.py`           | Random Forest Classifier     | Wine                    | Classifies wine types based on chemical properties.                              |

### Expected Outputs
- **Logistic Regression**: Accuracy (~0.97) and a classification report with precision, recall, and F1-scores for each iris species.
- **Decision Tree**: Accuracy (~0.78-0.82) and a confusion matrix showing true/false positives/negatives.
- **KNN**: Accuracy (~0.98) and sample predictions for the first five test digits.
- **SVM**: Accuracy (~0.95-0.97) and a classification report for malignant/benign classes.
- **Random Forest**: Accuracy (~0.97-1.00) and feature importance rankings for wine dataset features.

---

## 🚀 Getting Started

### Prerequisites
Ensure you have the following Python libraries installed:
```bash
pip install scikit-learn pandas numpy
```

### Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/username/MachineLearning_Algorithms_YourName
   cd MachineLearning_Algorithms_YourName
   ```

2. **Run a Script**:
   ```bash
   python 1_logistic_regression.py
   ```
   Replace with the desired script name (e.g., `2_decision_tree.py`).

### Running the Scripts
Each script is self-contained and uses scikit-learn's built-in datasets, so no external data files are needed. Run any script to see the model train, predict, and output evaluation metrics to the console.

---

## 📊 Sample Output
Here’s an example of what to expect when running `1_logistic_regression.py`:
```
Logistic Regression on Iris Dataset
Accuracy: 0.9667
Classification Report:
              precision    recall  f1-score   support
    setosa       1.00      1.00      1.00        10
versicolor       0.92      1.00      0.96        12
 virginica       1.00      0.88      0.93         8
accuracy                            0.97        30
macro avg       0.97      0.96      0.96        30
weighted avg    0.97      0.97      0.97        30
```

Similar outputs are generated for other scripts, including accuracy, confusion matrices, or feature importances, as described in each script’s comments.

---

## 💡 Why This Repository?
- **Educational**: Perfect for learning machine learning algorithms with clear, commented code.
- **Reproducible**: Uses standard scikit-learn datasets, ensuring anyone can run the scripts.
- **Practical**: Demonstrates real-world applications like medical diagnosis (SVM) and survival prediction (Decision Tree).

---

## 📝 Notes
- The scripts are designed for Python 3.7+ and require scikit-learn, pandas, and numpy.
- Outputs may vary slightly due to random train-test splits, but accuracy is typically above 0.8 for all models.
- For further exploration, try modifying hyperparameters (e.g., `n_neighbors` in KNN or `n_estimators` in Random Forest) to see their impact!

---

## 🔐 Email & Password Manager Agent

This repository also includes a secure **Email & Password Manager Agent** (`email_password_manager.py`) - a command-line tool for securely managing your email accounts and passwords.

### Features
- **Secure Encryption**: Uses Fernet (AES-128-CBC) symmetric encryption from the cryptography library
- **Master Password Protection**: Key derivation using PBKDF2 with 480,000 iterations
- **Quick Access Aliases**: Save credentials with short aliases like "twitter" or "grok email" for quick retrieval
- **CRUD Operations**: Add, view, update, and delete email/password entries
- **Search Functionality**: Search credentials by email, service, alias, or notes
- **Password Generator**: Generate secure random passwords with customizable length
- **Export Functionality**: Export credentials to JSON format

### Prerequisites
```bash
pip install cryptography
```

### Usage
```bash
python email_password_manager.py
```

### Quick Access with Aliases
You can save your email and password with a simple keyword or phrase (alias) for quick retrieval:
```
# When adding a credential, set an alias:
Email address: user@gmail.com
Service name: Gmail
Password: ********
Quick access alias: grok email

# Later, quickly retrieve it using the alias:
Select option 3 (Quick view by alias)
Alias: grok email
✓ Found credential for alias 'grok email'
```

### Example Session
```
Welcome to the Email & Password Manager Agent
=============================================
No existing vault found. Let's create a new one.
Please create a master password (min 8 characters).

✓ Vault unlocked successfully!

==================================================
       Email & Password Manager Agent
==================================================
1. Add new credential
2. View credential (by email)
3. Quick view by alias (e.g., 'twitter', 'grok email')
4. View all credentials
5. Update credential
6. Delete credential
7. Search credentials
8. Generate secure password
9. Export credentials
10. Exit
==================================================
```

### Security Notes
- All credentials are encrypted using AES-128-CBC (Fernet)
- Master password is never stored; only used to derive the encryption key
- Uses PBKDF2 with SHA-256 and 480,000 iterations for key derivation
- Salt is randomly generated and stored separately

---

## 🙌 Contributing
Feel free to fork this repository, experiment with the code, or suggest improvements via pull requests. Issues and feedback are welcome!

---

## 📬 Contact
For questions or suggestions, reach out via GitHub Issues or email at `your_email@example.com`.

*Happy coding and exploring machine learning! 🎉*