import zipfile
import pickle

# Path to your PTH file (which seems to contain zipped data)
pth_file_path = 'heavyweight_model.pth'

# Extract the .pkl file
with zipfile.ZipFile(pth_file_path, 'r') as zip_ref:
    print(zip_ref.co)
    zip_ref.extractall('extracted_data')

# Now, load the .pkl file
pkl_file_path = 'extracted_data/hidden_flag/data.pkl'

with open(pkl_file_path, 'rb') as f:
    data = pickle.load(f)
    print(data)  # Check the contents, potentially the flag
