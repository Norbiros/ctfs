import pickle

with open('heavyweight_model.pth', 'rb') as f:
    model = pickle.load(f)
    print(model)

# Use the model as needed
