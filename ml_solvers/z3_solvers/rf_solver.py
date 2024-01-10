
import pandas as pd
from z3 import *

# Function for verifying random forest model using Z3 solver
def rf_solver(epsilon):
  """
  Solves the random forest using Z3 solver.

  Args:
  - epsilon: Epsilon value for constraints
  """
  # Function to extract and structure random forest rules
  def create_rf_structure(rf_rules):
    """
    Extracts and structures rules for each tree in the random forest.

    Args:
    - rf_rules: DataFrame containing rules for random forest

    Returns:
    - List of tuples containing associated classes with their conditions for each tree
    """
    # Get unique ntree values
    unique_ntree_values = rf_rules['ntree'].unique()

    # Initialize an empty list to store all trees
    all_trees = []

    # Iterate over unique ntree values
    for tree_num in unique_ntree_values:
      # Filter the DataFrame for the current tree number
      tree_data = rf_rules[rf_rules['ntree'] == tree_num]

      # Initialize an empty list to store rules for this tree
      tree_rules = []

      # Iterate over each row of the filtered data
      for _, row in tree_data.iterrows():
        # Split the condition by ' & ' to get individual conditions
        conditions = row['condition'].split(' & ')

        # Store the rule and class/prediction for this condition
        rule = conditions
        class_prediction = row['pred']

        # Add the rule and class to the list for this tree
        #tree_rules.append({'class': class_prediction, 'rule': rule})
        tree_rules.append((class_prediction, rule))

      # Add the list of rules for this tree to the list of all trees
      all_trees.append(tree_rules)
    return all_trees

  # Function encodes the random forest model into constraints in z3 and solves using z3 solver
  def rf_smt_solver(rf_structure, ref_input, epsilon):
    """
    Encodes the random forest model into Z3 constraints and solves using Z3 solver.

    Args:
    - rf_structure: List of tuples containing associated classes with their conditions
    - ref_input: Reference input data
    - epsilon: Epsilon value for constraints
    """
    # Create Z3 solver instance
    solver = Solver()

    # Symbolic variables for input features
    feature_columns = ref_input.columns[:-1] # Extract feature column names from the dataframe
    X = {feature: Real(feature) for feature in feature_columns} # Create Z3 variables for each feature
    R = {feature: ref_input.at[0, feature] for feature in feature_columns} # Extract the values of features for the reference input R
    O = mapping[ref_input.iloc[0,-1]]
    final_out = Int('final_out') # Variable to store final output of random forest
    out = [Int('out_' + str(i)) for i in range(len(rf_rules['ntree'].unique()))] # Variable to store output of each tree  
    epsilon = RealVal(epsilon)  
    
    # Function to add pre-constraints
    def add_pre(R, solver, X, epsilon):
      for feature in R:
        solver.add(X[feature] <= R[feature] + epsilon)
        solver.add(R[feature] - epsilon <= X[feature])

    # Function to add post-constraints
    def add_post(O, solver):
      solver.add(Not(final_out == O))
    
    # Function to encode each tree in the random forest as constraints in Z3
    def add_model(rf_structure, X, out, solver):
      # Create Z3 conditions and combine with And
      for classes, condition in rf_structure:
        z3_condition = True  # Initialize with True for AND operations
        for term in condition:
          possible_operators = ['<=', '>=', '<', '>']
          operator = None
          for op in possible_operators:
            if op in term:
              operator = op
              break
          if operator is None:
            continue  # Handle cases where no operator is found

          variable_name, value = term.split(operator)
          z3_var = X[variable_name]  # Get the corresponding Z3 variable

          if operator == '<':
            z3_condition = And(z3_condition, z3_var < float(value))
          elif operator == '>':
            z3_condition = And(z3_condition, z3_var > float(value))
          elif operator == '<=':
            z3_condition = And(z3_condition, z3_var <= float(value))
          elif operator == '>=':
            z3_condition = And(z3_condition, z3_var >= float(value))

        # Add the implication to the solver
        solver.add(Implies(z3_condition, out == classes))

    # Call the functions to create Z3 constraints
    add_pre(R, solver, X, epsilon)
    add_post(O, solver)
    for i in range(len(rf_structure)):
      add_model(rf_structure[i], X, out[i], solver)
    
    # Creating constraints to track the prediction of each tree 
    # Create indicator variables with names 'ind_i_j' for each combination of i = trees and j = class
    ind = [Bool(f'ind_{i}_{j}') for i in range(len(rf_rules['ntree'].unique())) for j in range(len(rf_rules['pred'].unique()))]

    # Add constraints: ind_i_j == 1 if out_i == j, else ind_i_j == 0
    for i in range(len(rf_rules['ntree'].unique())):
      for j in range(len(rf_rules['pred'].unique())):
        solver.add(ind[i * len(rf_rules['pred'].unique()) + j] == If(out[i] == j, 1, 0))
    
    # Creating constraints to count how many times each class is predicted across all trees
    # Create count variables with names count_j, j = class
    count = [Int(f'count_{i}') for i in range(len(rf_rules['pred'].unique()))]

    # Add constraints: count_j == summ i=trees: ind_i_j
    for j in range(len(rf_rules['pred'].unique())):
      solver.add(count[j] == Sum([ind[i * len(rf_rules['pred'].unique()) + j] for i in range(len(rf_rules['ntree'].unique()))]))

    # Creating constraint to find the most frequently predicted class 
    # Add constraints to assign the class i with max count to final_out
    max_count_constraint = True
    for i in range(len(rf_rules['pred'].unique())):
      max_count_constraint = And([count[i] >= count[j] for j in  range(len(rf_rules['pred'].unique())) if i != j])
      solver.add(Implies(max_count_constraint, final_out == i))

    # Uncomment below line to print the solver
    #print("rf constraints:\n", solver)

    # Check satisfiability and get the model
    if solver.check() == sat:
      model = solver.model()
      for var_name, z3_var in X.items():
        print(f"{var_name}: {model[z3_var]}")
      print(f"Class: {next(key for key, value in mapping.items() if value == model[final_out])}")
    else:
        print("\nUnsatisfiable.")

  # Read data and initialize variables
  rf_rules = pd.read_csv(r"temp_data\rf_rules.csv")
  ref_input = pd.read_csv(r"temp_data\sample_input.csv")

  # Mapping classes to integer values
  mapping = dict([(y,x) for x,y in enumerate(sorted(set(rf_rules['pred'])))])
  rf_rules['pred'] = [mapping[x] for x in rf_rules['pred']]

  # Create random forest structure and solve constraints
  rf_structure = create_rf_structure(rf_rules)
  rf_smt_solver(rf_structure, ref_input, epsilon)
