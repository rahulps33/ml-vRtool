
# Load necessary libraries
library(kernlab)

# Activate the specific Python environment
use_virtualenv("r-reticulate")

# Function to extract rules for binary SVM model using a z3 solver
svmbin_solver_r <- function(model, referal_input, epsilon) {
  
  # Extracting weights and bias from the model
  weight = model@coef[[1]] %*% model@xmatrix[[1]]
  bias = model@b
  
  # Create a data frame for this separation
  svm_bin_coef <- data.frame(weight, bias = bias)
  
  # Write rules and sample input to CSV files
  write.csv(svm_bin_coef, "temp_data//svm_bin_coef.csv", row.names=FALSE)
  write.csv(referal_input, "temp_data//sample_binary_input.csv", row.names=FALSE)
  
  # Run the binary SVM solver in Z3
  solver <- py_run_file("ml_solvers//z3_solvers//svm_solver.py")
  solver$svmbin_solver(epsilon)
  
  # Remove temporary CSV files
  unlink("temp_data//svm_bin_coef.csv")
  unlink("temp_data//sample_binary_input.csv")
}


# Function to extract rules for multiclass SVM model using a z3 solver
svm_solver_r <- function(model, referal_input, epsilon) {
  
  # Get the number of classes
  n <- model@nclass
  
  # Calculate the total number of separation planes
  #k <- choose(n,2)  #n * (n - 1) / 2
  k <- 1
  svm_coef <- data.frame()
  
  # Calculate weights and biases for all separation planes
  for (i in 1:(n - 1)) {
    for (j in (i + 1):n) {
      # Extract weights for the i vs. j separation
      coef_ij <- model@coef[[k]] %*% model@xmatrix[[k]]
      # Calculate the bias term for the i vs. j separation
      bias_ij <- model@b[k]
      
      # Create a data frame for this separation
      separation_plane <- data.frame(hyperplane = paste(i, "_", j), coef_ij, Bias = bias_ij)
      
      # Append the data frame to the result dataframe
      svm_coef <- rbind(svm_coef, separation_plane)
      k <- k + 1
    }
  }
  
  # Write rules and sample input to CSV files
  write.csv(svm_coef, "temp_data//svm_coef.csv", row.names=FALSE)
  write.csv(referal_input, "temp_data//sample_input.csv", row.names=FALSE)
  
  # Run the svm solver in z3
  solver <- py_run_file("ml_solvers//z3_solvers//svm_solver.py")
  solver$svm_solver(epsilon, model@lev)
  
  # Remove temporary CSV files
  unlink("temp_data//svm_coef.csv")
  unlink("temp_data//sample_binary_input.csv")
}