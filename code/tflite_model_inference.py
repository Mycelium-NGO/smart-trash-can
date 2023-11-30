import numpy as np
import tensorflow as tf
from PIL import Image
from tensorflow.keras.applications.mobilenet import preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array, load_img

# Define the class names
class_names = ['Aluminum Can', 'Glass', 'HDPE', 'PET']

# Load TFLite model and allocate tensors
interpreter = tf.lite.Interpreter(model_path="trash_model_v1.tflite")
interpreter.allocate_tensors()

# Get input and output details
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def load_and_preprocess_image(image_path, target_size=(224, 224)):
    # Load the image
    img = load_img(image_path, target_size=target_size)

    # Convert the image to a numpy array
    img_array = img_to_array(img)

    # Expand dimensions to match the model's input format
    img_array = np.expand_dims(img_array, axis=0)

    # Preprocess the image
    img_array = preprocess_input(img_array)

    return img_array

# Function to run inference
def run_inference(image_path):
    # Preprocess the image
    input_data = load_and_preprocess_image(image_path, 
                                  (input_details[0]['shape'][1], input_details[0]['shape'][2]))

    # Set the tensor to point to the input data to be inferred
    interpreter.set_tensor(input_details[0]['index'], input_data)

    # Run the inference
    interpreter.invoke()

    # Extract the output data
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

# Example usage
image_path = "plastic_bottles/testing/1662500498.5266643.jpg"
prediction = run_inference(image_path)

# Assuming a classification model, find the class with the highest probability
predicted_class_index = np.argmax(prediction)
predicted_class_label = class_names[predicted_class_index]
print("Predicted class:", predicted_class_label)
