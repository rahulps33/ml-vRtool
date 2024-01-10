
import onnx
import tf2onnx
from tensorflow.keras.models import load_model

# Load the Keras model
loaded_keras_model = load_model(r"temp_data\model.h5")

# Convert the Keras model to ONNX format
onnx_model, _ = tf2onnx.convert.from_keras(loaded_keras_model)

# Save the ONNX model
onnx.save(onnx_model, r"temp_data\model.onnx")
