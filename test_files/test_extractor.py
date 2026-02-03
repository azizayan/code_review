import extractor

# A sample script with messy formatting to test the AI's flexibility
sample_code = """
import torch.nn as nn
import torch.optim as optim

# The AI should find these even if they are scattered
learning_rate = 1e-4 
BATCH_SIZE = 64

class SimpleNet(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1 = nn.Linear(10, 1)

def train():
    model = SimpleNet()
    # It should identify 'Adam' from this line
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    # It should identify 'MSELoss'
    criterion = nn.MSELoss()
    
    epochs = 15
    for epoch in range(epochs):
        pass
"""

print(" Sending code to local AI (Mistral)...")
facts = extractor.extract_ml_facts(sample_code)

print("\n---Extracted Facts ---")
print(facts)

# Verification Logic
if facts.get('optimizer') == 'Adam' and facts.get('epochs') == 15:
    print("\n✅ SUCCESS: AI correctly identified parameters.")
else:
    print("\n❌ FAILURE: AI missed some parameters.")