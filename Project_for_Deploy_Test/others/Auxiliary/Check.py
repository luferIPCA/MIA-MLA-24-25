#lufer
#check if X_test.csv is present

import os
import pandas as pd

# Define file path
X_test_path = os.path.join("model", "X_test.csv")

# Debugging: Print path
print(f"Loading X_test from: {X_test_path}")

# Check if the file exists
if not os.path.exists(X_test_path):
    raise FileNotFoundError(f"X_test.csv not found at {X_test_path}")

# Load dataset
X_test = pd.read_csv(X_test_path)

# Debugging: Print first rows
print("X_test loaded successfully!")
print(X_test.head())  # Print a sample to verify contents
