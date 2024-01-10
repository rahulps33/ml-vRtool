# ml-vRtool
Verification tool for machine learning models in R

ml-vRtool is a dedicated machine learning model verification tool designed specifically for R users. It aims to bridge the accessibility gap by providing robust verification capabilities across various machine learning models. The tool focuses on verifying the robustness property, particularly $\varepsilon$-robustness, employing deductive verification techniques.

## Overview
There's a critical need for accessible and comprehensive machine learning model verification tools, especially for R-using researchers. Existing verification techniques, largely implemented in Python and C++, often have limitations in accessibility and scope, particularly beyond neural networks. Our work addresses this gap by introducing a tool specifically tailored for R users, offering robust verification capabilities across diverse machine learning models.


## Verification Approach

The core focus of ml-vRtool lies in verifying the robustness property, specifically targeting $\varepsilon$-robustness. This is achieved through the application of deductive verification techniques. Machine learning models are encoded in conjunction with the negation of the intended robustness property, establishing constraints within theories of linear real arithmetic. This approach effectively reduces the verification problem into a constraint satisfiability problem. To tackle this, ml-vRtool leverages satisfiability modulo theories (SMT) solvers. To address this satisfiability problem, ml-vRtool employs powerful SMT solvers.

- **Z3 Theorem Prover:** An SMT solver integrated and tailored within ml-vRtool to handle the verification of machine learning models. 

- **Marabou Integration for Neural Networks:** For neural network models, ml-vRtool converts them into the ONNX (Open Neural Network Exchange) format. This standard format enables compatibility with various state-of-the-art verification tools. Marabou, an SMT-based tool specialized in verifying neural network models, is integrated within ml-vRtool to effectively handle and verify these complex models.

By employing these solvers, ml-vRtool offers a robust means to verify the $\varepsilon$-robustness property across a range of machine learning models supported by the tool.

## Supported Machine Learning (ML) Models and Libraries
ml-vRtool provides support for various machine learning classification models using specific libraries in R:

- **Decision Tree**
    - Supported Library: `rpart`

- **Random Forest**
    - Supported Library: `randomForest`

- **Support Vector Machine (SVM)**
  - Linear Binary SVM
  - Linear Multiclass SVM
    - Supported Library: `Kernlab`

- **Neural Networks (NN)**
    - Supported Library: `keras`

## Usage

To utilize ml-vRtool for verifying machine learning models in R, follow these steps:

1. **Clone the Repository**: 
   ```bash
   git clone https://github.com/rahulps33/ml-vRtool.git
   ```
   
2. **Open the Project**: 
   - Open the project using RStudio by navigating to the cloned directory and opening `ml-vRtool.Rproj`.
   - Alternatively, double-click on `ml-vRtool.Rproj` to open it with RStudio.

3. **Example Usage**:
   For a detailed example of how to use ml-vRtool, refer to the `example.R` file in this repository. Here's a brief overview:

   - **Installing Requirements for ML Solvers**:
     Run the following command in R to install requirements for ML solvers:
     ```R
     source("requirements/requirements_ml.R")
     ```

   - **Verifying ML Models**:
     For decision tree, random forests, and SVM models, utilize the solver scripts provided in the `ml_solvers` directory as exemplified in the `example.R` file.
     For instance, for a decision tree model:
     ```R
     # Run the decision tree solver code
     source("ml_solvers/dt_solver.R")
     # Call the function for decision tree solver
     dt_solver_r(model, ref_input, epsilon_value)
     ```
     Parameters:
     - `model`: Corresponding trained machine learning model
     - `ref_input`: A 1-row dataframe with features i.e., the reference input and its corresponding class (class should be the last column). For example:
       ```R
       iris[1,]
           Sepal.Length Sepal.Width Petal.Length Petal.Width Species
       1       5.1          3.5         1.4          0.2     setosa

       ```
     - `epsilon_value`: User-defined value used to verify the $\varepsilon$-robustness of the provided reference input.

   - **Installing Requirements for NN Solvers**:
     Marabou tool integrated here supports Linux or MacOS for verifying neural network models. Follow these steps:
     - Activate the virtual environment used for training your neural network model. For example, if the environment is "r-keras", use:
       ```R
       use_virtualenv("r-keras")
       ```
     - Install required Python packages to convert the neural network model to ONNX format:
       ```R
       py_install(c("onnx", "tf2onnx", "h5py", "onnxruntime"))
       ```
     - Install Marabou tool in this environment. Instructions are available in their GitHub repository: [Marabou](https://github.com/NeuralNetworkVerification/Marabou)
       
   - **Verifying Neural Network Models**:
     - To call Marabou from `nn_solvers` directory, run:
       ```R
       source("nn_solvers/nn_solver.R")
       marabou_solver_r(model, epsilon, ref_input, class)
       ```
       For neural network models, different considerations apply compared to other models. Ensure the input matches the model's expected shape, especially when dealing with        images.


       Parameters:
       - `model` and `epsilon`: Trained neural network model and epsilon value for verifying $\varepsilon$-robustness of the provided reference input.
       - `ref_input` and `class`: Reference input and its corresponding class for neural network models. If dealing with images, ensure the input image matches the model's 
       expected input shape (e.g., 28x28 for MNIST).

## Contribution

Contributions to ml-vRtool are welcome! Feel free to submit issues, feature requests, or pull requests. Help us improve and expand the capabilities of this verification tool to serve the community better.


## Acknowledgments

Special thanks to the contributors and supporters of ml-vRtool for their valuable input and efforts in making this tool accessible and efficient for R-using researchers.

**Note:** This tool is a work-in-progress and may have limitations or ongoing developments. Your feedback and contributions are highly appreciated!
