# Function for solving using Marabou solver
def marabou_solver(epsilon, image, correct_class):
  """
    Verifies the NN model using Marabou solver.

    Args:
    - epsilon: The epsilon value
    - image: The input image for evaluation
    - correct_class: The correct class for the input image

    Returns:
    - vals: The values calculated by the solver
    - stats: The statistics obtained during the solving process
    - maxClass: The class determined by the solver
  """

  from maraboupy import Marabou
  from maraboupy import MarabouCore
  
  # Read the ONNX model
  network = Marabou.read_onnx(r"temp_data\model.onnx")
  
  # Set solver options
  options = Marabou.createOptions(verbosity = 0)
  
   # Evaluate local robustness
  vals, stats, maxClass = network.evaluateLocalRobustness(input=image, epsilon=epsilon, originalClass=correct_class, verbose=False, options=options)
  
  return vals, stats, maxClass
