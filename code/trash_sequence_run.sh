#!/bin/bash

# Run tflite_model_inference.py and store its output in a temporary file
python tflite_model_inference.py > temp_output.txt

# Read the output into a variable
predicted_class_label=$(<temp_output.txt)

# Export the variable so it's available in the environment of second file
export predicted_class_label

# Run test2.py
python  pi_controlling_multiple_CNC_arduinos.py

# Cleanup: Remove the temporary file
rm temp_output.txt
