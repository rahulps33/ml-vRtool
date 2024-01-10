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

**Note:** This tool is a work-in-progress and may have limitations or ongoing developments. Your feedback and contributions are highly appreciated!

## Supported Machine Learning Models and Libraries
ML-vRtool provides support for various machine learning models using specific libraries in R:

- **Decision Tree**
    - Supported Library: `rpart`

- **Random Forest**
    - Supported Library: `randomForest`

- **Support Vector Machine (SVM)**
  - Linear Binary SVM
  - Linear Multiclass SVM
    - Supported Library: `Kernlab`

- **Neural Networks**
    - Supported Library: `keras`

