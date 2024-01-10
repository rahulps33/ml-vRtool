

# Function for solving neural network using Marabou solver
marabou_solver_r <- function(model, epsilon, image, correct_class) {
  
  # Save the Keras model to .h5 format
  model %>% save_model_hdf5("temp_data//model.h5")
  
  # Convert the model to ONNX format
  py_run_file("nn_solvers//convert_to_onnx.py")
  
  # Import necessary Python libraries
  py_numpy <- import("numpy")
  
  # Convert R matrix to Python ndarray
  py_image <- r_to_py(image)
  
  # Run the Marabou solver
  solver <- py_run_file("nn_solvers//tools//marabou_solver.py")
  solver$marabou_solver(epsilon, py_image, correct_class)
  
  # Remove temporary files
  unlink("temp_data//model.h5")
  unlink("temp_data//model.onnx")
}