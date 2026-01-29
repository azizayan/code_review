from analyzer import parse_code
import os

# 1. Create a dummy Python file to test
# We include: normal imports, aliased imports, 'from' imports, and functions (with/without docstrings)
dummy_code = """
import numpy as np
import pandas
from sklearn.model_selection import train_test_split

def load_data():
    '''Loads the dataset from CSV.'''
    return [1, 2, 3]

def train_model(data):
    # This function has NO docstring
    pass
"""

filename = "temp_dummy_script.py"

# Write the file to disk
with open(filename, "w") as f:
    f.write(dummy_code)

try:
    # 2. Run your analyzer
    print(f"🔍 Analyzing {filename}...\n")
    stats = parse_code(filename)

    # 3. Print the results nicely
    print("--- 📦 IMPORTS FOUND ---")
    for imp in stats["imports"]:
        alias_str = f" (aliased as '{imp.alias}')" if imp.alias else ""
        print(f"Line {imp.lineno}: {imp.module}{alias_str}")

    print("\n--- ⚡ FUNCTIONS FOUND ---")
    for func in stats["functions"]:
        status = "✅ Has Docstring" if func.docstring else "❌ No Docstring"
        print(f"Line {func.lineno}: {func.name} -> {status}")

finally:
    # Cleanup: remove the dummy file
    if os.path.exists(filename):
        os.remove(filename)