import pandas as pd
from sklearn.linear_model import LogisticRegression

# No docstring here
def load_and_train():
    data = pd.read_csv("C:/Users/Admin/data.csv") # Hardcoded path
    model = LogisticRegression() # No random_state
    model.fit(data, data) # No splitting!

if __name__ == "__main__":
    load_and_train()