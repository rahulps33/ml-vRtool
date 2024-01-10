
# Load necessary libraries
library("rpart.plot")
library("reticulate")

# Activate the specific Python environment
use_virtualenv("r-reticulate")

# Function to extract rules from a decision tree model and solve using a z3 solver
dt_solver_r <- function(model, referal_input, epsilon) {
  
  # Extract rules using rpart.plot
  rules <- rpart.rules(model) # Extract rules from the decision tree model
  
  # Write rules and sample input to CSV files
  write.csv(rules, "temp_data//dt_rules.csv", row.names=FALSE)
  write.csv(referal_input, "temp_data//sample_input.csv", row.names=FALSE)
  
  # Run the decision tree solver using Z3 solver
  solver <- py_run_file("ml_solvers//z3_solvers//dt_solver.py")
  solver$dt_solver(epsilon)
  
  # Remove temporary CSV files
  unlink("temp_data//dt_rules.csv")
  unlink("temp_data//sample_input.csv")
}