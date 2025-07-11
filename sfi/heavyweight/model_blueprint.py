import torch
import torch.nn as nn
import streamlit as st
import numpy as np
from PIL import Image
import torchvision.transforms as transforms
from streamlit_drawable_canvas import st_canvas

# Define your model
class Heavyweight(nn.Module):
    def __init__(self):
        super(Heavyweight, self).__init__()
        self.features = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=8, kernel_size=8, bias=False),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            nn.Conv2d(in_channels=8, out_channels=32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2)
        )
        self.classifier = nn.Sequential(
            nn.Flatten(),
            nn.Linear(32 * 5 * 5, 128),
            nn.ReLU(),
            nn.Linear(128, 10)
        )

    def forward(self, x):
        x = self.features(x)
        x = self.classifier(x)
        return x

# Load your model (here just initializing)
model = Heavyweight()

# Streamlit setup
st.title("Digit Recognition Playground")
st.subheader("Draw a digit and get the prediction")

# Canvas for drawing digits
canvas = st_canvas(
    width=280,
    height=280,
    stroke_width=10,
    stroke_color="white",
    background_color="black"
)

if canvas.image_data is not None:
    # Convert drawn image to PIL format
    img = Image.fromarray(canvas.image_data.astype(np.uint8))

    # Preprocess image to fit the model input
    transform = transforms.Compose([
        transforms.Grayscale(num_output_channels=1),
        transforms.Resize((28, 28)),  # Resize to 28x28 as required by MNIST
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))
    ])

    input_tensor = transform(img).unsqueeze(0)  # Add batch dimension (1, 1, 28, 28)

    # Predict
    with torch.no_grad():
        output = model(input_tensor)
        predicted_class = torch.argmax(output, dim=1).item()

    # Display results
    st.image(img, caption="Your Drawing", use_column_width=True)
    st.write(f"Predicted Number: {predicted_class}")
