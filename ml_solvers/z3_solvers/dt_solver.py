
import pandas as pd
from z3 import * 

# Function for verifying decision tree model using Z3 solver
def dt_solver(epsilon):
  """
  Solves decision tree constraints using Z3 solver.

  Args:
  - epsilon: Epsilon value for constraints
  """
  # Function to extract and structure decision tree rules
  def create_decision_tree_structure(dt_rules):
    """
    Extracts decision tree rules and structures them for further processing.

    Args:
    - dt_rules: DataFrame containing decision tree rules

    Returns:
    - List of tuples containing associated classes with their conditions
    """
    # Iterate through each row in the dataframe
    conditions = []
    for index, row in dt_rules.iterrows():
      value = []
      for col in row.index[3:]:
        value.append(str(row[col]))

      # Split the input string into individual words
      string = " ".join(value)
      words = string.split()

      # Initialize a list to store the blocks
      blocks = []
      current_block = []

      # Iterate through the words to construct blocks
      for word in words:
        if word.lower() == 'nan':
          continue
        current_block.append(word)
        if word == '&':
          blocks.append(current_block[:-1])  # Exclude the trailing '&' from the block
          current_block = []

      # Add the last block if not empty
      if current_block:
        blocks.append(current_block)

      # Construct the final condition strings
      blocks2 = []
      for block in blocks:
        if 'to' in block:
          idx = block.index('to')
          condition1 = f"{block[0]}>={block[idx - 1]}"
          blocks2.append(condition1)
          condition2 = f"{block[0]}<{block[idx + 1]}"
          blocks2.append(condition2)
        else:
          blocks2.append("".join(block))
      conditions.append(blocks2)

    class_list = dt_rules.iloc[:,0].tolist()  # Get the list of classes from the dataframe
    # Initialize a list to store the associated species for each row
    conditions_with_classes = []

    # Iterate through conditions and match with classes
    for index, condition_list in enumerate(conditions):
        classes = class_list[index]
        conditions_with_classes.append((classes, condition_list))

    return conditions_with_classes

  # Function to solve decision tree constraints using Z3 solver
  def dt_smt_solver(decision_tree_structure, ref_input, epsilon):
    """
    Solves decision tree constraints using Z3 solver.

    Args:
    - decision_tree_structure: List of tuples containing class and conditions
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
    out = Int('out')  # Varaible to store output of decision tree
    epsilon = RealVal(epsilon)

    # Functions to create Z3 constraints
    # Function to add pre-constraints
    def add_pre(R, solver, X, epsilon):
      for feature in R:
        solver.add(X[feature] <= R[feature] + epsilon)
        solver.add(R[feature] - epsilon <= X[feature])

    # Function to add post-constraints
    def add_post(O, solver):
      solver.add(Not(out == O))

    # Function to encode the decision tree model by constructing constraints for each rule in decision tree in Z3
    def add_model(decision_tree_structure, X, out, solver):
      # Create Z3 conditions and combine with And
      for classes, condition in decision_tree_structure:
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
    add_model(decision_tree_structure, X, out, solver)
    add_post(O, solver)

    # Uncomment below line to print the solver
    #print("rf constraints:\n", solver)

    # Check satisfiability and get the model
    if solver.check() == sat:
      model = solver.model()
      for var_name, z3_var in X.items():
        print(f"{var_name}: {model[z3_var]}")
      print(f"Class: {next(key for key, value in mapping.items() if value == model[out])}")
    else:
        print("\nUnsatisfiable.")
  
  # Read data and initialize variables
  dt_rules = pd.read_csv(r"temp_data\dt_rules.csv")
  ref_input = pd.read_csv(r"temp_data\sample_input.csv")

  # Mapping classes to integer values
  mapping = dict([(y,x) for x,y in enumerate(sorted(set(dt_rules.iloc[:,0])))])
  dt_rules.iloc[:,0] = [mapping[x] for x in dt_rules.iloc[:,0]]

  # Create decision tree structure and solve constraints
  decision_tree_structure = create_decision_tree_structure(dt_rules)
  dt_smt_solver(decision_tree_structure, ref_input, epsilon)
