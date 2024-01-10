
import pandas as pd
from z3 import *

# Function for verifying binary SVM model using Z3 solver
def svmbin_solver(epsilon):
  """
  Solves binary SVM using Z3 solver.

  Args:
  - epsilon: Epsilon value for constraints
  """
  # Load SVM binary coefficients and reference input
  svm_bin_coef = pd.read_csv(r"temp_data\svm_bin_coef.csv")
  ref_input = pd.read_csv(r"temp_data\sample_binary_input.csv")

  # Extract coefficients and bias from SVM binary model
  values = svm_bin_coef.iloc[0].values
  w = values[:-1].tolist() # Coefficients
  b = values[-1] # Bias term

  # Create Z3 solver instance
  solver = Solver()

  # Symbolic variables for input features
  feature_columns = ref_input.columns[:-1] # Extract feature column names from the dataframe
  X = {i: Real(feature) for i, feature in enumerate(feature_columns)} # Create Z3 variables for each feature
  R = {i: ref_input.at[0, feature] for i, feature in enumerate(feature_columns)} # Extract the values of features for the reference input R
  O = ref_input.iloc[0,-1]  
  out = Int('out')
  epsilon = RealVal(epsilon)

  # Function to add pre-constraints
  def add_pre(R, solver, X, epsilon):
    for feature in R:
      solver.add(X[feature] <= R[feature] + epsilon)
      solver.add(R[feature] - epsilon <= X[feature])

  # Function to add post-constraints
  def add_post(O, solver):
    solver.add(Not(out == O))

  # Add pre and post constraints
  add_pre(R, solver, X, epsilon)
  add_post(O, solver)

  # Add SVM binary constraints
  solver.add(Implies((Sum([w[i]*X[i] for i in range(len(w))]) + b) > 0, out == 1))
  solver.add(Implies((Sum([w[i]*X[i] for i in range(len(w))]) + b) < 0, out == -1))

  # Uncomment below line to print the solver
  #print("binary svm constraints:\n", solver)

  # Check satisfiability and get the model
  if solver.check() == sat:
    model = solver.model()
    for var_name, z3_var in X.items():
      print(f"{var_name}: {model[z3_var]}")
    print(f"Class: {model[out]}")
  else:
      print("\nUnsatisfiable.")

# Function for verifying multiclass SVM model using Z3 solver
def svm_solver(epsilon, class_list):
  """
  Solves multiclass SVM using Z3 solver.

  Args:
  - epsilon: Epsilon value for constraints
  - class_list: List of classes in the SVM model
  """
  # Load SVM  coefficients and reference input
  ref_input = pd.read_csv(r"temp_data\sample_input.csv")
  svm_coef = pd.read_csv(r"temp_data\svm_coef.csv")

  bias = svm_coef.Bias  #bias
  svm_coef = svm_coef.drop(svm_coef.columns[[0, -1]], axis=1)   #coefficients
  class_mapping = {cls: idx for idx, cls in enumerate(class_list)} # Mapping classes to integer values
  n = len(class_list)  # number of classes

  # Create Z3 solver instance
  solver = Solver()

  # Symbolic variables for input features
  feature_columns = ref_input.columns[:-1] # Extract feature column names from the dataframe
  X = {feature: Real(feature) for feature in feature_columns} # Create Z3 variables for each feature
  R = {feature: ref_input.at[0, feature] for feature in feature_columns} # Extract the values of features for the reference input R
  O = class_mapping[ref_input.iloc[0,-1]]
  out = Int('out')
  epsilon = RealVal(epsilon)

  # Function to add pre-constraints
  def add_pre(R, solver, X, epsilon):
    for feature in R:
      solver.add(X[feature] <= R[feature] + epsilon)
      solver.add(R[feature] - epsilon <= X[feature])
  
  # Function to add post-constraints
  def add_post(O, solver):
    solver.add(Not(out == O))

  # Call the functions to create Z3 constraints
  add_pre(R, solver, X, epsilon)
  add_post(O, solver)

  # Creating a variable Y_i_j to store decision values fore each pair (i,j) of distinct classes from n classes
  Y = [Real(f'Y_{i}_{j}') for i in range(1, n)  for j in range(i + 1, n + 1)]
  
  # Creating constraint for representing each binary classifier for pair (i,j)
  for index, row in svm_coef.iterrows():
    solver.add(Y[index] == Sum([value*X[column] for column, value in row.items()]) + bias[index])

  # Creating constraints to track the prediction of each binary classifier 
  # Create indicator variables for representing the predicted classes for each classifier for pair (i,j)
  ind = {}
  k=0
  for i in range(1, n):
    for j in range(i + 1, n + 1):
      # Create indicator variables
      ind[(i, i, j)] = Bool(f'ind_{i}_{i}_{j}')
      ind[(j, i, j)] = Bool(f'ind_{j}_{i}_{j}')
      # Add constraints based on Y_i_j values
      solver.add(ind[(i, i, j)] == If(Y[k] > 0, 1, 0))
      solver.add(ind[(j, i, j)] == If(Y[k] < 0, 1, 0))
      k =k+1
  
  # Creating constraints to count how many times each class c is predicted across all binary classifiers
  # Create count variables with names count_i, i = class
  count = [Int(f'count_{i}') for i in range(1, n + 1)]
  for c in range(1, n + 1):
    solver.add(count[c-1] == Sum([ind[(c, i, j)] for i in range(1, n) for j in range(i + 1, n + 1) if i == c or j == c]))

  # Creating constraint to find the most frequently predicted class 
  # Add constraints to assign the class i with max count to out
  max_count_constraint = True
  for i in range(n):
    max_count_constraint = And([count[i] >= count[j] for j in range(n) if i != j])
    solver.add(Implies(max_count_constraint, out == i))

  # Uncomment below line to print the solver
  #print("multiclass svm constraints:\n", solver)

  # Check satisfiability and get the model
  if solver.check() == sat:
    model = solver.model()
    for var_name, z3_var in X.items():
      print(f"{var_name}: {model[z3_var]}")
    print(f"Class: {next(key for key, value in class_mapping.items() if value == model[out])}")
  else:
      print("\nUnsatisfiable.")
